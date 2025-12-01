from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de Conexão do PostgreSQL
# Formato: postgresql://USUARIO:SENHA@ENDERECO/NOME_DO_BANCO
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/patinhas"

# Cria a engine (No Postgres não precisa do check_same_thread)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

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