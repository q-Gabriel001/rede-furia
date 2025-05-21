from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Chave do Token
SECRET_KEY = "Chave secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_normal, senha_hash):
    return pwd_context.verify(senha_normal, senha_hash)

def gerar_hash(senha):
    return pwd_context.hash(senha)

def criar_token(data: dict, expira_em_min=ACCESS_TOKEN_EXPIRE_MINUTES):
    dados = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=expira_em_min)
    dados.update({"exp": exp})
    token_jwt = jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
