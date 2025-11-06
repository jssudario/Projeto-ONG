from sqlalchemy import Column, Integer, String
from app.core.base import Base # Importa a Base declarativa

# Herda da classe Base para ser mapeado pelo SQLAlchemy
# Os usuários que podem logar no painel /admin.
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False) # Senha criptografada (hash)
