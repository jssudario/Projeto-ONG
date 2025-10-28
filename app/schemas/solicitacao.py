from datetime import date
from pydantic import BaseModel, Field # type: ignore # Field: restrições: max, min, default, etc
from typing import Literal

Status = Literal["pendente", "em_avaliacao", "aprovado", "recusado", "cancelado"]

class SolicitacaoBase(BaseModel):
    # todos campos obrigatórios
    animal_id: int
    adotante_id: int
    data_solicitacao: date = Field(default_factory=date.today) # data de hoje

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


