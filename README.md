# Projeto Patinhas (ONG)

Um sistema completo de gerenciamento e adoção de animais para ONGs, desenvolvido com um backend FastAPI e um frontend em HTML/CSS/JavaScript.

## Sobre o Projeto

Este projeto tem como objetivo criar uma plataforma web funcional para ONGs de proteção animal.
Ele permite que a equipe administrativa gerencie os animais resgatados (CRUD) através de uma API e que o público geral veja os animais disponíveis para adoção através de um site amigável.

## Tecnologias Utilizadas

### Backend
- Python 3.11+
- FastAPI (para a API RESTful)
- Uvicorn (para servir a API)
- SQLAlchemy (para o ORM com o banco de dados)
- SQLite (banco de dados)

### Frontend
- HTML5  
- CSS3 (com Variáveis CSS)  
- JavaScript (a ser implementado)

## Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### 1. Pré-requisitos
- Python 3.11+
- Git

### 2. Clonar o Repositório
```bash
git clone git@github.com:jssudario/Projeto-ONG.git
cd Projeto-ONG
```

### 3. Configurar o Ambiente Backend

É altamente recomendado usar um ambiente virtual (venv).

```bash
# 1. Crie o ambiente virtual (na pasta raiz do projeto)
python -m venv venv

# 2. Ative o ambiente
# No Linux/macOS:
source venv/bin/activate
# No Windows (Git Bash):
source venv/Scripts/activate
# No Windows (CMD/PowerShell):
.\venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

### 4. Executar o Projeto

Você precisará de dois terminais abertos: um para o backend e um para o frontend.

#### Terminal 1: Rodar o Backend (API)

O servidor da API será iniciado em [http://localhost:8000](http://localhost:8000).

```bash
# A partir da pasta raiz, execute o uvicorn
uvicorn app.main:app --reload
```

Você pode acessar a documentação interativa da API em [http://localhost:8000/docs](http://localhost:8000/docs)

#### Terminal 2: Ver o Frontend (Site)

A forma mais fácil de visualizar o frontend é usando a extensão Live Server do VS Code.

1. Abra o projeto no VS Code.
2. Clique com o botão direito no arquivo `static/index.html`.
3. Selecione “Open with Live Server”.

Se preferir não usar a extensão, você pode simplesmente abrir o arquivo `static/index.html` diretamente no seu navegador.
