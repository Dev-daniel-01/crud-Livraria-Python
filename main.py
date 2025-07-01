from fastapi import FastAPI
from database import engine, Base
from routers.livros import livros_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API da Livraria",
    description="API para gerenciar livros da livraria com operações CRUD.",
    version="1.0.0",
)

app.include_router(livros_router, tags=["livros"])
