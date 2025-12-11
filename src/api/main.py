from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr
from contextlib import asynccontextmanager
from src.utils.database import create_db
from src.models.usuario import Usuario
import logging

# -----------------------------
# FASTAPI configuration
# -----------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    create_db()
    yield
    # Code to run on shutdown
    print("Application shutting down...")
    logger.info("Application shutting down...")


app = FastAPI(
    title="Exercício - API de Usuários",
    description="API for managing users",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@usersapi.com",
    },
    lifespan=lifespan
)

# -----------------------------
# CORS configuration
# -----------------------------

origins = [
    "http://localhost:3000",      # Exemplo para um frontend Vue/React/Angular local
    "http://localhost:5173",
]

# 2. Adicione o Middleware à sua aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Permite estas origens específicas
    allow_credentials=True,         # Permite cookies e cabeçalhos de autorização (Bearer Tokens)
    allow_methods=["*"],            # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Permite todos os cabeçalhos HTTP
)

# -----------------------------
# LOGGING configuration
# -----------------------------

# Configure logging to a file
logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
 
logger = logging.getLogger(__name__)

logger.info('****************** API Started *****************')

# -----------------------------
# FAVICON configuration
# -----------------------------

app.mount("/static", StaticFiles(directory="src/static"), name="static")
favicon_path = 'src/static/favicon.ico'


# -----------------------------
# ROUTES configuration
# -----------------------------


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/health", summary="Rota de saúde da API", description="Retorna uma mensagem de status se estiver em funcionamento.")
def get_health():
    """ Rota de saúde da API """
    return {"status": "healthy"}


@app.get("/", summary="Rota padrão da API", description="Retorna o status e versão da API.")
def home():
    """ Rota padrão da API """
    return {"status": "running", "versao": "1.0.0"}


# Rota de listar usuários
@app.get("/usuarios", summary="Listar usuários", description="Retorna todos os usuários cadastrados no banco de dados.",
      responses = {
          404: {"description": "Sem usuários cadastrados"}
} )
def get_users():
    """ Rota para retornar todos os usuários """
    return {"message": "Rota para listar usuários"}


# Rota de cadastrar usuários
@app.post("/usuario/cadastro", summary="Cadastrar usuário", description="Cadastra um usuário no banco de dados.",
      responses = {
          200: {"description": "Usuário cadastrado com sucesso."},
          400: {"description": "Bad request: Usuário já existe!"},
} )
def create_user(usuario: Usuario):
    """ Rota de cadastrar usuários """
    return {"message": "Rota para criar usuários"}


# Rota de procurar usuários
@app.get("/usuario/procurar/{email_id}", summary="Procurar usuário", description="Retorna um único usuário pelo seu e-mail.",
        responses = {
            404: {"description": "Item not found"}
} )
def find_user(email_id: EmailStr):
    """
        Rota para procurar usuário. Insira o e-mail do usuário que deseja buscar.
    """
    return {"message": "Rota para procurar usuário"}
    

