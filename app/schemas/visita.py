from datetime import datetime
from pydantic import BaseModel
from typing import Literal, Optional

Retorno = Literal["aprovado", "reprovado", "pendente"]

class VisitaBase(BaseModel):
    # Campos obrigatórios
    solicitacao_id: int
    data_hora: datetime
    retorno: Retorno = "pendente"

    # Campos opcionais
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