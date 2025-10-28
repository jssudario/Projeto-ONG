from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey # importa as ferramentas
from app.core.database import Base # importa base
from sqlalchemy.orm import relationship

class Solicitacao(Base):
    __tablename__ = "solicitacao"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animal.id"), nullable=False)
    adotante_id = Column(Integer, ForeignKey("adotante.id"), nullable=False)
    data_solicitacao = Column(Date, nullable=False)
    status = Column(String(15), nullable=False, default="pendente") # pendente, em_avaliacao, aprovado, recusado, cancelado
    motivo_recusa = Column(Text)


    animal = relationship("Animal", back_populates="solicitacoes") 
    adotante = relationship("Adotante", back_populates="solicitacoes")
    visitas = relationship("Visita", back_populates="solicitacao")
