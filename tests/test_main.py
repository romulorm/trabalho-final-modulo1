"""
Testes Automatizados - API de Cadastro de usuários
Estrutura AAA: Arrange, Act, Assert
"""

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_check():
    """
    Teste básico: verificar se a API está funcionando
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root():
    """
    Teste: verificar endpoint raiz
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "versao" in data


def test_cad_usuario_valido():
    """
    Teste: Cadastro de usuário válido.
    """
    payload = {
        "nome": "João da Silva",
        "email": "joao.silva@example.com",
        "idade": 30,
        "ativo": True
    }

    response = client.post("/usuario/cadastro", json=payload)

    assert response.status_code == 200
    assert "cadastrado com sucesso" in response.json().lower()

    

def test_cad_usuario_email_invalido():
    """
    Teste: Tentativa de cadastro de usuário com e-mail inválido.
    """
    response = client.get("/usuario/procurar/nao_existe@example.com")
    assert response.status_code == 404
    assert "não encontrado" in response.json().lower()
