from datetime import date
from pydantic import BaseModel, Field, EmailStr # type: ignore # Field: restrições: max, min, default, etc

class AdotanteBase(BaseModel):
    # todos campos obrigatórios
    nome_completo: str = Field(min_length=1, max_length=255)
    cpf: str = Field(min_length=11, max_length=11)
    data_nascimento: date
    email: EmailStr # obriga email válido
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




