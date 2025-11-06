from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List, Optional
from app.core.database import get_db
from app.models import visita as visita_model
from app.schemas import visita as visita_schema

# Camada de repositório para interagir com a tabela visita
class VisitaRepository:
    # Inicializa o repositório com uma sessão de banco de dados
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    # Busca todas as visitas, com filtro opcional por retorno
    def get_all(self, retorno_filter: Optional[str] = None) -> List[visita_model.Visita]:
        query = self.db.query(visita_model.Visita)
        if retorno_filter:
            query = query.filter(visita_model.Visita.retorno == retorno_filter) 
        return query.all()

    # Busca uma única visita pelo ID
    def get_by_id(self, visita_id: int) -> Optional[visita_model.Visita]:
        return self.db.query(visita_model.Visita).get(visita_id)

    # Cria uma nova visita no banco de dados
    # Assume que a validação de solicitacao_id já foi feita
    def create(self, payload: visita_schema.VisitaCreate) -> visita_model.Visita:
        visita = visita_model.Visita(**payload.model_dump()) 
        self.db.add(visita) 
        self.db.commit()
        self.db.refresh(visita)
        return visita

    # Atualiza uma visita existente
    def update(self, visita: visita_model.Visita, payload: visita_schema.VisitaUpdate) -> visita_model.Visita:
        for k, v in payload.model_dump(exclude_unset=True).items(): 
            setattr(visita, k, v)  
        self.db.commit()
        self.db.refresh(visita)
        return visita

    # Deleta uma visita
    def delete(self, visita: visita_model.Visita) -> None:
        self.db.delete(visita)
        self.db.commit()
        return