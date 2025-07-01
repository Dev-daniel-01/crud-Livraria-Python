from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Livro as ModelLivro
from schemas import Livro, LivroCreate, LivroUpdate

livros_router = APIRouter()

@livros_router.get("/livros", response_model=List[Livro])
def listar_livros(db: Session = Depends(get_db)):
    livros = db.query(ModelLivro).all()
    return livros

@livros_router.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(ModelLivro).filter(ModelLivro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

@livros_router.post("/livros", response_model=Livro, status_code=status.HTTP_201_CREATED)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    # Verificar se ISBN já existe
    livro_existente = db.query(ModelLivro).filter(ModelLivro.isbn == livro.isbn).first()
    if livro_existente:
        raise HTTPException(status_code=400, detail="ISBN já cadastrado")
    novo_livro = ModelLivro(**livro.dict())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro

@livros_router.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro: LivroUpdate, db: Session = Depends(get_db)):
    livro_db = db.query(ModelLivro).filter(ModelLivro.id == livro_id).first()
    if not livro_db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    # Se for atualizar o ISBN, verificar duplicidade
    if livro.isbn != livro_db.isbn:
        livro_existente = db.query(ModelLivro).filter(ModelLivro.isbn == livro.isbn).first()
        if livro_existente:
            raise HTTPException(status_code=400, detail="ISBN já cadastrado para outro livro")

    for key, value in livro.dict(exclude_unset=True).items():
        setattr(livro_db, key, value)

    db.commit()
    db.refresh(livro_db)
    return livro_db

@livros_router.delete("/livros/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(ModelLivro).filter(ModelLivro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(livro)
    db.commit()
