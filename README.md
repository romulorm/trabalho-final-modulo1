# Trabalho final do Módulo 1

## 🧑🏻‍💻 INTEGRANTES DO GRUPO
- Filipe Ribeiro de Oliveira
- Luiz Eduardo Paes Salomão
- Rômulo Ribeiro Moreira

## 🎯 Desenvolver uma API contendo:
- **Organização**: Código limpo, estruturado, PEP 8
- **API funcionando**: Endpoints rodando, validação Pydantic
- **Testes**: Cobertura, casos válidos/inválidos
- **Git**: Commits descritivos, histórico claro
- **Documentação**: README completo, instruções claras

## 📋 Ferramentas necessárias ao desenvolvimento
- Python 3.12+
- Git
- VS Code (recomendado)
- Conta no GitHub

## 📂 Estrutura do Repositório local

```
trabalho-final-modulo1/
│
├── README.md                         # Este arquivo
├── requirements.txt                  # Dependências do projeto
├── .gitignore                        # Arquivos ignorados pelo Git
├── usuarios_teste.txt                # Arquivo contendo dicionários de usuários de teste
│
├── .venv/                            # Pasta do ambiente virtual
├── artifacts/                        # Pasta de artefatos do projeto (não utilizada)
│   ├── models/                       # Pasta de modelos treinados do projeto (não utilizada)
│
├── logs/                             # 🔍 Debug e Logs
│
├── src/                              # Códigos da aplicação
│   ├── api/                          # Pasta principal da API
│   ├── data/                         # Pasta de dados (não utilizada)
│   ├── models/                       # Pasta contendo os modelos do Pydantic
│   ├── static/                       # Pasta contendo arquivos estáticos
│       └── favicon.ico               # Ícone favicon.ico
│
├── logs/                             # 🔍 Debug e Logs
├── tests/                            # ✅ Testes Automatizados
```

## 🚀 Setup do sistema

### 1. Clone o repositório
```bash
git clone https://github.com/romulorm/trabalho-final-modulo1.git
cd trabalho-final-modulo1
```
### 2. Crie e ative o ambiente virtual
- No Linux
```bash
python -m venv .venv
source .venv/bin/activate
```
- No Windows
```bash
python -m venv .venv
.\.venv/bin/activate
```


### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Inicie a aplicação
```bash
cd trabalho-final-modulo1
uvicorn src.api.main:app --port 8001
```

## 🚀 Acesso ao Swagger do sistema

### 1. Abra o navegador de Internet
### 2. Acesse o endereço eletrônico http://127.0.0.1:8001/docs

## ✅ Teste a aplicação
```bash
cd trabalho-final-modulo1
```
### No Linux/macOS:
```bash
PYTHONPATH=. pytest -v -rP
```

### No Windows (Command Prompt):
```bash
set PYTHONPATH=. && pytest -v -rP
```

### No Windows (PowerShell):
```bash
$env:PYTHONPATH='.' ; pytest -v -rP
```
