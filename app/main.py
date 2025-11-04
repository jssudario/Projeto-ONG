from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView

from app.core.database import engine, Base
from app.routers import animais, adotantes, solicitacoes, visitas

from app.models.animal import Animal
from app.models.adotante import Adotante
from app.models.solicitacao import Solicitacao
from app.models.visita import Visita
from app.models.user import User

from sqladmin import Admin, ModelView
from app.admin_auth import authentication_backend


# criar as tabelas no sqlite com base no models
Base.metadata.create_all(bind=engine)


# instancia do app, inicia o server
app = FastAPI(title="Patinhas API")

# configuracao do painel admin > utilizado sqladmin
class AnimalAdmin(ModelView, model=Animal):
    column_list = [Animal.id, Animal.nome, Animal.especie, Animal.status] 
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
    # Queremos ver o username, mas NUNCA a senha
    column_list = [User.id, User.username] 
    icon = "fa-solid fa-user-shield"
    name = "Usuário"
    name_plural = "Usuários"


# plug do admin
admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(AnimalAdmin)
admin.add_view(AdotanteAdmin)
admin.add_view(VisitaAdmin)
admin.add_view(SolicitacaoAdmin)
admin.add_view(UserAdmin)


# ativa o CORS, middlewares e rotas
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