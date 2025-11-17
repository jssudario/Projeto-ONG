from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin, ModelView
from wtforms.fields import SelectField
from markupsafe import Markup
from starlette.datastructures import UploadFile

from app.core.database import engine
from app.core.base import Base
from app.models.animal import Animal
from app.models.adotante import Adotante
from app.models.solicitacao import Solicitacao
from app.models.visita import Visita
from app.models.user import User
from app.routers import animais, adotantes, solicitacoes, visitas
from app.admin_auth import authentication_backend

# Criar as tabelas no sqlite com base no models
Base.metadata.create_all(bind=engine)

# Instancia do app, inicia o server
app = FastAPI(title="Patinhas API")

# Servir arquivos enviados
app.mount("/static/uploads", StaticFiles(directory="static/uploads"), name="static_uploads")

STATUS_LABELS = {
    "pendente": "Pendente",
    "em_avaliacao": "Em avaliação",
    "aprovado": "Aprovado",
    "reprovado": "Recusado",
    "cancelado": "Cancelado",
    "disponivel": "Disponível",
    "reservado": "Reservado",
    "adotado": "Adotado",
}

RETORNO_LABELS = {
    "pendente": "Pendente",
    "aprovado": "Aprovado",
    "reprovado": "Reprovado",
}

BOOL_LABELS = {
    True: "Sim",
    False: "Não",
}

ESPECIE_LABELS = {
    "cachorro": "Cachorro",
    "gato": "Gato",
}

ESPECIE_CHOICES = [
    ("cachorro", "Cachorro"),
    ("gato", "Gato"), 
]

SEXO_LABELS = {
    "macho": "Macho",
    "femea": "Fêmea",
}

PORTE_LABELS = {
    "pequeno": "Pequeno",
    "medio": "Médio",
    "grande": "Grande",
    "nao_se_aplica": "Não se aplica",
}

# Views do SQLAdmin
class AnimalAdmin(ModelView, model=Animal):
    name = "Animal"
    name_plural = "Animais"
    icon = "fa-solid fa-paw"

    column_list = [Animal.id, Animal.nome, Animal.especie, Animal.status, Animal.foto]

    # Thumbnail da foto na listagem + formatação de rótulos
    column_formatters = {
        # "foto": lambda m, a: Markup(f'<img src="/{m.foto}" style="height:48px;">') if m.foto else "",
        "foto": lambda m, a: Markup(f'<img src="/{m.foto}" style="height:48px;">') if m.foto else "",
        "castrado": lambda m, a: BOOL_LABELS.get(m.castrado, m.castrado),
        "vacinado": lambda m, a: BOOL_LABELS.get(m.vacinado, m.vacinado),
        "especie": lambda m, a: ESPECIE_LABELS.get(m.especie, m.especie),
        "status": lambda m, a: STATUS_LABELS.get(m.status, m.status),
        "porte": lambda m, a: PORTE_LABELS.get(m.porte, m.porte),
        "sexo": lambda m, a: SEXO_LABELS.get(m.sexo, m.sexo),
    }
    column_formatters_detail = column_formatters
    column_formatters_export = column_formatters

    form_columns = [
        Animal.nome, Animal.especie, Animal.raca, Animal.sexo,
        Animal.idade_meses, Animal.porte, Animal.castrado, Animal.vacinado,
        Animal.status, Animal.data_entrada, Animal.observacoes,
        Animal.foto,  # Campo de upload (FileType)
    ]

    column_labels = {
        Animal.id: "ID", Animal.solicitacoes: "Solicitações",
        Animal.nome: "Nome", Animal.especie: "Espécie", Animal.raca: "Raça",
        Animal.sexo: "Sexo", Animal.idade_meses: "Idade (em meses)",
        Animal.porte: "Porte", Animal.castrado: "Castrado?", Animal.vacinado: "Vacinado?",
        Animal.status: "Status", Animal.data_entrada: "Data de entrada",
        Animal.observacoes: "Observações", Animal.foto: "Foto",
    }

    form_overrides = {
        "especie": SelectField,
        "sexo": SelectField,
        "porte": SelectField,
        "castrado": SelectField,
        "vacinado": SelectField,
        "status": SelectField,
    }

    form_args = {
        "especie": {"choices": [("cachorro", "Cachorro"), ("gato", "Gato")]},
        "sexo": {"choices": [("macho", "Macho"), ("femea", "Fêmea")]},
        "porte": {
            "choices": [
                ("pequeno", "Pequeno"),
                ("medio", "Médio"),
                ("grande", "Grande"),
                ("nao_se_aplica", "Não se aplica (Gato)"),
            ]
        },
        # Booleans como SelectField
        "castrado": {"choices": [(False, "Não"), (True, "Sim")], "coerce": bool},
        "vacinado": {"choices": [(False, "Não"), (True, "Sim")], "coerce": bool},
        "status": {
            "choices": [
                ("disponivel", "Disponível"),
                ("reservado", "Reservado"),
                ("adotado", "Adotado"),
            ],
            "default": "disponivel",
        },
    }

