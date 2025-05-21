from fastapi import FastAPI
from database import engine
from models import user_models
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from routes import users_routes, post_routes, comment_routes, like_routes

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")

# Liberar CORS para acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INCLUINDO ROTAS
app.include_router(users_routes.router)
app.include_router(post_routes.router)
app.include_router(comment_routes.router)
app.include_router(like_routes.router)

# CONFIGURAÇÃO PERSONALIZADA DO SWAGGER (OPENAPI) COM JWT
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FURIA API",
        version="1.0.0",
        description="API da rede social da FURIA",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "/login" not in path and "/register" not in path:
                openapi_schema["paths"][path][method]["security"] = [{"OAuth2PasswordBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Ativa o schema customizado
app.openapi = custom_openapi

# Criação das tabelas no banco
user_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"mensagem": "API da FURIA está no ar!"}
