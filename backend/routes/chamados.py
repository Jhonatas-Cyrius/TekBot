from fastapi import APIRouter, Depends, Response, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Chamado, Empresa
from datetime import datetime

router = APIRouter(tags=["Chamados"])


@router.get("/")
def list_chamados(
    response: Response,
    db: Session = Depends(get_db),
    _start: int = Query(0, alias="_start"),
    _end:   int = Query(10, alias="_end"),
):
    total = db.query(Chamado).count()
    chamados = (
        db.query(Chamado)
          .offset(_start)
          .limit(_end - _start)
          .all()
    )
    # Expondo total para o React-Admin
    if total:
        end = _start + len(chamados) - 1
    else:
        end = 0
    response.headers["Content-Range"] = f"{_start}-{end}/{total}"
    return chamados
