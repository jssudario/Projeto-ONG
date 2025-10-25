from fastapi import FastAPI # type: ignore
from app.database import engine, Base
from app.routers import animals
from fastapi.middleware.cors import CORSMiddleware # type: ignore # permite que o front acesse a api

# criar as tabelas no sqlite com base no models
Base.metadata.create_all(bind=engine)

# instancia do app, inicia o server
app = FastAPI(title="Patinhas API")

# ativa o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # qlqr origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# registra rota > animals
app.include_router(animals.router)

# teste api
@app.get("/")
def root():
    return {"ok": True, "message": "API funcionando"}