class AdotanteAdmin(ModelView, model=Adotante):
    column_list = [Adotante.id, Adotante.nome_completo, Adotante.email, Adotante.telefone]

    column_labels = {
        Adotante.id: "ID",
        Adotante.solicitacoes: "Solicitações",
        Adotante.nome_completo: "Nome completo",
        Adotante.email: "E-mail",
        Adotante.telefone: "Telefone",
        Adotante.cpf: "CPF",
        Adotante.data_nascimento: "Data de nascimento",
        Adotante.endereco: "Endereço",
    }

    icon = "fa-solid fa-user"
    name = "Adotante"
    name_plural = "Adotantes"


class SolicitacaoAdmin(ModelView, model=Solicitacao):
    icon = "fa-solid fa-file-lines"
    name = "Solicitação"
    name_plural = "Solicitações"

    column_list = [
        Solicitacao.id,
        "animal.nome",  # Mostra nome do animal
        "adotante.nome_completo",  # Mostra nome do adotante
        Solicitacao.status,
        Solicitacao.data_solicitacao,
    ]

    column_labels = {
        "animal.nome": "Animal",
        "adotante.nome_completo": "Adotante",
        Solicitacao.animal: "Animal",
        Solicitacao.adotante: "Adotante",
        Solicitacao.visitas: "Visitas",
        Solicitacao.id: "ID",
        Solicitacao.data_solicitacao: "Data",
        Solicitacao.status: "Status",
        Solicitacao.motivo_recusa: "Motivo da recusa",
        Solicitacao.animal_id: "Animal ID",
        Solicitacao.adotante_id: "Adotante ID",
    }

    # Usa relacionamento direto no formulário
    form_columns = [
        Solicitacao.animal,
        Solicitacao.adotante,
        Solicitacao.data_solicitacao,
        Solicitacao.status,
        Solicitacao.motivo_recusa,
    ]

    form_overrides = {"status": SelectField}
    form_args = {
        "status": {
            "choices": [
                ("pendente", "Pendente"),
                ("em_avaliacao", "Em Avaliação"),
                ("aprovado", "Aprovado"),
                ("reprovado", "Recusado"),
                ("cancelado", "Cancelado"),
            ],
            "default": "pendente",
        }
    }

    # Pesquisa assíncrona nos relacionamentos por nome
    form_ajax_refs = {
        "animal": {"fields": ("nome",)},
        "adotante": {"fields": ("nome_completo",)},
    }

    column_formatters = {
        "status": lambda m, a: STATUS_LABELS.get(m.status, m.status),
    }
    column_formatters_detail = column_formatters
    column_formatters_export = column_formatters


class VisitaAdmin(ModelView, model=Visita):
    icon = "fa-solid fa-calendar-check"
    name = "Visita"
    name_plural = "Visitas"

    column_list = [
        Visita.id,
        "solicitacao.id",
        Visita.data_hora,
        Visita.retorno,
    ]

    column_labels = {
        "solicitacao.id": "Solicitação",
        Visita.id: "ID",
        Visita.data_hora: "Data/Hora",
        Visita.retorno: "Resultado",
        Visita.observacoes: "Observações",
        Visita.solicitacao: "Solicitação",
        Visita.solicitacao_id: "Solicitação ID"
    }

    form_columns = [Visita.solicitacao, Visita.data_hora, Visita.retorno, Visita.observacoes]

    form_overrides = {"retorno": SelectField}
    form_args = {
        "retorno": {
            "choices": [
                ("pendente", "Pendente"),
                ("aprovado", "Aprovado"),
                ("reprovado", "Reprovado"),
            ],
            "default": "pendente",
        }
    }

    form_ajax_refs = {
        "solicitacao": {"fields": ("id",)},
    }

    column_formatters = {
        "retorno": lambda m, a: RETORNO_LABELS.get(m.retorno, m.retorno),
    }
    column_formatters_detail = column_formatters
    column_formatters_export = column_formatters


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]
    icon = "fa-solid fa-user-shield"
    name = "Usuário"
    name_plural = "Usuários"


# Painel admin - LOGIN
# admin = Admin(app, engine, authentication_backend=authentication_backend)
admin = Admin(app, engine)

admin.add_view(AnimalAdmin)
admin.add_view(AdotanteAdmin)
admin.add_view(SolicitacaoAdmin)
admin.add_view(VisitaAdmin)
admin.add_view(UserAdmin)

# Middlewares e rotas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(animais.router)
app.include_router(adotantes.router)
app.include_router(solicitacoes.router)
app.include_router(visitas.router)

# Teste API
@app.get("/")
def root():
    return {"ok": True, "message": "API funcionando"}
