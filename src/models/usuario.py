from sqlmodel import SQLModel, Field, AutoString
from typing import Optional


# Modelo da tabela (SQLModel)
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    email: str = Field(index=True, unique=True, sa_type=AutoString)
    idade: int = Field(default=18)
    ativo: bool = Field(default=True)