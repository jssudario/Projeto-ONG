from datetime import date
from pydantic import BaseModel, Field, ConfigDict # type: ignore # Field: restrições: max, min, default, etc
from typing import Literal

Sexo = Literal["macho", "femea"]
Porte = Literal["pequeno", "medio", "grande"]
Especie = Literal["cachorro", "gato"] 

class AnimalBase(BaseModel):
    # campos obrigatórios
    nome: str = Field(min_length=1, max_length=80) 
    especie: Especie
    raca: str = Field(min_length=1, max_length=60)
    sexo: Sexo
    idade_meses: int = Field(ge=0) # impede inserir idade negativa
    porte: Porte

    # campos opcionais
    # cadastrado e vacinado ficam com default False de padrão
    castrado: bool = False
    vacinado: bool = False
    status: str = "disponivel" # default é disponivel
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

class AnimalOut(AnimalBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True

        