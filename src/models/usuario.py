from sqlmodel import SQLModel, Field
from typing import Optional


# Modelo da tabela (SQLModel)
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    idade: int = Field(default=18)
    ativo: bool = Field(default=True)