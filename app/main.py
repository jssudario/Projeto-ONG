import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin, ModelView

from app.core.database import engine, Base
from app.routers import animais, adotantes, solicitacoes, visitas

from app.models.animal import Animal
from app.models.adotante import Adotante
from app.models.solicitacao import Solicitacao
from app.models.visita import Visita
from app.models.user import User

from app.admin_auth import authentication_backend

# garante que a pasta de uploads exista
os.makedirs("static/uploads", exist_ok=True)

# criar as tabelas no sqlite com base no models
Base.metadata.create_all(bind=engine)

# instância do app, inicia o server
app = FastAPI(title="Patinhas API")

# ativa o CORS, middlewares e rotas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # qlqr origem 
    allow_credentials=True,
    allow_methods=["*"], # todos os metodos
    allow_headers=["*"],
)

# servir os arquivos enviados em /uploads
app.mount("/uploads", StaticFiles(directory="static/uploads"), name="uploads")

# configuracao do painel admin > utilizado sqladmin
class AnimalAdmin(ModelView, model=Animal):
    # Cclunas exibidas na lista
    column_list = [Animal.id, Animal.nome, Animal.especie, Animal.status]
    # campos exibidos no formulário de criação/edição
    form_columns = [
        Animal.nome,
        Animal.especie,
        Animal.raca,
        Animal.sexo,
        Animal.idade_meses,
        Animal.porte,
        Animal.castrado,
        Animal.vacinado,
        Animal.status,
        Animal.data_entrada,
        Animal.observacoes,
        Animal.foto_url,
    ]

    icon = "fa-solid fa-paw"
    name = "Animal"
    name_plural = "Animais"


class AdotanteAdmin(ModelView, model=Adotante):
    column_list = [Adotante.id, Adotante.nome_completo, Adotante.email, Adotante.telefone]
    icon = "fa-solid fa-user"
    name = "Adotante"
    name_plural = "Adotantes"


class VisitaAdmin(ModelView, model=Visita):
    column_list = [Visita.id, Visita.data_hora, Visita.retorno]
    icon = "fa-solid fa-calendar-check"
    name = "Visita"
    name_plural = "Visitas"


class SolicitacaoAdmin(ModelView, model=Solicitacao):
    column_list = [Solicitacao.id, Solicitacao.status, Solicitacao.data_solicitacao]
    icon = "fa-solid fa-file-lines"
    name = "Solicitação"
    name_plural = "Solicitações"


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]  # nunca exibe a  senha
    icon = "fa-solid fa-user-shield"
    name = "Usuário"
    name_plural = "Usuários"


# PLUG DO ADMIN
admin = Admin(app, engine, authentication_backend=authentication_backend) # com login
# admin = Admin(app, engine) # sem login

# registra as views
admin.add_view(AnimalAdmin)
admin.add_view(AdotanteAdmin)
admin.add_view(VisitaAdmin)
admin.add_view(SolicitacaoAdmin)
admin.add_view(UserAdmin)

# registra rota
app.include_router(animais.router)
app.include_router(adotantes.router)
app.include_router(solicitacoes.router)
app.include_router(visitas.router)

# healthcheck
@app.get("/")
def root():
    return {"ok": True, "message": "API funcionando"}