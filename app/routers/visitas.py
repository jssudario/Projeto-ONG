from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional 
from app.core.database import get_db
from app.schemas import visita as visita_schema
from app.models import visita as visita_model
from app.models import solicitacao as solicitacao_model

router = APIRouter(prefix="/visitas", tags=["visitas"])

# get, listar
@router.get("/", response_model=List[visita_schema.VisitaOut])
def list_visitas(retorno_filter: Optional[str] = None, db: Session = Depends(get_db)): 
    query = db.query(visita_model.Visita)
    if retorno_filter: # filtro retorno
        query = query.filter(visita_model.Visita.retorno == retorno_filter) 

    return query.all()

# get, buscar id
@router.get("/{visita_id}", response_model=visita_schema.VisitaOut)
def get_visita(visita_id: int, db: Session = Depends(get_db)):
    visita = db.query(visita_model.Visita).get(visita_id)
    if not visita:
        raise HTTPException(status_code=404, detail="Oops! Visita não encontrada. 🐾") 

# post, criar
@router.post("/", response_model=visita_schema.VisitaOut, status_code=status.HTTP_201_CREATED) 
def create_visita(payload: visita_schema.VisitaCreate, db: Session = Depends(get_db)):
    # verifica se a solicitação-mãe existe
    solicitacao = db.query(solicitacao_model.Solicitacao).get(payload.solicitacao_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

    # se existir, cria visita
    visita = visita_model.Visita(**payload.model_dump()) 
    db.add(visita) 
    db.commit()
    db.refresh(visita)
    return visita

# put, atualiza
@router.put("/{visita_id}", response_model=visita_schema.VisitaOut)
def update_visita(visita_id: int, payload: visita_schema.VisitaUpdate, db: Session = Depends(get_db)):
    visita = db.query(visita_model.Visita).get(visita_id) 
    if not visita:
        raise HTTPException(status_code=404, detail="Oops! Visita não encontrada. 🐾")
    
    # atualiza os campos que vieram no payload
    for k, v in payload.model_dump(exclude_unset=True).items(): 
        setattr(visita, k, v)  
    db.commit()
    db.refresh(visita)
    return visita

# delete
@router.delete("/{visita_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_visita(visita_id: int, db: Session = Depends(get_db)):
    visita = db.query(visita_model.Visita).get(visita_id)
    if not visita:
        raise HTTPException(status_code=404, detail="Oops! Visita não encontrada. 🐾")
    db.delete(visita)
    db.commit()
    return