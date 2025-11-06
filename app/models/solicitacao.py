from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import Base # Importa a Base declarativa

# Herda da classe Base para ser mapeado pelo SQLAlchemy
class Solicitacao(Base):
    __tablename__ = "solicitacao"

    id = Column(Integer, primary_key=True, index=True)
    data_solicitacao = Column(Date, nullable=False)
    status = Column(String(15), nullable=False, default="pendente") # Status: pendente, em_avaliacao, aprovado, recusado, cancelado
    motivo_recusa = Column(Text)
    animal_id = Column(Integer, ForeignKey("animal.id"), nullable=False) # FK garante vínculo a um animal.id
    adotante_id = Column(Integer, ForeignKey("adotante.id"), nullable=False) # FK garante vínculo a um adotante.id

    # Relacionamentos: Muitas Solicitações para um Animal / Adotante
    animal = relationship("Animal", back_populates="solicitacoes")
    adotante = relationship("Adotante", back_populates="solicitacoes")

    # Uma Solicitação para muitas Visitas
    visitas = relationship("Visita", back_populates="solicitacao")

    # Mostra o número da Solicitação no SQLAdmin (dropdowns)
    def __str__(self) -> str:
        return f"Solicitação #{self.id} ({self.status})"