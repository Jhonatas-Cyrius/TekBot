# backend/app/main.py

from fastapi import FastAPI
from app.database import engine, Base
import app.models

from routes.chamados import router as chamados_router
from routes.webhook   import router as webhook_router

app = FastAPI(title="TekBot API")
app.include_router(webhook_router, prefix="", tags=["Webhook"])

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "TekBot API está funcionando"}

# Roteadores existentes
app.include_router(chamados_router, prefix="/chamados", tags=["Chamados"])
app.include_router(webhook_router, prefix="",          tags=["Webhook"])
