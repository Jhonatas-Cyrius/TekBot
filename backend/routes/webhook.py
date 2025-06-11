# backend/routes/webhook.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Mensagem, Chamado, Empresa
from app.ai_utils import classify_issue
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhook", status_code=200)
async def receive_message(payload: dict, db: Session = Depends(get_db)):
    print("➡️ [Webhook] payload recebido:", payload)
    origem = payload.get("from"); texto = payload.get("body")
    if not origem or not texto:
        raise HTTPException(400, "Payload inválido")

    telefone = origem.split("@")[0]
    empresa = db.query(Empresa).filter_by(contato=telefone).first()
    if not empresa:
        empresa = Empresa(nome_fantasia=telefone, contato=telefone)
        db.add(empresa); db.commit(); db.refresh(empresa)

    chamado = (
        db.query(Chamado)
          .filter_by(empresa_id=empresa.id, status="Aberto")
          .order_by(Chamado.data_criacao.desc())
          .first()
    )
    if not chamado:
        chamado = Chamado(
            empresa_id=empresa.id,
            tipo_problema="Desconhecido",
            prioridade="Média",
            status="Aberto",
            data_criacao=datetime.utcnow()
        )
        db.add(chamado); db.commit(); db.refresh(chamado)

    # INVOCAR A NOVA IA VIA HTTP
    print(f"🔍 [IA] classificando texto: {texto}")
    tipo, prioridade = await classify_issue(texto)
    chamado.tipo_problema = tipo
    chamado.prioridade    = prioridade
    db.commit(); db.refresh(chamado)
    print(f"✅ Chamado atualizado: tipo={tipo}, prioridade={prioridade}")

    msg = Mensagem(
        chamado_id=chamado.id,
        remetente="Cliente",
        conteudo=texto,
        origem="WhatsApp",
        data_hora=datetime.utcnow()
    )
    db.add(msg); db.commit()

    return {"status": "ok", "chamado_id": chamado.id}
