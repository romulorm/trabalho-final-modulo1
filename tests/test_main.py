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
    # ARRANGE (Preparar)
    payload = {
        "valor": 15000,  # Acima do threshold
        "hora_do_dia": 14,
        "distancia_ultima_compra_km": 50,
        "numero_transacoes_hoje": 3,
        "idade_conta_dias": 100
    }
    
    # ACT (Agir)
    response = client.post("/usuario/cadastro", json=payload)
    
    # ASSERT (Verificar)
    assert response.status_code == 200
    data = response.json()
    assert data["fraude"] == True  # ESPECIFICAÇÃO: > 10k = fraude
    assert data["confianca"] > 0.5
    assert "threshold" in data["motivo"].lower()


def test_cad_usuario_email_invalido():
    """
    Teste: Tentativa de cadastro de usuário com e-mail inválido.
    """
    # ARRANGE
    payload = {
        "valor": 500,  # Abaixo do threshold
        "hora_do_dia": 14,
        "distancia_ultima_compra_km": 10,
        "numero_transacoes_hoje": 2,
        "idade_conta_dias": 100
    }
    
    # ACT
    response = client.post("/usuario/cadastro", json=payload)
    
    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert data["fraude"] == False
    assert data["confianca"] > 0.5
