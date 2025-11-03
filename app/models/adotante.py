from sqlalchemy import Column, Integer, String, Date, Text # importa as ferramentas
from app.core.database import Base # importa base
from sqlalchemy.orm import relationship

class Adotante(Base):
    __tablename__ = "adotante"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    data_nascimento = Column(Date, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    telefone = Column(String(15), nullable=False)
    endereco = Column(Text, nullable=False)

    solicitacoes = relationship("Solicitacao", back_populates="adotante")