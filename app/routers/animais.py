from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.schemas import animal as animal_schema
from app.repositories.animal_repository import AnimalRepository 

router = APIRouter(prefix="/animais", tags=["animais"])

# Lista todos os animais, com um filtro opcional por status
@router.get("/", response_model=List[animal_schema.AnimalOut])
def list_animais(
    status_filter: Optional[str] = None, 
    repo: AnimalRepository = Depends()
):
    return repo.get_all(status_filter)

# Busca um animal específico pelo ID
@router.get("/{animal_id}", response_model=animal_schema.AnimalOut)
def get_animal(animal_id: int, repo: AnimalRepository = Depends()):
    animal = repo.get_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Oops! Animal não encontrado. 🐾")
    return animal

# Cria um novo animal
@router.post("/", response_model=animal_schema.AnimalOut, status_code=status.HTTP_201_CREATED)
def create_animal(
    payload: animal_schema.AnimalCreate, 
    repo: AnimalRepository = Depends()
): 
    return repo.create(payload)

# Atualiza um animal existente
@router.put("/{animal_id}", response_model=animal_schema.AnimalOut)
def update_animal(
    animal_id: int, 
    payload: animal_schema.AnimalUpdate, 
    repo: AnimalRepository = Depends()
):
    # O router primeiro verifica se o animal existe
    animal = repo.get_by_id(animal_id) 
    if not animal:
        raise HTTPException(status_code=404, detail="Oops! Animal não encontrado. 🐾")
    # Se existe manda o repositório atualizar
    return repo.update(animal=animal, payload=payload)

# Deleta um animal
@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal(animal_id: int, repo: AnimalRepository = Depends()):
    # O router primeiro verifica se o animal existe
    animal = repo.get_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Oops! Animal não encontrado. 🐾")
    # Se existe manda o repositório deletar
    repo.delete(animal=animal)
    return