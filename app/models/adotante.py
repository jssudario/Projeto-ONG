from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.core.base import Base # Importa a Base declarativa

# Herda da classe Base para ser mapeado pelo SQLAlchemy
class Adotante(Base):
    __tablename__ = "adotante"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    data_nascimento = Column(Date, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    telefone = Column(String(15), nullable=False)
    estado = Column(String(2), nullable=False)  # Sigla
    cidade = Column(String(100), nullable=False)
    rua = Column(String(200), nullable=False)
    numero = Column(String(30), nullable=True)
    complemento = Column(String(100), nullable=True)

    # Relacionamentos: Um Adotante pode ter muitas Solicitações
    solicitacoes = relationship("Solicitacao", back_populates="adotante")

    # Mostra o nome do Adotante no SQLAdmin (dropdowns)
    def __str__(self) -> str:
        return self.nome_completo or f"Adotante #{self.id}"