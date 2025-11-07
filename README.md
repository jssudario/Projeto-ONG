# Projeto ONG - Sistema de Gerenciamento de Adoção

Este repositório contém o código-fonte de um sistema web completo para gerenciamento de adoção de animais, desenvolvido para Organizações Não Governamentais (ONGs). A plataforma é composta por um backend robusto em FastAPI e um frontend para interação pública.

## Visão Geral do Projeto

O sistema é dividido em duas componentes principais:

1.  **Portal Público (Frontend)**: Uma interface web (`/static`) onde o público geral pode visualizar os animais disponíveis para adoção (consumindo dados da API) e submeter formulários de interesse.
2.  **Painel Administrativo (Backend)**: Uma área restrita (`/admin`), protegida por autenticação, onde a equipe da ONG pode realizar o gerenciamento completo (CRUD) de animais, administrar usuários e processar solicitações de adoção.

## Tecnologias Utilizadas

### Backend

  * **Python 3.11+**
  * **FastAPI**: Framework principal da API.
  * **SQLAlchemy**: ORM para interação com o banco de dados.
  * **SQLAdmin**: Interface para o painel administrativo.
  * **Uvicorn**: Servidor ASGI.
  * **Segurança**:
      * `Argon2` / `Passlib`: Hashing de senhas.
      * `JOSE` / `JWT`: Tokens de autenticação.

### Frontend

  * **HTML5**
  * **CSS3** (Variáveis CSS, Grid Layout)
  * **JavaScript (ES6+)**: Consumo da API via `Fetch`.

## Instalação e Execução Local

Siga os passos abaixo para configurar e executar o projeto em um ambiente de desenvolvimento.

### 1\. Pré-requisitos

  * Python 3.11 ou superior
  * Git

### 2\. Clonar o Repositório

```bash
git clone git@github.com:jssudario/Projeto-ONG.git
cd Projeto-ONG
```

### 3\. Configuração do Ambiente Virtual (Backend)

Recomenda-se o uso de um ambiente virtual (`venv`) para isolar as dependências.

```bash
# 1. Crie o ambiente virtual
python -m venv venv

# 2. Ative o ambiente
# Linux/macOS
source venv/bin/activate
# Windows (Git Bash/PowerShell)
.\venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

### 4\. Execução

O projeto requer dois terminais para execução simultânea do backend e do frontend.

#### Terminal 1: Backend (API e Admin)

```bash
# Inicia o servidor com hot-reload
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

#### Terminal 2: Frontend (Portal Público)

Para visualizar o frontend, utilize um servidor local. Se você usa o VS Code, pode usar a extensão "Live Server":

1.  Abra a pasta do projeto no VS Code.
2.  Clique com o botão direito no arquivo `static/index.html`.
3.  Selecione "Open with Live Server".

-----

## Configuração Inicial do Superusuário

Por padrão, o painel administrativo é iniciado com a autenticação ativada. Siga este procedimento para criar o primeiro usuário administrador:

### 1\. Gerar Hash de Senha

Com o `venv` ativado, execute o comando abaixo para gerar um hash Argon2 para sua senha (ex: `admin123`).

```bash
python -c "from app.security import get_password_hash; print(get_password_hash('admin123'))"
```

Copie o hash gerado (ex: `$argon2id$...`).

### 2\. Desabilitar Autenticação Temporariamente

1.  Edite o arquivo `app/main.py`.
2.  Localize a linha de inicialização do `Admin` (próximo à linha 70):
    ```python
    admin = Admin(app, engine, authentication_backend=authentication_backend)
    ```
3.  Comente a linha acima e adicione a inicialização sem autenticação logo abaixo:
    ```python
    # admin = Admin(app, engine, authentication_backend=authentication_backend)
    admin = Admin(app, engine)
    ```
4.  Salve o arquivo. O servidor `uvicorn` reiniciará automaticamente.

### 3\. Criar Usuário Administrador

1.  Acesse o painel administrativo, agora desprotegido: `http://localhost:8000/admin`.
2.  Navegue até a seção "Usuários" e clique em "Criar".
3.  Preencha os campos:
      * **username**: `admin`
      * **hashed\_password**: (Cole o hash gerado no Passo 1)
4.  Clique em "Salvar".

### 4\. Reabilitar Autenticação

1.  Retorne ao arquivo `app/main.py`.
2.  Reverta a alteração: descomente a linha original e remova a linha temporária.
    ```python
    admin = Admin(app, engine, authentication_backend=authentication_backend)
    # admin = Admin(app, engine)
    ```
3.  Salve o arquivo. O servidor reiniciará.

A partir deste ponto, o painel administrativo em `http://localhost:8000/admin` está protegido e acessível com as credenciais criadas (ex: `admin` / `admin123`).
