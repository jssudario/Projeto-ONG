from sqlalchemy import Column, Integer, String, Boolean, Date, Text # importa as ferramentas
from .database import Base # importa base

# classe Animal
class Animal(Base):
    __tablename__ = "animal"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(80), nullable=False)
    especie = Column(String(30), nullable=False) # cachorro, gato, etc.
    raca = Column(String(60))
    sexo = Column(String(10), nullable=False ) # macho, fêmea
    idade_meses = Column(Integer, nullable=False)
    porte = Column(String(15)) # pequeno, medio, grande
    castrado = Column(Boolean, default=False)
    vacinado = Column(Boolean, default=False)
    status = Column(String(15), nullable=False, default="disponivel") # disponivel, reservado, adotado
    data_entrada = Column(Date)
    observacoes = Column(Text)

# nullable=False torna campo obrigatório
