# Projeto Patinhas (ONG)

Um sistema completo de gerenciamento e adoção de animais para ONGs, desenvolvido com um backend FastAPI (com painel de admin seguro) e um frontend em HTML/CSS/JavaScript.

## Sobre o Projeto

Este projeto cria uma plataforma web funcional para ONGs de proteção animal.

1. **Site Público (`/static`):** Uma vitrine para o público ver os animais disponíveis (lendo dinamicamente da API) e enviar formulários de adoção.
2. **Painel de Admin (`/admin`):** Uma área de gerenciamento interna, protegida por login, para a ONG cadastrar animais (CRUD), gerenciar usuários e aprovar solicitações.

## Tecnologias Utilizadas

### Backend
- Python 3.11+
- FastAPI (API)
- Uvicorn (Servidor)
- SQLAlchemy (ORM)
- **SQLAdmin** (Painel de Admin)
- **Argon2 / Passlib** (Criptografia de senha)
- **JOSE / JWT** (Tokens de autenticação)

### Frontend
- HTML5, CSS3 (Variáveis CSS, Grid)
- JavaScript (Fetch API)

## Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### 1. Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### 2. Clonar o Repositório

```bash
git clone git@github.com:jssudario/Projeto-ONG.git
cd Projeto-ONG
```

### 3. Configurar o Ambiente Backend

É altamente recomendado usar um ambiente virtual (venv).

```bash
# 1. Crie o ambiente virtual
python -m venv venv

# 2. Ative o ambiente
# No Linux/macOS:
source venv/bin/activate
# No Windows (Git Bash):
source venv/Scripts/activate

# 3. Instale todas as dependências
pip install -r requirements.txt
```

### 4. Executar o Projeto

Você precisará de dois terminais abertos: um para o backend e um para o frontend.

#### Terminal 1: Rodar o Backend (API + Admin)

```bash
uvicorn app.main:app --reload
```
O servidor da API será iniciado em [http://localhost:8000](http://localhost:8000).

#### Terminal 2: Ver o Frontend (Site Público)

Abra o projeto no VS Code.
Clique com o botão direito no arquivo `static/index.html`.
Selecione **"Open with Live Server"**.

---

## Como Criar seu Primeiro Usuário Admin

O painel `/admin` é protegido. Para o primeiro acesso, você precisa criar um usuário manualmente:

### 1. Gere a Senha (Hash)

```bash
python -c "from app.security import get_password_hash; print(get_password_hash('admin123'))"
```

### 2. Copie o Hash

Copie o hash que aparecer no terminal (exemplo: `$argon2id$...`).

### 3. Crie o Usuário

Com o servidor rodando, acesse [http://localhost:8000/admin](http://localhost:8000/admin).
Clique na aba **"Usuários"** → **"Criar"**.

Preencha os campos:

- `username`: admin
- `hashed_password`: (cole o hash que você copiou)

Clique em **Salvar**.

### 4. Ative a Segurança

No arquivo `app/main.py`, encontre esta linha:

```python
admin = Admin(app, engine)
```

Altere para:

```python
admin = Admin(app, engine, authentication_backend=authentication_backend)
```

Certifique-se de importar o backend corretamente:

```python
from app.admin_auth import authentication_backend
```

O servidor irá recarregar automaticamente.
Agora, o `/admin` exigirá login com **admin** e senha **admin123**.
