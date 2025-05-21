from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user_models import User, Post, Like
from schemas.like_schemas import LikeCreate
from utils.auth import verificar_token

router = APIRouter()

@router.post("/like")
def curtir_post(dados: LikeCreate, db: Session = Depends(get_db), email: str = Depends(verificar_token)):
    user = db.query(User).filter(User.email == email).first()
    post = db.query(Post).filter(Post.id == dados.post_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")

    like_existente = db.query(Like).filter(Like.user_id == user.id, Like.post_id == dados.post_id).first()
    if like_existente:
        raise HTTPException(status_code=400, detail="Você já curtiu esse post")

    novo_like = Like(user_id=user.id, post_id=dados.post_id)
    db.add(novo_like)
    db.commit()
    return {"mensagem": "Post curtido com sucesso!"}
