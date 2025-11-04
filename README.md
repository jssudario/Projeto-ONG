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
- SQLAdmin (Painel de Admin)
- Argon2 / Passlib (Criptografia de senha)
- JOSE / JWT (Tokens de autenticação)

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

## Como Criar o Primeiro Usuário (Setup Inicial)

Para o primeiro acesso, você precisa criar um superusuário. Como o painel já vem "trancado" por padrão no código, seguimos este processo:

---

### 1. Gere a Senha (Hash)

Com o `venv` ativado, rode este comando no terminal para gerar um hash para sua senha (ex: `admin123`):

```bash
python -c "from app.security import get_password_hash; print(get_password_hash('admin123'))"
````

---

### 2. Copie o Hash

Copie o hash gigante que aparecer no terminal (exemplo: `$argon2id$...`).

---

### 3. "Destranque" o Admin Temporariamente

Abra o arquivo `app/main.py`.

Encontre a linha que "tranca" o admin (ela deve estar por volta da linha 70):

```python
admin = Admin(app, engine, authentication_backend=authentication_backend)
```

Comente essa linha (coloque um `#` na frente) e, logo abaixo, adicione a versão "destrancada":

```python
# admin = Admin(app, engine, authentication_backend=authentication_backend)
admin = Admin(app, engine)
```

Salve o arquivo. O `uvicorn` irá recarregar.

---

### 4. Crie o Usuário no Painel Aberto

Agora, acesse o painel (que estará desprotegido):
[http://localhost:8000/admin](http://localhost:8000/admin)

Clique na aba **"Usuários"** e depois em **"Criar"**.

Preencha os campos:

* **username:** `admin`
* **hashed_password:** *(Cole o hash que você copiou no Passo 2)*

Clique em **Salvar**.

---

### 5. "Tranque" o Admin Novamente

Volte ao arquivo `app/main.py`.

Desfaça a mudança: apague a linha `admin = Admin(app, engine)` e tire o `#` da linha de segurança:

```python
admin = Admin(app, engine, authentication_backend=authentication_backend)
# admin = Admin(app, engine)
```

Salve o arquivo. O servidor irá recarregar.

---

Agora o painel está trancado permanentemente e você pode logar em
[http://localhost:8000/admin](http://localhost:8000/admin)
com o usuário **admin** e a senha **admin123**.

```
