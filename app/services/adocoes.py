from fastapi import Depends, HTTPException, status
from typing import List, Optional
from app.schemas import solicitacao as solicitacao_schema
from app.repositories.solicitacao_repository import SolicitacaoRepository # O serviço depende dos repositórios 
from app.repositories.animal_repository import AnimalRepository
from app.repositories.adotante_repository import AdotanteRepository

# Classe que ordena os repositórios e aplica regras de negócio
# antes de interagir com o banco de dados
class AdocaoService:
    # Inicializa o serviço injetando os repositórios necessários
    def __init__(
        self,
        repo: SolicitacaoRepository = Depends(),
        animal_repo: AnimalRepository = Depends(),
        adotante_repo: AdotanteRepository = Depends()
    ):
        self.repo = repo
        self.animal_repo = animal_repo
        self.adotante_repo = adotante_repo

    # Delega a busca de todas as solicitações para o repositório
    def get_all(self, status_filter: Optional[str] = None) -> List:
        return self.repo.get_all(status_filter)

    # Busca uma solicitação pelo ID > verifica a existência
    def get_by_id(self, solicitacao_id: int):
        solicitacao = self.repo.get_by_id(solicitacao_id)
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Oops! Solicitação não encontrada. 🐾")
        return solicitacao

    # Aplica a lógica de negócio para criar uma nova solicitação
    def create(self, payload: solicitacao_schema.SolicitacaoCreate): 
        # Verifica se o animal existe
        animal = self.animal_repo.get_by_id(payload.animal_id)
        if not animal:
            raise HTTPException(status_code=404, detail="Oops! Animal não encontrado. 🐾")

        # Verifica se o adotante existe
        adotante = self.adotante_repo.get_by_id(payload.adotante_id)
        if not adotante:
            raise HTTPException(status_code=404, detail="Oops! Adotante não encontrado. 🐾")
        return self.repo.create(payload)

    # Aplica a lógica de negócio para atualizar uma solicitação
    def update(self, solicitacao_id: int, payload: solicitacao_schema.SolicitacaoUpdate):
        # Verifica se a solicitação existe
        solicitacao = self.get_by_id(solicitacao_id) 
        
        # Manda o repositório atualizar
        return self.repo.update(solicitacao=solicitacao, payload=payload)

    # Aplica a lógica de negócio para deletar uma solicitação
    def delete(self, solicitacao_id: int):
        # Verifica se a solicitação existe
        solicitacao = self.get_by_id(solicitacao_id)
        # Manda o repositório deletar
        self.repo.delete(solicitacao=solicitacao)
        return