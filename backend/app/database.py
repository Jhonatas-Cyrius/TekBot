# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carrega .env
base_dir = os.path.dirname(os.path.dirname(__file__))  # aponta para backend/
dotenv_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path)

# backend/app/database.py
load_dotenv()  
DATABASE_URL = os.getenv("DATABASE_URL")
print("▶️ DATABASE_URL carregada:", DATABASE_URL)    # <-- adicione esta linha

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não encontrada em .env")

# Cria engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,    # mostra no console as queries SQL
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

Base = declarative_base()

def get_db():
    """Dependency do FastAPI para fornecer a sessão do SQLAlchemy."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()