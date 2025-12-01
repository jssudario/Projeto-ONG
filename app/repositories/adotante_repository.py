from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List, Optional
from app.core.database import get_db
from app.models import adotante as adotante_model
from app.schemas import adotante as adotante_schema

# Camada de repositório para interagir com a tabela adotante
class AdotanteRepository: 
    # Inicializa o repositório com uma sessão de banco de dados
    def __init__(self, db: Session = Depends(get_db)): 
        self.db = db

    # Busca todos os adotantes
    def get_all(self) -> List[adotante_model.Adotante]:
        return self.db.query(adotante_model.Adotante).all()

    # Busca um único adotante por ID
    def get_by_id(self, adotante_id: int) -> Optional[adotante_model.Adotante]:
        return self.db.query(adotante_model.Adotante).get(adotante_id)
    
    # Busca um único adotante por email
    def get_by_email(self, email: str) -> Optional[adotante_model.Adotante]:
        return self.db.query(adotante_model.Adotante).filter(adotante_model.Adotante.email == email).first()

    # Cria um novo adotante no banco de dados
    def create(self, payload: adotante_schema.AdotanteCreate) -> adotante_model.Adotante:
        adotante = adotante_model.Adotante(**payload.model_dump()) 
        self.db.add(adotante) 
        self.db.commit()
        self.db.refresh(adotante)
        return adotante

    # Atualiza um adotante existente
    def update(self, adotante: adotante_model.Adotante, payload: adotante_schema.AdotanteUpdate) -> adotante_model.Adotante:
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(adotante, k, v)
        self.db.commit()
        self.db.refresh(adotante)
        return adotante

    # Deleta um adotante existente
    def delete(self, adotante: adotante_model.Adotante) -> None:
        self.db.delete(adotante)
        self.db.commit()
        return