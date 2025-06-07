# 1) Arquivo: backend/routes/webhook.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Mensagem, Chamado, Empresa
from datetime import datetime

router = APIRouter()

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhook", status_code=200)
async def receive_message(payload: dict, db: Session = Depends(get_db)):
    """
    Recebe JSON com {'from': '<jid>@c.us', 'body': '<texto>'}
    Cria um Chamado (se necessário) e armazena a Mensagem no banco.
    """
    origem = payload.get("from")
    texto = payload.get("body")
    if not origem or not texto:
        raise HTTPException(400, "Payload inválido")

    # Exemplo: sempre criamos um chamado novo (você pode aprimorar)
    empresa = db.query(Empresa).filter_by(id=1).first()
    if not empresa:
        raise HTTPException(404, "Empresa padrão não encontrada")

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

    msg = Mensagem(
        chamado_id=chamado.id,
        remetente="Cliente",
        conteudo=texto,
        origem="WhatsApp",
        data_hora=datetime.utcnow()
    )
    db.add(msg)
    db.commit()

    return {"status": "ok", "chamado_id": chamado.id}