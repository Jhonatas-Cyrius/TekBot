# backend/app/main.py
from fastapi import FastAPI
from .database import engine, Base
# (quando criar rotas, importe-as aqui)
# from .routes import chamados

app = FastAPI(title="TekBot API")

@app.on_event("startup")
def on_startup():
    # Cria todas as tabelas no banco (se ainda não existirem)
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "TekBot API está funcionando"}

# Se tiver um arquivo backend/routes/chamados.py expondo um APIRouter, faça:
# app.include_router(chamados.router, prefix="/chamados", tags=["Chamados"])
