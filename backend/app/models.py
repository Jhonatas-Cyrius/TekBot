# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Tecnico(Base):
    __tablename__ = "tecnicos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)

class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    nome_fantasia = Column(String, nullable=False)
    cnpj = Column(String, nullable=True)
    contato = Column(String, nullable=True)
    telefone = Column(String, nullable=True)

class Chamado(Base):
    __tablename__ = "chamados"
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=True)
    tipo_problema = Column(String, nullable=False)
    prioridade = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Aberto")
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_fechamento = Column(DateTime(timezone=True), nullable=True)
    solucao = Column(Text, nullable=True)

class Mensagem(Base):
    __tablename__ = "mensagens"
    id = Column(Integer, primary_key=True, index=True)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)
    remetente = Column(String, nullable=False)  # "Cliente", "Técnico" ou "IA"
    conteudo = Column(Text, nullable=False)
    data_hora = Column(DateTime(timezone=True), server_default=func.now())
    origem = Column(String, nullable=False)     # "WhatsApp", "Painel", "Interno"

class InsightIA(Base):
    __tablename__ = "insights_ia"
    id = Column(Integer, primary_key=True, index=True)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)
    resumo = Column(Text, nullable=True)
    sugestoes = Column(Text, nullable=True)
    similares = Column(Text, nullable=True)      # IDs semelhantes em JSON, por ex.
    data_gerado = Column(DateTime(timezone=True), server_default=func.now())

class LogSistema(Base):
    __tablename__ = "logs_sistema"
    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime(timezone=True), server_default=func.now())
    usuario = Column(String, nullable=False)     # "Técnico", "IA", "Sistema"
    acao = Column(String, nullable=False)        # Ex: "mensagem_recebida", "chamado_criado"
    descricao = Column(Text, nullable=True)      # Descrição legível do evento
    origem = Column(String, nullable=True)       # "API", "Web", "WhatsApp"
