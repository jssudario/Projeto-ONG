from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List, Optional
from app.core.database import get_db
from app.models import solicitacao as solicitacao_model
from app.schemas import solicitacao as solicitacao_schema

# Camada de repositório para interagir com a tabela solicitacao
class SolicitacaoRepository:
    # Inicializa o repositório com uma sessão de banco de dados
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    # Busca todas as solicitações, com filtro opcional por status
    def get_all(self, status_filter: Optional[str] = None) -> List[solicitacao_model.Solicitacao]: 
        query = self.db.query(solicitacao_model.Solicitacao)
        if status_filter:
            query = query.filter(solicitacao_model.Solicitacao.status == status_filter)
        return query.all()

    # Busca uma única solicitação pelo ID
    def get_by_id(self, solicitacao_id: int) -> Optional[solicitacao_model.Solicitacao]:
        return self.db.query(solicitacao_model.Solicitacao).get(solicitacao_id)

    # Cria uma nova solicitação no banco de dados
    # Aqui assume-se que a validação de animal_id e adotante_id já foi feita na camada router
    def create(self, payload: solicitacao_schema.SolicitacaoCreate) -> solicitacao_model.Solicitacao:
        solicitacao = solicitacao_model.Solicitacao(**payload.model_dump())
        self.db.add(solicitacao) 
        self.db.commit() 
        self.db.refresh(solicitacao)
        return solicitacao

    # Atualiza uma solicitação existente no banco de dados
    def update(self, solicitacao: solicitacao_model.Solicitacao, payload: solicitacao_schema.SolicitacaoUpdate) -> solicitacao_model.Solicitacao:
        for k, v in payload.model_dump(exclude_unset=True).items(): 
            setattr(solicitacao, k, v)  
        self.db.commit()
        self.db.refresh(solicitacao)
        return solicitacao

    # Deleta uma solicitação do banco de dados
    def delete(self, solicitacao: solicitacao_model.Solicitacao) -> None:
        self.db.delete(solicitacao)
        self.db.commit()
        return