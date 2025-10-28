from datetime import datetime
from pydantic import BaseModel # type: ignore # Field: restrições: max, min, default, etc
from typing import Literal

Retorno = Literal["aprovado", "reprovado", "pendente"]

class VisitaBase(BaseModel):
    # campos obrigatórios
    solicitacao_id: int
    data_hora: datetime
    retorno: Retorno = "pendente"

    # campos opcionais
    observacoes: str | None = None

class VisitaCreate(VisitaBase):
    pass

class VisitaUpdate(BaseModel):
    retorno: Retorno | None = None
    data_hora: datetime | None = None
    observacoes: str | None = None

class VisitaOut(VisitaBase):
    id: int
    class Config:
        from_attributes = True









    # id = Column(Integer, primary_key=True, index=True)
    # solicitacao_id = Column(Integer, ForeignKey("solicitacao.id"), nullable=False)
    # data_hora = Column(DateTime, nullable=False)
    # retorno = Column(String(15), nullable=False, default="pendente") # aprovado, reprovado, pendente
    # observacoes = Column(Text)
