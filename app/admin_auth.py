from typing import Optional
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend
from app.core.database import SessionLocal
from app.models.user import User
from app.security import verify_password, create_access_token, decode_access_token, SECRET_KEY

# Implementa a lógica de autenticação customizada para o SQLAdmin
class AdminAuth(AuthenticationBackend):
    # Chamado quando o usuário tenta logar no /admin
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # Tenta achar o usuário no banco
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
        finally:
            db.close()

        # Se o usuário não existe, ou a senha está errada >
        if not user or not verify_password(password, user.hashed_password):
            return False # > Login falha

        # Se deu certo, pedimos ao security.py para criar o token
        token_data = {"sub": user.username} # sub = subject
        token = create_access_token(data=token_data)

        # Guarda o token nos cookies do navegador
        request.session.update({"token": token})

        return True

    # Chamado quando o usuário clica em logout
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    # Toda vez que o usuário tenta acessar uma página no /admin, é verificado se o token ainda é válido
    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        # security.py verifica o token
        payload = decode_access_token(token) 
        if not payload:
            return False # O token é inválido ou expirou
        
        return True

# Instancia o backend de autenticação
authentication_backend = AdminAuth(secret_key=SECRET_KEY)