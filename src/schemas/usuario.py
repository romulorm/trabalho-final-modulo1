from pydantic import BaseModel, EmailStr

# Modelo para validação de entrada (Pydantic puro)
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    idade: int = 18
    ativo: int = 1