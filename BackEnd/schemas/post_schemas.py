from pydantic import BaseModel

class PostCreate(BaseModel):
    conteudo: str

class PostOut(BaseModel):
    id: int
    conteudo: str
    dono_id: int

    model_config = {
        "from_attributes": True
    }