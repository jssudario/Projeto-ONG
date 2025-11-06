from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Token, JWT
SECRET_KEY = "e7eb07d53bd0cc4b541f5122d51f43a7a8e87ab70b85996bcafa5c7a19bfe181"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Verifica se a senha bate com o hash no banco
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Cria um hash a partir de uma senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Cria novo token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    
    # Adiciona o tempo de expiração
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Lê um token e vê se é válido
def decode_access_token(token: str) -> Optional[dict]:
    try:
        # Tenta decodificar o token
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_payload
    except jwt.JWTError:
        # Se o token for inválido ou expirado, retorna None
        return None