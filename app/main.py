from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin, ModelView
from wtforms.fields import SelectField
from markupsafe import Markup
from sqlalchemy.exc import IntegrityError

from app.core.database import engine
from app.core.base import Base
from app.models.animal import Animal
from app.models.adotante import Adotante
from app.models.solicitacao import Solicitacao
from app.models.visita import Visita
from app.models.user import User
from app.routers import animais, adotantes, solicitacoes, visitas
from app.admin_auth import authentication_backend

# Inicializa a estrutura do banco de dados criando tabelas para os modelos definidos
# A operação ignora tabelas já existentes
Base.metadata.create_all(bind=engine)

# Inicialização da instância principal do framework FastAPI
app = FastAPI(title="Patinhas API")


# Definição de exceção personalizada para erros de deleção no painel administrativo
class ErroDelecao(Exception):
    def __init__(self, message: str):
        self.message = message


# Manipulador de exceção global para capturar ErroDelecao
# Retorna uma resposta em texto plano (PlainTextResponse) com código HTTP 400 (Bad Request)
# Isso evita a renderização de HTML padrão do framework em alertas do frontend administrativo
@app.exception_handler(ErroDelecao)
async def delete_exception_handler(request: Request, exc: ErroDelecao):
    return PlainTextResponse(str(exc.message), status_code=400)


# Configuração de rota para servir arquivos estáticos (imagens de upload)
# Mapeia a URL "/static/uploads" para o diretório físico "static/uploads"
app.mount(
    "/static/uploads", 
    StaticFiles(directory="static/uploads"), 
    name="static_uploads"
)

# Mapeamento de status internos do banco de dados para rótulos legíveis na interface
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


# ===========================================
# Configuração das Views do SQLAdmin
# ===========================================

class AnimalAdmin(ModelView, model=Animal):
    """
    Configuração da interface administrativa para o modelo Animal
    Define colunas visíveis, formatação de dados e campos de formulário
    """
    name = "Animal"
    name_plural = "Animais"
    icon = "fa-solid fa-paw"

    async def delete_model(self, request, pk):
        """
        Sobrescreve o método de deleção padrão para implementar validação de integridade
        Captura exceções de integridade (Foreign Key) e levanta ErroDelecao com mensagem amigável
        """
        try:
            await super().delete_model(request, pk)
        except IntegrityError:
            raise ErroDelecao("Não é possível deletar! Este animal tem vínculos com solicitações.")

    column_list = [
        Animal.id,
        Animal.nome,
        Animal.especie,
        Animal.status,
        Animal.foto
    ]

    # Formatação condicional de colunas para exibição na listagem
    column_formatters = {
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
        Animal.foto,
    ]

    column_labels = {
        Animal.id: "ID",
        Animal.solicitacoes: "Solicitações",
        Animal.nome: "Nome",
        Animal.especie: "Espécie",
        Animal.raca: "Raça",
        Animal.sexo: "Sexo",
        Animal.idade_meses: "Idade (em meses)",
        Animal.porte: "Porte",
        Animal.castrado: "Castrado?",
        Animal.vacinado: "Vacinado?",
        Animal.status: "Status",
        Animal.data_entrada: "Data de entrada",
        Animal.observacoes: "Observações",
        Animal.foto: "Foto",
    }

    # Substituição de widgets padrão por SelectField para campos enumerados
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
    """
    Configuração da interface administrativa para o modelo Adotante
    """
    column_list = [
        Adotante.id,
        Adotante.nome_completo,
        Adotante.email,
        Adotante.telefone,
        Adotante.cidade,
        Adotante.estado
    ]

    column_labels = {
        Adotante.id: "ID",
        Adotante.solicitacoes: "Solicitações",
        Adotante.nome_completo: "Nome completo",
        Adotante.email: "E-mail",
        Adotante.telefone: "Telefone",
        Adotante.cpf: "CPF",
        Adotante.data_nascimento: "Data de nascimento",
        Adotante.estado: "Estado (UF)",
        Adotante.cidade: "Cidade",
        Adotante.rua: "Rua",
        Adotante.numero: "Número",
        Adotante.complemento: "Complemento"
    }

    icon = "fa-solid fa-user"
    name = "Adotante"
    name_plural = "Adotantes"


class SolicitacaoAdmin(ModelView, model=Solicitacao):
    """
    Configuração da interface administrativa para o modelo Solicitacao
    Inclui relacionamentos com Animal e Adotante na listagem
    """
    icon = "fa-solid fa-file-lines"
    name = "Solicitação"
    name_plural = "Solicitações"

    column_list = [
        Solicitacao.id,
        "animal.nome",
        "adotante.nome_completo",
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

    # Habilita busca assíncrona (AJAX) para campos de relacionamento
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
    """
    Configuração da interface administrativa para o modelo Visita
    """
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
    """
    Configuração da interface administrativa para o modelo User
    """
    column_list = [
        User.id,
        User.username
    ]
    icon = "fa-solid fa-user-shield"
    name = "Usuário"
    name_plural = "Usuários"


# ===========================================
# Inicialização do Painel Admin
# ===========================================

# Inicialização do painel administrativo sem autenticação (para fins de desenvolvimento/teste)
# Para habilitar segurança, utilize o parâmetro authentication_backend
admin = Admin(app, engine)
# admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(AnimalAdmin)
admin.add_view(AdotanteAdmin)
admin.add_view(SolicitacaoAdmin)
admin.add_view(VisitaAdmin)
admin.add_view(UserAdmin)


# ===========================================
# Middlewares e Rotas
# ===========================================

# Configuração de CORS (Cross-Origin Resource Sharing)
# Permite que aplicações web em domínios diferentes acessem a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro dos routers da aplicação.
app.include_router(animais.router)
app.include_router(adotantes.router)
app.include_router(solicitacoes.router)
app.include_router(visitas.router)


# Rota de verificação de saúde da API (Health Check)
@app.get("/")
def root():
    return {"ok": True, "message": "API funcionando"}