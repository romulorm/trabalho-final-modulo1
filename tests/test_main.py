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
        "nome": "Pytest User",
        "email": "pytest@example.com",
        "idade": 30,
        "ativo": 1
    }

    response = client.post("/usuarios/cadastrar", json=payload)
    
    assert response.status_code == 201
    assert response.json()["message"] == "Usuário cadastrado com sucesso"

def test_cad_usuario_existente():
    """
    Teste: Cadastro com e-mail já existente.
    """
    payload = {
        "nome": "Pytest User",
        "email": "pytest@example.com",
        "idade": 30,
        "ativo": 1
    }

    response = client.post("/usuarios/cadastrar", json=payload)

    assert response.status_code == 400
    assert response.json()["message"] == "E-mail já utilizado em outro cadastro"


def test_procurar_usuario_inexistente():
    """
    Teste: Procurar usuário inexistente.
    """
    payload = "inexistente@pytest.com"

    response = client.get(f"/usuarios/procurar/{payload}")
    assert response.status_code == 404
    assert response.json()["message"] == "Usuário não localizado"

def test_remover_usuario():
    """
    Teste: Excluir usuário já existente.
    """
    payload = "pytest@example.com"

    response = client.delete(f"/usuarios/remover/{payload}")

    assert response.status_code == 200
    assert response.json()["message"] == "Usuário removido com sucesso"