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
    # 1) log para confirmar que o POST chegou
    print("➡️ [Webhook] payload recebido:", payload)

    origem = payload.get("from")
    texto  = payload.get("body")
    if not origem or not texto:
        raise HTTPException(400, "Payload inválido")

    telefone = origem.split("@")[0]

    # 2) get or create Empresa
    empresa = db.query(Empresa).filter_by(contato=telefone).first()
    if not empresa:
        empresa = Empresa(nome_fantasia=telefone, contato=telefone)
        db.add(empresa)
        db.commit()
        db.refresh(empresa)

    # 3) agrupar em Chamado aberto
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
        db.add(chamado)
        db.commit()
        db.refresh(chamado)

    # 4) log antes de chamar a IA
    print(f"🔍 [IA] classificando texto: {texto}")

    # 5) chamada à IA
    try:
        tipo, prioridade = await classify_issue(texto)
        print(f"🔍 [IA] retornou: tipo={tipo}, prioridade={prioridade}")
        chamado.tipo_problema = tipo
        chamado.prioridade    = prioridade
        db.commit()
        db.refresh(chamado)
    except Exception as e:
        print("❌ [IA] falha ao classificar:", e)

    # 6) persiste a mensagem
    msg = Mensagem(
        chamado_id = chamado.id,
        remetente   = "Cliente",
        conteudo    = texto,
        origem      = "WhatsApp",
        data_hora   = datetime.utcnow()
    )
    db.add(msg)
    db.commit()

    return {"status": "ok", "chamado_id": chamado.id}
