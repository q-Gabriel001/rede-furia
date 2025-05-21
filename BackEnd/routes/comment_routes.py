from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user_models import User, Comment, Post
from database import get_db
from utils.auth import verificar_token
from schemas.comment_schemas import CommentCreate, CommentOut

router = APIRouter()

@router.post("/comments", response_model=CommentOut)
def criar_comentario(comment: CommentCreate, db: Session = Depends(get_db), email: str = Depends(verificar_token)):
    user = db.query(User).filter(User.email == email).first()
    post = db.query(Post).filter(Post.id == comment.post_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not post:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")

    novo_comentario = Comment(conteudo=comment.conteudo, dono_id=user.id, post_id=post.id)
    db.add(novo_comentario)
    db.commit()
    db.refresh(novo_comentario)

    return novo_comentario

@router.get("/comments/{post_id}", response_model=list[CommentOut])
def listar_comentarios(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.id.desc()).all()
