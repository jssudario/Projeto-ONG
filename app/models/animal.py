from sqlalchemy import Column, Integer, String, Boolean, Date, Text # importa as ferramentas
from app.core.database import Base # importa base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType

uploads_storage = FileSystemStorage(
    path="static/uploads", # onde salvar no disco
)
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

    foto_url: Mapped[FileType] = mapped_column(FileType(storage=uploads_storage)) # guarda o caminho da foto

    solicitacoes = relationship("Solicitacao", back_populates="animal")

# nullable=False torna campo obrigatório
