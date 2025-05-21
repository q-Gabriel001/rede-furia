import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from models.user_models import Post
from database import get_db
from utils.auth import verificar_token

router = APIRouter()

MEDIA_PATH = "media"
os.makedirs(f"{MEDIA_PATH}/imagens", exist_ok=True)
os.makedirs(f"{MEDIA_PATH}/videos", exist_ok=True)

@router.post("/posts")
def criar_post(
    texto: str = Form(...),
    imagem: UploadFile = File(None),
    video: UploadFile = File(None),
    db: Session = Depends(get_db),
    email: str = Depends(verificar_token)
):
    imagem_path = None
    video_path = None

    if imagem:
        imagem_path = f"{MEDIA_PATH}/imagens/{imagem.filename}"
        with open(imagem_path, "wb") as buffer:
            shutil.copyfileobj(imagem.file, buffer)

    if video:
        video_path = f"{MEDIA_PATH}/videos/{video.filename}"
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

    novo_post = Post(
        texto=texto,
        imagem_url=imagem_path,
        video_url=video_path,
        autor_email=email
    )

    db.add(novo_post)
    db.commit()
    db.refresh(novo_post)

    return {
        "mensagem": "Post criado com sucesso",
        "post": {
            "id": novo_post.id,
            "texto": novo_post.texto,
            "imagem": imagem_path,
            "video": video_path,
            "autor": email
        }
    }

@router.get("/posts")
def listar_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.id.desc()).all()
    return [
        {
            "id": post.id,
            "texto": post.texto,
            "imagem_url": post.imagem_url,
            "video_url": post.video_url,
            "autor": post.autor_email
        }
        for post in posts
    ]
