from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List, Optional
from app.core.database import get_db 
from app.models import animal as animal_model
from app.schemas import animal as animal_schema

# Camada de repositório para interagir com a tabela animal
class AnimalRepository:
    # Inicializa o repositório com uma sessão de banco de dados
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
    
    # Busca todos os animais, com filtro opcional por status
    def get_all(self, status_filter: Optional[str] = None) -> List[animal_model.Animal]:
        query = self.db.query(animal_model.Animal)
        if status_filter:
            query = query.filter(animal_model.Animal.status == status_filter)
        return query.all()

    # Busca um único animal pelo ID
    def get_by_id(self, animal_id: int) -> Optional[animal_model.Animal]:
        return self.db.query(animal_model.Animal).get(animal_id)
 
    # Cria um novo animal no banco de dados
    def create(self, payload: animal_schema.AnimalCreate) -> animal_model.Animal:
        animal = animal_model.Animal(**payload.model_dump()) 
        self.db.add(animal) 
        self.db.commit()
        self.db.refresh(animal)
        return animal

    # Atualiza um animal existente
    def update(self, animal: animal_model.Animal, payload: animal_schema.AnimalUpdate) -> animal_model.Animal:
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(animal, k, v)
        self.db.commit()
        self.db.refresh(animal)
        return animal

    # Deleta um animal
    def delete(self, animal: animal_model.Animal) -> None:
        self.db.delete(animal)
        self.db.commit()
        return