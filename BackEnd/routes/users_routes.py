from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.user_models import User
from utils.auth import verificar_senha, criar_token, gerar_hash, verificar_token
from schemas.user_schemas import UserCreate
import secrets
import string



router = APIRouter()

#  ROTA DE CADASTRO DE USUÁRIO

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    user_existente = db.query(User).filter(User.email == user.email).first()
    if user_existente:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    novo_user = User(
        username=user.username,
        email=user.email,
        hashed_password=gerar_hash(user.password)
    )
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)

    token = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

    return {
        "mensagem": "Usuário criado com sucesso",
        "token": token,
        "email": novo_user.email
    }

#  ROTA DE LOGIN
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verificar_senha(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    token = criar_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def perfil_usuario(email: str = Depends(verificar_token)):
    return {"mensagem": f"Seja bem-vindo, {email}!"}


# FUNÇÃO DE PONTUAÇÃO DOS USUÁRIOS ATIVOS

@router.post("/pontuar")
def pontuar_usuario(db: Session = Depends(get_db), email: str = Depends(verificar_token)):
    usuario = db.query(User).filter(User.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    usuario.pontuacao += 10  # exemplo: +10 pontos por interação
    db.commit()
    db.refresh(usuario)

    return {"mensagem": "Pontuação atualizada", "pontuacao": usuario.pontuacao}

@router.get("/ranking")
def ranking_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(User).order_by(User.pontuacao.desc()).limit(10).all()

    ranking = [
        {
            "username": user.username,
            "email": user.email,
            "pontuacao": user.pontuacao
        }
        for user in usuarios
    ]

    return {"ranking": ranking}
