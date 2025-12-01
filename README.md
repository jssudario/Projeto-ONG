# Projeto ONG - Sistema de Gerenciamento de Adoção

Este repositório contém o código-fonte de um sistema web completo para gerenciamento de adoção de animais, desenvolvido para Organizações Não Governamentais (ONGs). A plataforma utiliza uma arquitetura desacoplada, com uma API RESTful robusta no backend e uma interface responsiva no frontend.

## Estrutura de Diretórios

Abaixo, a organização dos arquivos dentro do diretório do projeto:

```text
patinhas/                   # Raiz do Projeto
│
├── README.md               # Documentação
├── requirements.txt        # Dependências do Python
│
├── static/                 # Frontend (Arquivos Públicos)
│   ├── css/
│   ├── js/
│   ├── img/
│   └── uploads/            # Fotos dos Animais
│
└── app/                    # Backend (Código Fonte API)
    ├── admin_auth.py       # Configuração de Login do Admin
    ├── security.py         # Lógica de Senhas e Tokens (JWT)
    ├── main.py             # Arquivo Principal (Start)
    ├── core/               # Configurações de Banco
    ├── models/             # Tabelas do Banco
    ├── routers/            # Rotas da API
    └── services/           # Regras de Negócio
```

## Visão Geral do Projeto

O sistema é composto por:

1.  **Portal Público (Frontend)**: Interface web para visualização de animais e submissão de interesse em adoção.
2.  **Painel Administrativo (Backend)**: Área restrita para gestão (CRUD) de animais, adotantes e solicitações.
3.  **Documentação Interativa**: Interface Swagger automática para teste e visualização dos endpoints da API.

## Tecnologias Utilizadas

### Backend (API)

* **Python 3.11+**
* **FastAPI**: Framework de alta performance.
* **PostgreSQL**: Banco de dados relacional.
* **SQLAlchemy**: ORM para manipulação de dados.
* **SQLAdmin**: Interface administrativa integrada.
* **Segurança**: Autenticação via JWT (JSON Web Tokens) e Hashing Argon2.

### Frontend (Cliente)

* **HTML5 / CSS3**: Design responsivo com CSS Variables e Grid Layout.
* **JavaScript (ES6+)**: Consumo assíncrono da API (Fetch API).
* **Integração Externa**: API do IBGE para localização.

---

## Instalação e Configuração

### 1. Pré-requisitos

* Python 3.11+
* PostgreSQL instalado e rodando.
* Git.
* VS Code (recomendado para execução do frontend).

### 2. Clonar o Repositório

```bash
git clone git@github.com:jssudario/Projeto-ONG.git
cd Projeto-ONG
```

### 3. Configuração do Backend

```bash
# Crie e ative o ambiente virtual
python -m venv .venv
# Windows: .\.venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 4. Configuração do Banco de Dados

1.  Crie um banco de dados vazio chamado `patinhas` no seu PostgreSQL.
2.  Verifique a string de conexão em `app/core/database.py`:

    ```python
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:SUA_SENHA@localhost/patinhas"
    ```

    *(As tabelas serão criadas automaticamente na primeira execução).*

---

## Execução do Projeto

O projeto opera com o Backend e o Frontend rodando em portas distintas (Simulação de ambiente desacoplado).

### Passo 1: Iniciar a API (Backend)

No terminal, navegue até a pasta do código fonte e inicie o servidor:

```bash
# 1. Entre na pasta do pacote principal
cd patinhas

# 2. Inicie o servidor
uvicorn app.main:app --reload
````

*O servidor iniciará em `http://localhost:8000`*

### Passo 2: Iniciar o Site (Frontend)

Sirva a pasta `patinhas/static` utilizando um servidor local.

  * **Recomendado (VS Code):** Clique com o botão direito no arquivo `index.html` e selecione **"Open with Live Server"**.
  * *O site iniciará geralmente em `http://127.0.0.1:5500`.*

---

## Acesso e Documentação

  * **Portal Público:** `http://127.0.0.1:5500` (ou a porta do seu servidor local)
  * **Painel Administrativo:** `http://localhost:8000/admin`
  * **Documentação da API (Swagger):** `http://localhost:8000/docs`

---

## Configuração do Primeiro Acesso (Admin)

O painel administrativo é protegido. Para o primeiro acesso, insira um usuário administrador diretamente no banco de dados:

1.  Gere um hash de senha seguro no terminal:

    ```bash
    python -c "from app.security import get_password_hash; print(get_password_hash('admin123'))"
    ```

2.  Execute o SQL no seu banco de dados:

    ```sql
    INSERT INTO "user" (username, hashed_password) 
    VALUES ('admin', 'COLE_O_HASH_GERADO_AQUI');
    ```

3.  Faça login em `/admin` com as credenciais criadas.
