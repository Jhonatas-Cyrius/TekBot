# backend/app/main.py

from fastapi import FastAPI
from app.database import engine, Base
import app.models
from routes.chamados import router as chamados_router
from routes.webhook   import router as webhook_router
from routes.empresas import router as empresas_router
from routes.mensagens import router as mensagens_router
from routes.insights_ia import router as insights_router
from routes.tests import router as tests_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1) Cria a instância do FastAPI **antes** de usar include_router
app = FastAPI(title="TekBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # ou restrinja p/ localhost:3000,3001…
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range"],  # <–– aqui
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "TekBot API está funcionando"}

# 2) Agora sim inclua todos os routers
app.include_router(chamados_router,   prefix="/chamados",   tags=["Chamados"])
app.include_router(empresas_router,   prefix="/empresas",   tags=["Empresas"])
app.include_router(mensagens_router,  prefix="/mensagens",  tags=["Mensagens"])
app.include_router(insights_router,   prefix="/insights_ia", tags=["InsightsIA"])
app.include_router(tests_router, prefix="/tests", tags=["Tests"])


