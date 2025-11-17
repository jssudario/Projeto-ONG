from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas import adotante as adotante_schema
from app.repositories.adotante_repository import AdotanteRepository
from datetime import date, timedelta

router = APIRouter(prefix="/adotantes", tags=["adotantes"])

# Lista todos os adotantes
@router.get("/", response_model=List[adotante_schema.AdotanteOut])
def list_adotante(repo: AdotanteRepository = Depends()):
    return repo.get_all()

# Busca um adotante específico pelo ID
@router.get("/{adotante_id}", response_model=adotante_schema.AdotanteOut)
def get_adotante(adotante_id: int, repo: AdotanteRepository = Depends()):
    adotante = repo.get_by_id(adotante_id)
    if not adotante:
        raise HTTPException(status_code=404, detail="Oops! Adotante não encontrado. 🐾")
    return adotante

# Cria um novo adotante
@router.post("/", response_model=adotante_schema.AdotanteOut, status_code=status.HTTP_201_CREATED)
def create_adotante(
    payload: adotante_schema.AdotanteCreate, 
    repo: AdotanteRepository = Depends()
): 
    # Pega a data de nascimento do payload (que veio do formulário)
    data_nascimento = payload.data_nascimento
    
    # Calcula a data exata de 18 anos atrás
    # (hoje - 18 anos)
    data_maioridade = date.today() - timedelta(days=18*365.25) 
    
    # Se a data de nascimento for DEPOIS da data de maioridade, a pessoa é menor.
    if data_nascimento > data_maioridade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Adoção não permitida. O adotante deve ser maior de 18 anos."
        )
    return repo.create(payload)

# Atualiza um adotante existente
@router.put("/{adotante_id}", response_model=adotante_schema.AdotanteOut)
def update_adotante(
    adotante_id: int, 
    payload: adotante_schema.AdotanteUpdate, 
    repo: AdotanteRepository = Depends()
):
    # O router verifica se o adotante existe
    adotante = repo.get_by_id(adotante_id) 
    if not adotante:
        raise HTTPException(status_code=404, detail="Oops! Adotante não encontrado. 🐾")
    # Se existe, o router manda o repositório atualizar
    return repo.update(adotante=adotante, payload=payload)

# Deleta um adotante
@router.delete("/{adotante_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_adotante(adotante_id: int, repo: AdotanteRepository = Depends()):
    # O router verifica se o adotante existe
    adotante = repo.get_by_id(adotante_id)
    if not adotante:
        raise HTTPException(status_code=404, detail="Oops! Adotante não encontrado. 🐾")
    # Se existe, o router manda o repositório deletar
    repo.delete(adotante=adotante)
    return