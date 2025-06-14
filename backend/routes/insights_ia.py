from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import InsightIA

router = APIRouter(tags=["InsightsIA"])

@router.get("/")
def list_insights(
    response: Response,
    chamado_id: int,
    db: Session = Depends(get_db),
    _start: int = Query(0, alias="_start"),
    _end:   int = Query(10, alias="_end"),
):
    query = db.query(InsightIA).filter_by(chamado_id=chamado_id)
    total = query.count()
    insights = query.offset(_start).limit(_end - _start).all()
    end = _start + len(insights) - 1 if total else 0
    response.headers["Content-Range"] = f"{_start}-{end}/{total}"
    return insights
