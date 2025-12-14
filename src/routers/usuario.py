from fastapi import APIRouter, HTTPException, status
from src.models.usuario import Usuario
from sqlmodel import select, Session
from src.utils.database import engine
from sqlalchemy.exc import IntegrityError
from src.utils.logger import logger

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



# Rota de cadastrar usuário
@router.post("/usuarios/cadastro", summary="Cadastrar usuário", description="Cadastra um usuário no banco de dados.",
      responses = {
          200: {"description": "Usuário cadastrado com sucesso."},
          400: {"description": "Bad request: Usuário já existe!"},
          409: {"description": "Erro de integridade: ID duplicado ou constraint violada"},
          422: {"description": "Bad request: Erro de validação do e-mail!"},
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
                return {"message": f"Usuário com o e-mail {usuario.email} já existe no banco de dados"}
            else:
                session.add(usuario) 
                session.commit()
                session.refresh(usuario)
                return {"message": f"Usuário cadastrado com sucesso"}
        logger.info(f'Usuário ${usuario.nome} cadastrado com sucesso')
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Erro de integridade: ID duplicado ou constraint violada"
        )


# Rota de procurar usuários
@router.get("/usuarios/procurar/{email_id}", summary="Procurar usuário", description="Retorna um único usuário pelo seu e-mail.",
        responses = {
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
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        else:
            return usuario
    

