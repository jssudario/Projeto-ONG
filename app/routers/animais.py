from fastapi import APIRouter, Depends, HTTPException, status # type: ignore
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas import animal as animal_schema
from app.models import animal as animal_model

router = APIRouter(prefix="/animais", tags=["animais"])

# get, busca animais do banco
@router.get("/", response_model=List[animal_schema.AnimalOut])
def list_animais(status_filter: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(animal_model.Animal)
    if status_filter:
        query = query.filter(animal_model.Animal.status == status_filter)
    return query.all()

# get, buscar pelo id
@router.get("/{animal_id}", response_model=animal_schema.AnimalOut)
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(animal_model.Animal).get(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Oops! Animal não encontrado. 🐾")
    return animal

# post, criar registro
# VERSÃO CORRIGIDA
@router.post("/", response_model=animal_schema.AnimalOut, status_code=status.HTTP_201_CREATED)
def create_animal(payload: animal_schema.AnimalCreate, db: Session = Depends(get_db)): 
    animal = animal_model.Animal(**payload.model_dump()) 
    db.add(animal) 
    db.commit() # salva no db
    db.refresh(animal) # recarrega pra pegar o id gerado
    return animal

# put, atualizar 
@router.put("/{animal_id}", response_model=animal_schema.AnimalOut)
def update_animal(animal_id: int, payload: animal_schema.AnimalUpdate, db: Session = Depends(get_db)):
    animal = db.query(animal_model.Animal).get(animal_id) 
    if not animal:
        raise HTTPException(status_code=404, detail="Oops! Animal não encontrado. 🐾")
    for k, v in payload.model_dump(exclude_unset=True).items(): # atualiza só campos enviados > exclude_unset=True
        setattr(animal, k, v)
    db.commit()
    db.refresh(animal)
    return animal

# delete
@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(animal_model.Animal).get(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Oops! Animal não encontrado. 🐾")
    db.delete(animal)
    db.commit()
    return