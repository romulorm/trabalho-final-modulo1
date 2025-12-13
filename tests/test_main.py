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
    assert "version" in data


def test_cad_usuario_valido():
    """
    Teste: Cadastro de usuário válido.
    """
    payload = {
        "nome": "João da Silva",
        "email": "joao.silva2@example.com",
        "idade": 30,
        "ativo": True
    }

    response = client.post("/usuarios/cadastro", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Usuário cadastrado com sucesso"


def test_cadastro_usuario_email_invalido():
    """
    Teste: cadastro com e-mail com formato inválido deve retornar 422.
    Validação feita automaticamente pelo Pydantic (EmailStr).
    """
    payload = {
        "nome": "Usuário Teste",
        "email": "email-invalido",   # sem @ e domínio
        "idade": 25,
        "ativo": True
    }

    response = client.post("/usuarios/cadastro", json=payload)

    error_response = response.json()
    assert response.status_code == 422

