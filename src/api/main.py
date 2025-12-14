from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.utils.database import create_db
from src.routers import usuario
from src.utils.logger import logger

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


logger.info('****************** API Started *****************')

# -----------------------------
# FAVICON configuration
# -----------------------------

app.mount("/static", StaticFiles(directory="src/static"), name="static")
favicon_path = 'src/static/favicon.ico'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

# -----------------------------
# API ROUTES configuration
# -----------------------------


@app.get("/health", summary="Rota de saúde da API", description="Retorna uma mensagem de status se estiver em funcionamento.")
def get_health():
    """ Rota de saúde da API """
    return {"status": "healthy"}


@app.get("/", summary="Rota padrão da API", description="Retorna o status e versão da API.")
def home():
    """ Rota padrão da API """
    return {"status": "running", "version": "2.0.0"}


app.include_router(usuario.router)