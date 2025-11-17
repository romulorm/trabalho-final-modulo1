from pydantic import BaseModel, Field, EmailStr

class Usuario(BaseModel):
    nome: str = Field(..., min_length=3, description="Nome do usuário")
    email: EmailStr = Field(..., description="E-mail do usuário")
    idade: int = Field(..., ge=18, le=100, description="Idade do usuário")
    ativo: bool = Field(default=True, description="Usuário ativo?")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Jane Doe",
                    "email": "jane.doe@example.com",
                    "idade": 35,
                    "ativo": True
                }
            ]
        }
    }