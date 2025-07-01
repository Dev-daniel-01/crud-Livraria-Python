from pydantic import BaseModel

class LivroBase(BaseModel):
    titulo: str
    autor: str
    ano_publicacao: int
    editora: str
    isbn: str

class LivroCreate(LivroBase):
    pass

class LivroUpdate(LivroBase):
    pass

class Livro(LivroBase):
    id: int

    class Config:
        orm_mode = True
