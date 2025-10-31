from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import adotante as adotante_schema
from app.models import adotante as adotante_model

router = APIRouter(prefix="/adotantes", tags=["adotante"])

# get
@router.get("/", response_model=List[adotante_schema.AdotanteOut])
def list_adotante(db: Session = Depends(get_db)):
    query = db.query(adotante_model.Adotante)
    return query.all()


@router.get("/{adotante_id}", response_model=adotante_schema.AdotanteOut)
def get_adotante(adotante_id: int, db: Session = Depends(get_db)):
    adotante = db.query(adotante_model.Adotante).get(adotante_id)
    if not adotante:
        raise HTTPException(status_code=404, detail="Oops! Adotante não encontrado. 🐾")
    return adotante

# post, criar registro
@router.post("/", response_model=adotante_schema.AdotanteOut, status_code=status.HTTP_201_CREATED)
def create_adotante(payload: adotante_schema.AdotanteCreate, db: Session = Depends(get_db)): 
    adotante = adotante_model.Adotante(**payload.model_dump()) 
    db.add(adotante) 
    db.commit() # salva no db
    db.refresh(adotante) # recarrega pra pegar o id gerado
    return adotante

# put, atualizar 
@router.put("/{adotante_id}", response_model=adotante_schema.AdotanteOut)
def update_adotante(adotante_id: int, payload: adotante_schema.AdotanteUpdate, db: Session = Depends(get_db)):
    adotante = db.query(adotante_model.Adotante).get(adotante_id) 
    if not adotante:
        raise HTTPException(status_code=404, detail="Oops! Adotante não encontrado. 🐾")
    for k, v in payload.model_dump(exclude_unset=True).items(): # atualiza só campos enviados > exclude_unset=True
        setattr(adotante, k, v)
    db.commit()
    db.refresh(adotante)
    return adotante

# delete
@router.delete("/{adotante_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_adotante(adotante_id: int, db: Session = Depends(get_db)):
    adotante = db.query(adotante_model.Adotante).get(adotante_id)
    if not adotante:
        raise HTTPException(status_code=404, detail="Oops! Adotante não encontrado. 🐾")
    db.delete(adotante)
    db.commit()
    return