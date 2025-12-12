from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from src.models.usuario import Usuario
from sqlmodel import select, Session
from src.utils.database import engine

router = APIRouter()

# Rota de listar usuários
@router.get("/usuarios", summary="Listar usuários", description="Retorna todos os usuários cadastrados no banco de dados.",
      responses = {
          404: {"description": "Sem usuários cadastrados"}
} )
def get_users():
    """ Rota para retornar todos os usuários """
    with Session(engine) as session:
        statement = select(Usuario)
        results = session.exec(statement)
        usuarios = results.all()
        if not usuarios:
            raise HTTPException(status_code=404, detail="Sem usuários cadastrados")
        return usuarios


# Rota de cadastrar usuários
@router.post("/usuarios/cadastro", summary="Cadastrar usuário", description="Cadastra um usuário no banco de dados.",
      responses = {
          200: {"description": "Usuário cadastrado com sucesso."},
          400: {"description": "Bad request: Usuário já existe!"},
} )
def create_user(usuario: Usuario):
    """ Rota de cadastrar usuários """
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        return {"message": "Usuário criado"}


# Rota de procurar usuários
@router.get("/usuarios/procurar/{email_id}", summary="Procurar usuário", description="Retorna um único usuário pelo seu e-mail.",
        responses = {
            404: {"description": "Item not found"}
} )
def find_user(email_id: EmailStr):
    """
        Rota para procurar usuário. Insira o e-mail do usuário que deseja buscar.
    """
    with Session(engine) as session:
        statement = select(Usuario).where(Usuario.email == email_id)
        results = session.exec(statement)
        usuarios = results.all()
        return usuarios
    

