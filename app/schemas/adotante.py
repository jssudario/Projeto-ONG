from datetime import date
from pydantic import BaseModel, Field, EmailStr

class AdotanteBase(BaseModel):
    nome_completo: str = Field(min_length=1, max_length=255)
    cpf: str = Field(min_length=11, max_length=11)
    data_nascimento: date
    email: EmailStr 
    telefone: str 
    endereco: str

class AdotanteCreate(AdotanteBase):
    pass

class AdotanteUpdate(AdotanteBase):
    nome_completo: str | None = None
    cpf: str | None = Field(default=None, min_length=11, max_length=11) 
    data_nascimento: date | None = None
    email: EmailStr | None = None
    telefone: str | None = None
    endereco: str | None = None

class AdotanteOut(AdotanteBase):
    id: int

    class Config:
        from_attributes = True