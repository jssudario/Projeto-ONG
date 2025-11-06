from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.schemas import solicitacao as solicitacao_schema
from app.services.adocoes import AdocaoService

router = APIRouter(prefix="/solicitacoes", tags=["solicitacoes"])

# Lista todas as solicitações
@router.get("/", response_model=List[solicitacao_schema.SolicitacaoOut])
def list_solicitacoes(
    status_filter: Optional[str] = None, 
    service: AdocaoService = Depends()
):
    return service.get_all(status_filter)

# Busca uma solicitação pelo ID
@router.get("/{solicitacao_id}", response_model=solicitacao_schema.SolicitacaoOut)
def get_solicitacao(
    solicitacao_id: int, 
    service: AdocaoService = Depends()
):
    return service.get_by_id(solicitacao_id)

# Cria uma nova solicitação
@router.post("/", response_model=solicitacao_schema.SolicitacaoOut, status_code=status.HTTP_201_CREATED)
def create_solicitacao(
    payload: solicitacao_schema.SolicitacaoCreate, 
    service: AdocaoService = Depends()
): 
    return service.create(payload)

# Atualiza uma solicitação existente
@router.put("/{solicitacao_id}", response_model=solicitacao_schema.SolicitacaoOut)
def update_solicitacao(
    solicitacao_id: int, 
    payload: solicitacao_schema.SolicitacaoUpdate, 
    service: AdocaoService = Depends()
):
    return service.update(solicitacao_id, payload)

# Deleta uma solicitação
@router.delete("/{solicitacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_solicitacao(
    solicitacao_id: int, 
    service: AdocaoService = Depends()
):
    service.delete(solicitacao_id)
    return