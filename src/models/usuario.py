from sqlmodel import SQLModel, Field
from typing import Optional

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="ID do usuário")
    nome: str = Field(index=True, description="Nome do usuário")
    email: str = Field(index=True, unique=True, description="E-mail do usuário")
    idade: int = Field(default=18, description="Idade do usuário")
    ativo: int = Field(default=1, description="Status de atividade do usuário")
