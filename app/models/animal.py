from sqlalchemy import Integer, String, Boolean, Date, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from app.core.base import Base
from fastapi_storages import FileSystemStorage # Integração de upload local
from fastapi_storages.integrations.sqlalchemy import FileType

# Onde salvar os arquivos e como serão servidos
storage = FileSystemStorage(path="static/uploads") # path: Pasta real no disco

# Herda da classe Base para ser mapeado pelo SQLAlchemy
class Animal(Base):
    __tablename__ = "animal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(80), nullable=False)
    especie: Mapped[str] = mapped_column(String(30), nullable=False)
    raca: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    sexo: Mapped[str] = mapped_column(String(10), nullable=False)
    idade_meses: Mapped[int] = mapped_column(Integer, nullable=False)
    porte: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    castrado: Mapped[bool] = mapped_column(Boolean, default=False)
    vacinado: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(15), nullable=False, default="disponivel")
    data_entrada: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    observacoes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Campo de upload de imagem
    # O valor salvo no banco de dados será a URL relativa (/uploads/nome-arquivo.jpg)
    foto: Mapped[Optional[str]] = mapped_column(FileType(storage=storage), nullable=True)

    solicitacoes = relationship("Solicitacao", back_populates="animal")

    # Mostra o nome do Animal no SQLAdmin (dropdowns)
    def __str__(self) -> str:
        return self.nome or f"Animal #{self.id}"