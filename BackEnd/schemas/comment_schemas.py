from pydantic import BaseModel

class CommentCreate(BaseModel):
    conteudo: str
    post_id: int

class CommentOut(BaseModel):
    id: int
    conteudo: str
    dono_id: int
    post_id: int

    model_config = {
        "from_attributes": True
    }