from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from src.models.usuario import Usuario
from sqlmodel import select, Session
from src.utils.database import engine
from sqlalchemy.exc import IntegrityError
from src.utils.logger import logger

router = APIRouter()

# Rota de listar usuários
@router.get("/usuarios", summary="Listar usuários", description="Retorna todos os usuários cadastrados no banco de dados.",
      responses = {
          200: {"description": "Usuários retornados"},
          404: {"description": "Sem usuários cadastrados"}
} )
def get_users():
    """ Rota para retornar todos os usuários """
    with Session(engine) as session:
        statement = select(Usuario)
        results = session.exec(statement)
        usuarios = results.all()
        if not usuarios:
            return JSONResponse(status_code=404, content={"message": "Sem usuários cadastrados"})
        else:
            return usuarios



# Rota de cadastrar usuário
@router.post("/usuarios/cadastrar", summary="Cadastrar usuário", description="Cadastra um usuário no banco de dados.",
      responses = {
          201: {"description": "Usuário cadastrado com sucesso."},
          400: {"description": "Bad request: E-mail já utilizado em outro cadastro"},
          409: {"description": "Erro de integridade: ID duplicado ou constraint violada"},
} )
def create_user(usuario: Usuario):
    """ Rota de cadastrar usuários """
    try:
        with Session(engine) as session:
            # Verifica se o usuário existe
            statement = select(Usuario).where(Usuario.email == usuario.email)
            results = session.exec(statement)
            usuario_existente = results.first()
            if usuario_existente:
                return JSONResponse(status_code=400, content={"message": "E-mail já utilizado em outro cadastro"})
            else:
                session.add(usuario) 
                session.commit()
                session.refresh(usuario)
                logger.info(f'Usuário {usuario.nome} cadastrado com sucesso')
                return JSONResponse(status_code=201, content={"message": "Usuário cadastrado com sucesso"})
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Erro de integridade: ID duplicado ou constraint violada"
        )


# Rota de procurar usuários
@router.get("/usuarios/procurar/{email_id}", summary="Procurar usuário", description="Retorna um único usuário pelo seu e-mail.",
        responses = {
            200: {"description": "Usuário retornado"},
            404: {"description": "Item not found"}
} )
def find_user(email_id: str):
    """
        Rota para procurar usuário. Insira o e-mail do usuário que deseja buscar.
    """
    with Session(engine) as session:
        statement = select(Usuario).where(Usuario.email == email_id)
        results = session.exec(statement)
        usuario = results.first()
        if not usuario:
            return JSONResponse(status_code=404, content={"message": "Usuário não localizado"})
        else:
            return usuario
    

# Rota de deletar usuário
@router.delete("/usuarios/remover/{email_id}", summary="Remover usuário", description="Remove um usuário do banco de dados pelo seu e-mail.",
        responses = {
            200: {"description": "Usuário deletado com sucesso"},
            404: {"description": "Usuário não localizado"}
} )
def delete_user(email_id: str):
    """ Rota para deletar usuário. Insira o e-mail do usuário que deseja deletar. """
    with Session(engine) as session:
        statement = select(Usuario).where(Usuario.email == email_id)
        results = session.exec(statement)
        usuario = results.first()
        if not usuario:
            return JSONResponse(status_code=404, content={"message": "Usuário não localizado"})
        else:
            session.delete(usuario)
            session.commit()
            logger.info(f'Usuário {usuario.nome} deletado com sucesso')
            return JSONResponse(status_code=200, content={"message": "Usuário removido com sucesso"})