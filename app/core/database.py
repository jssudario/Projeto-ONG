from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define o endereço do database
SQLALCHEMY_DATABASE_URL = "sqlite:///./patinhas.db"

# Cria a engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  
)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Injeção de Dependência
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()