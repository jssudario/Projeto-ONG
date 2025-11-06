from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import Base  # Importa a Base declarativa

# Herda da classe Base para ser mapeado pelo SQLAlchemy
class Visita(Base):
    __tablename__ = "visita"

    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, nullable=False)
    retorno = Column(String(15), nullable=False, default="pendente")  # Status: aprovado, reprovado, pendente
    observacoes = Column(Text)
    solicitacao_id = Column(Integer, ForeignKey("solicitacao.id"), nullable=False)

    # Relacionamentos: Muitas Visitas pertencem a uma Solicitação
    solicitacao = relationship("Solicitacao", back_populates="visitas")

    # Mostra o número da Visita no SQLAdmin (dropdowns)
    def __str__(self) -> str:
        return f"Visita #{self.id} - {self.retorno}"
