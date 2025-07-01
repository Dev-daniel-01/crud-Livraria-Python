from sqlalchemy import Column, Integer, String
from database import Base

class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    ano_publicacao = Column(Integer, nullable=False)
    editora = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
