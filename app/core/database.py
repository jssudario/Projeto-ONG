from sqlalchemy import create_engine # ponte entre python e o db (sqlite)
from sqlalchemy.orm import sessionmaker, declarative_base # sessões temporárias, define classes que vriam tabelas no db

# caminho do db
SQLALCHEMY_DATABASE_URL = "sqlite:///./patinhas.db"

# motor
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  
)

# fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # commit e mudanças no meu controle
Base = declarative_base() # clase base de qual todos os modelos irão herdar

# fast api
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
