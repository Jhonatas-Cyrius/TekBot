# backend/routes/chamados.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Chamado, Empresa, Tecnico
from datetime import datetime

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_chamado(
    empresa_id: int,
    tipo_problema: str,
    prioridade: str,
    db: Session = Depends(get_db)
):
    # opcional: validar se empresa existe
    if not db.query(Empresa).filter_by(id=empresa_id).first():
        raise HTTPException(404, "Empresa não encontrada")
    chamado = Chamado(
        empresa_id=empresa_id,
        tipo_problema=tipo_problema,
        prioridade=prioridade,
        status="Aberto",
        data_criacao=datetime.utcnow()
    )
    db.add(chamado)
    db.commit()
    db.refresh(chamado)
    return chamado

# READ ALL
@router.get("/")
def list_chamados(db: Session = Depends(get_db)):
    return db.query(Chamado).all()

# READ ONE
@router.get("/{chamado_id}")
def get_chamado(chamado_id: int, db: Session = Depends(get_db)):
    chamado = db.query(Chamado).filter_by(id=chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    return chamado

# UPDATE
@router.put("/{chamado_id}")
def update_chamado(
    chamado_id: int,
    status: str = None,
    solucao: str = None,
    data_fechamento: datetime = None,
    db: Session = Depends(get_db)
):
    chamado = db.query(Chamado).filter_by(id=chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    if status:
        chamado.status = status
    if solucao:
        chamado.solucao = solucao
    if data_fechamento:
        chamado.data_fechamento = data_fechamento
    db.commit()
    db.refresh(chamado)
    return chamado

# DELETE (opcional)
@router.delete("/{chamado_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chamado(chamado_id: int, db: Session = Depends(get_db)):
    chamado = db.query(Chamado).filter_by(id=chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    db.delete(chamado)
    db.commit()
    return
