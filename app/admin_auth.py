from jose import jwt
from typing import Optional
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend
from app.core.database import SessionLocal # sessão com o banco
from app.models.user import User
from app.security import verify_password, get_password_hash # funções de senha
from datetime import datetime, timedelta, timezone

# NUNCA UTILIZAR EM PROJETO REAL > use .env
SECRET_KEY = "e7eb07d53bd0cc4b541f5122d51f43a7a8e87ab70b85996bcafa5c7a19bfe181" # openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # login dura 30 minutos

def create_access_token(data: dict) -> str:
    """Cria um novo token de acesso."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # calcula o tempo de expiração
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Lê um token e vê se é válido."""
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_payload
    except jwt.JWTError:
        return None

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """
        Chamado quando o usuário tenta logar no /admin.
        """
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # tenta achar o usuário no banco
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()

        # se o usuário não existe, ou a senha está errada
        if not user or not verify_password(password, user.hashed_password):
            return False # login falha

        # se deu certo, criamos o token
        token_data = {"sub": user.username} # sub = subject > dono do token
        token = create_access_token(data=token_data)

        # guarda o token nos cookies do navegador
        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        """
        Chamado quando o usuário clica em "Logout".
        """
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """
        Chamado TODA VEZ que o usuário tenta acessar uma página do /admin.
        Verifica se o token ainda é válido.
        """
        token = request.session.get("token")

        if not token:
            return False # não tem token, não entra

        payload = decode_access_token(token) # tenta ler o token 
        if not payload:
            return False # o token é inválido ou expirou

        return True # ok, token válido

# instancia o backend de autenticação
authentication_backend = AdminAuth(secret_key=SECRET_KEY)