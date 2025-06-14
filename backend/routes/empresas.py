from fastapi import APIRouter, Depends, Response, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Empresa

router = APIRouter(tags=["Empresas"])

@router.get("/")
def list_empresas(
    response: Response,
    db: Session = Depends(get_db),
    _start: int = Query(0, alias="_start"),
    _end:   int = Query(10, alias="_end"),
):
    total = db.query(Empresa).count()
    empresas = (
        db.query(Empresa)
          .offset(_start)
          .limit(_end - _start)
          .all()
    )
    end = _start + len(empresas) - 1 if total else 0
    response.headers["Content-Range"] = f"{_start}-{end}/{total}"
    return empresas
