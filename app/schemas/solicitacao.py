from datetime import date
from pydantic import BaseModel, Field
from typing import Literal, Optional

Status = Literal["pendente", "em_avaliacao", "aprovado", "recusado", "cancelado"]

class SolicitacaoBase(BaseModel):
    animal_id: int
    adotante_id: int
    data_solicitacao: date = Field(default_factory=date.today) 

class SolicitacaoCreate(SolicitacaoBase):
    pass

class SolicitacaoUpdate(BaseModel):
    status: Status | None = None
    motivo_recusa: str | None = None

class SolicitacaoOut(SolicitacaoBase):
    id: int 
    status: Status
    motivo_recusa: str | None = None

    class Config:
        from_attributes = True