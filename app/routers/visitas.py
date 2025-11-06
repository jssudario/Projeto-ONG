from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.schemas import visita as visita_schema
from app.repositories.visita_repository import VisitaRepository
from app.repositories.solicitacao_repository import SolicitacaoRepository # Para validar a FK

router = APIRouter(prefix="/visitas", tags=["visitas"])

# Lista todas as visitas, com filtro opcional por retorno
@router.get("/", response_model=List[visita_schema.VisitaOut])
def list_visitas(
    retorno_filter: Optional[str] = None, 
    repo: VisitaRepository = Depends()
): 
    return repo.get_all(retorno_filter)

# Busca uma visita pelo ID
@router.get("/{visita_id}", response_model=visita_schema.VisitaOut)
def get_visita(
    visita_id: int, 
    repo: VisitaRepository = Depends()
):
    visita = repo.get_by_id(visita_id)
    if not visita:
        raise HTTPException(status_code=404, detail="Oops! Visita não encontrada. 🐾") 
    return visita

# Cria uma nova visita, validando se a solicitação-mãe existe
@router.post("/", response_model=visita_schema.VisitaOut, status_code=status.HTTP_201_CREATED) 
def create_visita(
    payload: visita_schema.VisitaCreate, 
    repo: VisitaRepository = Depends(),
    solicitacao_repo: SolicitacaoRepository = Depends() # Injeta o repo de solicitação
):
    # Verifica se a solicitação-mãe existe
    solicitacao = solicitacao_repo.get_by_id(payload.solicitacao_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
    # Se existir, cria visita
    return repo.create(payload)

# Atualiza uma visita existente
@router.put("/{visita_id}", response_model=visita_schema.VisitaOut)
def update_visita(
    visita_id: int, 
    payload: visita_schema.VisitaUpdate, 
    repo: VisitaRepository = Depends()
):
    # O router primeiro verifica se a visita existe
    visita = repo.get_by_id(visita_id) 
    if not visita:
        raise HTTPException(status_code=404, detail="Oops! Visita não encontrada. 🐾")
    # Se existe manda o repositório atualizar
    return repo.update(visita=visita, payload=payload)

# Deleta uma visita
@router.delete("/{visita_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_visita(
    visita_id: int, 
    repo: VisitaRepository = Depends()
):
    # O router primeiro verifica se a visita existe
    visita = repo.get_by_id(visita_id)
    if not visita:
        raise HTTPException(status_code=404, detail="Oops! Visita não encontrada. 🐾")
    # Se existe manda o repositório deletar
    repo.delete(visita=visita)
    return