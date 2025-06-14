# backend/routes/mensagens.py

from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models import Mensagem

router = APIRouter(tags=["Mensagens"])

@router.get("/")
async def list_mensagens(
    response: Response,
    filter: str = Query("{}", alias="filter"),
    _start: int = Query(0, alias="_start"),
    _end:   int = Query(10, alias="_end"),
    db: Session = Depends(get_db),
):
    # 1) Parseia o filtro JSON
    try:
        filters = json.loads(filter)
    except json.JSONDecodeError:
        filters = {}
    # 2) Extrai e converte chamado_id, se for válido
    chamado_id = filters.get("chamado_id")
    try:
        chamado_id = int(chamado_id)
    except (TypeError, ValueError):
        chamado_id = None

    # 3) Monta query, opcionalmente filtrando
    query = db.query(Mensagem)
    if chamado_id is not None:
        query = query.filter(Mensagem.chamado_id == chamado_id)

    # 4) Conta total e busca o slice
    total = query.count()
    msgs = query.offset(_start).limit(_end - _start).all()

    # 5) Prepara header Content-Range
    end = (_start + len(msgs) - 1) if total else 0
    response.headers["Content-Range"] = f"{_start}-{end}/{total}"

    return msgs
