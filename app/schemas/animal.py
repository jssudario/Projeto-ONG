from datetime import date
from pydantic import BaseModel, Field
from typing import Literal, Optional

Sexo = Literal["macho", "femea"]
Porte = Literal["pequeno", "medio", "grande"]
Especie = Literal["cachorro", "gato"] 

class AnimalBase(BaseModel):
    # Campos obrigatórios
    nome: str = Field(min_length=1, max_length=80) 
    especie: Especie
    raca: str = Field(min_length=1, max_length=60)
    sexo: Sexo 
    idade_meses: int = Field(ge=0) # 'ge=0' > Impede idade negativa
    porte: Porte

    # Campos opcionais (com valores default)
    castrado: bool = False
    vacinado: bool = False
    status: str = "disponivel"
    data_entrada: date | None = None
    observacoes: str | None = None

class AnimalCreate(AnimalBase):
    pass

class AnimalUpdate(AnimalBase):
    nome: str | None = None
    especie: Especie | None = None
    raca: str | None = None
    sexo: Sexo | None = None
    idade_meses: int | None = Field(default=None, ge=0)
    porte: Porte | None = None
    castrado: bool | None = None
    vacinado: bool | None = None
    status: str | None = None
    data_entrada: date | None = None
    observacoes: str | None = None
class AnimalOut(BaseModel):
    id: int
    nome: str
    especie: str 
    raca: Optional[str] = None 
    sexo: str
    idade_meses: int
    porte: Optional[str] = None 
    castrado: bool
    vacinado: bool
    status: str
    data_entrada: Optional[date] = None
    observacoes: Optional[str] = None
    
    class Config:
        from_attributes = True