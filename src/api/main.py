from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr
from src.models.usuario import Usuario


app = FastAPI(
    title="Exercício - API de Usuários",
    description="API for managing users",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@usersapi.com",
    },
)


app.mount("/static", StaticFiles(directory="src/static"), name="static")

favicon_path = 'static/favicon.ico'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/", summary="Rota padrão da API", description="Retorna uma mensagem se estiver em funcionamento.")
def home():
    """ Rota padrão da API """
    return {"message": "API em funcionamento!"}

# Instancia o banco de dados de usuários na memória
bd_usuarios = []



@app.get("/usuarios", summary="Listar usuários", description="Retorna todos os usuários cadastrados no banco de dados.",
      responses = {
          404: {"description": "Sem usuários cadastrados"}
} )
def get_users():
    """ Rota para retornar todos os usuários """
    if len(bd_usuarios) == 0:
        return JSONResponse(status_code=404, content="Sem usuários cadastrados")
    else:
        return bd_usuarios



@app.post("/usuario/cadastro", summary="Cadastrar usuário", description="Cadastra um usuário no banco de dados.",
      responses = {
          200: {"description": "Usuário cadastrado com sucesso."},
          400: {"description": "Bad request: Usuário já existe!"},
} )
def create_user(usuario: Usuario):
    """ Rota de cadastrar usuários """
    usuario_existente = [user for user in bd_usuarios if user.email == usuario.email]
    if usuario_existente:
      return JSONResponse(status_code=400, content=f"Já possui um usuário cadastrado com o e-mail {usuario.email}")
    else:
        bd_usuarios.append(usuario)
        return JSONResponse(status_code=200, content=f"Usuário {usuario.nome} cadastrado com sucesso!")    



@app.get("/usuario/procurar/{email_id}", summary="Procurar usuário", description="Retorna um único usuário pelo seu e-mail.",
        responses = {
            404: {"description": "Item not found"}
} )
def find_user(email_id: EmailStr):
    """
        Rota para procurar usuário. Insira o e-mail do usuário que deseja buscar.
    """
    usuario_localizado = [usuario for usuario in bd_usuarios if usuario.email == email_id]
    if usuario_localizado:
        return usuario_localizado
    else:
        return JSONResponse(status_code=404, content="Usuário não encontrado com este e-mail")
    
