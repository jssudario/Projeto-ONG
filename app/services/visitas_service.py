from fastapi import Depends, HTTPException, status
from typing import List, Optional
from app.schemas import visita as visita_schema
from app.repositories.visita_repository import VisitaRepository
from app.repositories.solicitacao_repository import SolicitacaoRepository

class VisitaService:
    def __init__(
        self,
        repo: VisitaRepository = Depends(),
        solicitacao_repo: SolicitacaoRepository = Depends()
    ):
        # Injeta os repositórios de Visita e Solicitação
        self.repo = repo
        self.solicitacao_repo = solicitacao_repo

    # Delega a busca de todas as visitas para o repositório
    def get_all(self, retorno_filter: Optional[str] = None) -> List:
        return self.repo.get_all(retorno_filter)

    # Busca uma visita pelo ID
    def get_by_id(self, visita_id: int):
        visita = self.repo.get_by_id(visita_id)
        if not visita:
            raise HTTPException(status_code=404, detail="Oops! Visita não encontrada. 🐾")
        return visita

    # Aplica a lógica de negócio para criar uma nova visita
    def create(self, payload: visita_schema.VisitaCreate): 
        # Verifica se a solicitação-mãe existe
        solicitacao = self.solicitacao_repo.get_by_id(payload.solicitacao_id)
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
        # Se existir, cria visita 
        return self.repo.create(payload)

    # Aplica a lógica de negócio para atualizar uma visita
    def update(self, visita_id: int, payload: visita_schema.VisitaUpdate):
        # Verifica se a visita existe
        visita = self.get_by_id(visita_id)
        # Manda o repositório atualizar
        return self.repo.update(visita=visita, payload=payload)

    # Aplica a lógica de negócio para deletar uma visita
    def delete(self, visita_id: int):
        # Verifica se a visita existe
        visita = self.get_by_id(visita_id)
        # Manda o repositório deletar
        self.repo.delete(visita=visita)
        return