from passlib.context import CryptContext

# criptografia - argon2  
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# funcao verifica se uma senha normal bate com a senha criptografada
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida bate com o hash no banco."""
    return pwd_context.verify(plain_password, hashed_password)


# funcao gera a senha criptografada -> hash
def get_password_hash(password: str) -> str:
    """Cria um hash a partir de uma senha de texto puro."""
    return pwd_context.hash(password)