from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey # importa as ferramentas
from app.core.database import Base # importa base
from sqlalchemy.orm import relationship

class Visita(Base):
    __tablename__ = "visita"

    id = Column(Integer, primary_key=True, index=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacao.id"), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    retorno = Column(String(15), nullable=False, default="pendente") # aprovado, reprovado, pendente
    observacoes = Column(Text)

    # ponte solicitacao -> visita 
    solicitacao = relationship("Solicitacao", back_populates="visitas")

# ForeignKey -> garante que uma visita não pode ser criada se solicitacao_id nao existir na tabela solicitacao