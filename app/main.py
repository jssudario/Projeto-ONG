from fastapi import FastAPI
from app.core.database import engine, Base
from app.routers import animais, adotantes, solicitacoes, visitas
import app.models
from fastapi.middleware.cors import CORSMiddleware # permite que o front acesse a api

# criar as tabelas no sqlite com base no models
Base.metadata.create_all(bind=engine)

# instancia do app, inicia o server
app = FastAPI(title="Patinhas API")

# ativa o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # qlqr origem
    allow_credentials=True,
    allow_methods=["*"], # todos os metodos
    allow_headers=["*"],
)

# registra rota
app.include_router(animais.router)
app.include_router(adotantes.router)
app.include_router(solicitacoes.router)
app.include_router(visitas.router)

# teste api
@app.get("/")
def root():
    return {"ok": True, "message": "API funcionando"}