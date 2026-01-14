# 📧 Email Classifier API

API REST para classificação automática de emails usando GPT e técnicas de NLP.

## 🚀 Funcionalidades

- **Classificação de Emails**: Classifica emails como `Produtivo` ou `Improdutivo`
- **Geração de Respostas**: Cria respostas automáticas profissionais
- **Pré-processamento NLP**: Processamento de texto com spaCy
- **Cache em Memória**: Evita processamento duplicado
- **Paginação**: Lista emails ordenados por produtividade

## 📋 Requisitos

- Python 3.10+
- Chave de API da OpenAI

## 🛠️ Instalação

### Opção 1: Local (Recomendado para desenvolvimento)

```bash
# Crie ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt

# Baixe modelo spaCy para português (opcional, melhora NLP)
python -m spacy download pt_core_news_sm

# Configure variáveis de ambiente
# Crie um arquivo .env na raiz com:
# OPENAI_API_KEY=sua-chave-aqui
# OPENAI_MODEL=gpt-4o-mini

# Execute
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Opção 2: Docker

```bash
# Configure a variável de ambiente
set OPENAI_API_KEY=sua-chave-aqui  # Windows
# ou
export OPENAI_API_KEY=sua-chave-aqui  # Linux/Mac

# Execute com Docker Compose
docker-compose up -d
```

## 📚 Documentação da API

Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔌 Endpoints

### `POST /api/v1/classify-email`

Classifica um email e gera resposta sugerida.

**Request:**
```json
{
  "email_content": "Prezado, solicito uma análise urgente do relatório financeiro do mês anterior."
}
```

**Response:**
```json
{
  "classification": "Produtivo",
  "pontuation": 8,
  "suggested_reply": "Olá, recebemos sua solicitação e já estamos analisando. Em breve retornaremos com mais informações.",
  "confidence": 0.91
}
```

---

### `GET /api/v1/emails`

Lista emails classificados, ordenados por pontuação.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `page` | int | 1 | Número da página |
| `page_size` | int | 10 | Itens por página |
| `order` | string | desc | Ordenação: `desc` (mais produtivos) ou `asc` |

**Response:**
```json
{
  "items": [
    {
      "id": "uuid-aqui",
      "email_content": "Solicito análise...",
      "classification": "Produtivo",
      "pontuation": 9,
      "suggested_reply": "...",
      "confidence": 0.95,
      "created_at": "2026-01-14T10:30:00"
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10
}
```

---

### `GET /api/v1/health`

Verifica status da aplicação.

---

### `GET /api/v1/version`

Retorna versão da API.

---

### `GET /api/v1/history`

Retorna histórico completo de emails classificados.

---

## 📁 Estrutura do Projeto

```
projeto-teste/
├── app/
│   ├── api/
│   │   └── routes.py          # Endpoints da API
│   ├── services/
│   │   ├── openai_client.py   # Cliente OpenAI com retry
│   │   ├── classifier.py      # Serviço de classificação
│   │   └── response_generator.py
│   ├── nlp/
│   │   └── preprocess.py      # Pré-processamento NLP
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_nlp.py
│   ├── config.py              # Configurações
│   ├── models.py              # Schemas Pydantic
│   └── main.py                # Aplicação FastAPI
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## ⚙️ Variáveis de Ambiente

| Variável | Obrigatório | Padrão | Descrição |
|----------|-------------|--------|-----------|
| `OPENAI_API_KEY` | ✅ | - | Chave da API OpenAI |
| `OPENAI_MODEL` | ❌ | gpt-4o-mini | Modelo GPT |
| `OPENAI_TIMEOUT` | ❌ | 30 | Timeout em segundos |
| `DEBUG` | ❌ | false | Modo debug |

## 🧪 Testes

```bash
pip install pytest pytest-asyncio httpx
pytest app/tests/ -v
```

