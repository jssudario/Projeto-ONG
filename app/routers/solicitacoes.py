from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional 
from app.core.database import get_db
from app.schemas import solicitacao as solicitacao_schema
from app.models import solicitacao as solicitacao_model
from app.models import animal as animal_model
from app.models import adotante as adotante_model

router = APIRouter(prefix="/solicitacoes", tags=["solicitacoes"])

# get, listar
@router.get("/", response_model=List[solicitacao_schema.SolicitacaoOut])
def list_solicitacoes(status_filter: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(solicitacao_model.Solicitacao)
    if status_filter:
        query = query.filter(solicitacao_model.Solicitacao.status == status_filter)
    
    return query.all()

# get, buscar id
@router.get("/{solicitacao_id}", response_model=solicitacao_schema.SolicitacaoOut)
def get_solicitacao(solicitacao_id: int, db: Session = Depends(get_db)):
    solicitacao = db.query(solicitacao_model.Solicitacao).get(solicitacao_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Oops! Solicitação não encontrada. 🐾")
    return solicitacao

# post, criar
@router.post("/", response_model=solicitacao_schema.SolicitacaoOut, status_code=status.HTTP_201_CREATED)
def create_solicitacao(payload: solicitacao_schema.SolicitacaoCreate, db: Session = Depends(get_db)):
    # validacao da FK
    # verificar se o animal existe
    animal = db.query(animal_model.Animal).get(payload.animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Oops! Animal não encontrado. 🐾")

    # verificar se o adotante existe
    adotante = db.query(adotante_model.Adotante).get(payload.adotante_id)
    if not adotante:
        raise HTTPException(status_code=404, detail="Oops! Adotante não encontrado. 🐾")

    solicitacao = solicitacao_model.Solicitacao(**payload.model_dump()) # se animal e adotante existe > cria solicitacao
    db.add(solicitacao) 
    db.commit() 
    db.refresh(solicitacao)
    return solicitacao

# put, atualiza
@router.put("/{solicitacao_id}", response_model=solicitacao_schema.SolicitacaoOut)
def update_solicitacao(solicitacao_id: int, payload: solicitacao_schema.SolicitacaoUpdate, db: Session = Depends(get_db)):
    solicitacao = db.query(solicitacao_model.Solicitacao).get(solicitacao_id) 
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Oops! Solicitação não encontrada. 🐾")
    
    # atualiza os campos que vieram no payload
    for k, v in payload.model_dump(exclude_unset=True).items(): 
        setattr(solicitacao, k, v)  
    db.commit()
    db.refresh(solicitacao)
    return solicitacao

# delete
@router.delete("/{solicitacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_solicitacao(solicitacao_id: int, db: Session = Depends(get_db)):
    solicitacao = db.query(solicitacao_model.Solicitacao).get(solicitacao_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Oops! Solicitação não encontrada. 🐾")
    db.delete(solicitacao)
    db.commit()
    return


# db.refresh(solicitacao) -> recarrega pra pegar o id gerado