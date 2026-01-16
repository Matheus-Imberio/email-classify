# 📧 Email Intelligence

Sistema completo para classificação automática de emails usando **GPT** e técnicas de **NLP**, com interface web moderna em **Streamlit**.

![Interface do Email Intelligence](https://img.shields.io/badge/Status-Ativo-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green) ![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)

## 🚀 Funcionalidades

- **🤖 Classificação Inteligente**: Classifica emails como `Produtivo` ou `Improdutivo` usando IA
- **✍️ Geração de Respostas**: Cria respostas automáticas profissionais
- **📊 Pontuação de Produtividade**: Escala de 0-10 com nível de confiança
- **🔍 Pré-processamento NLP**: Processamento de texto com spaCy
- **💾 Cache em Memória**: Evita processamento duplicado
- **📜 Histórico**: Acompanhe todos os emails classificados
- **🎨 Interface Web**: Frontend moderno e intuitivo com Streamlit

## 📋 Requisitos

- Python 3.10+
- Chave de API da OpenAI

## 🛠️ Instalação

### 1. Clone e configure o ambiente

```bash
# Crie ambiente virtual
python -m venv venv

# Ative o ambiente
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Instale dependências
pip install -r requirements.txt

# (Opcional) Baixe modelo spaCy para português
python -m spacy download pt_core_news_sm
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua-chave-aqui
OPENAI_MODEL=gpt-4o-mini
DEBUG=false
```

## ▶️ Como Executar

### Opção 1: Script Windows (Recomendado)

```bash
start.bat
```

Isso abre duas janelas automaticamente com backend e frontend.

### Opção 2: Script Python

```bash
python run.py
```

### Opção 3: Executar separadamente (Desenvolvimento)

**Terminal 1 - Backend:**
```bash
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
streamlit run app/frontend.py
```

Ou use o script auxiliar:
```bash
python run_frontend.py
```

### Opção 4: Docker

```bash
# Configure a variável de ambiente
set OPENAI_API_KEY=sua-chave-aqui      # Windows
export OPENAI_API_KEY=sua-chave-aqui   # Linux/Mac

# Execute com Docker Compose
docker-compose up -d
```

## 🌐 Acessar a Aplicação

Após iniciar, acesse:

| Serviço | URL |
|---------|-----|
| **🎨 Frontend (Interface)** | http://localhost:8501 |
| **📡 Backend API** | http://localhost:8000 |
| **📚 Swagger UI** | http://localhost:8000/docs |
| **📖 ReDoc** | http://localhost:8000/redoc |

---

## 🔌 Endpoints da API

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

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `page` | int | 1 | Número da página |
| `page_size` | int | 10 | Itens por página |
| `order` | string | desc | Ordenação: `desc` ou `asc` |

---

### `GET /api/v1/history`

Retorna histórico completo de emails classificados.

---

### `DELETE /api/v1/history`

Limpa o histórico de emails.

---

### `GET /api/v1/health`

Verifica status da aplicação.

---

### `GET /api/v1/version`

Retorna versão da API.

---

## 📁 Estrutura do Projeto

```
projeto-teste/
├── app/
│   ├── api/
│   │   └── routes.py              # Endpoints da API
│   ├── services/
│   │   ├── openai_client.py       # Cliente OpenAI com retry
│   │   ├── classifier.py          # Serviço de classificação
│   │   └── response_generator.py  # Gerador de respostas
│   ├── nlp/
│   │   └── preprocess.py          # Pré-processamento NLP
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_nlp.py
│   ├── config.py                  # Configurações
│   ├── models.py                  # Schemas Pydantic
│   ├── main.py                    # Aplicação FastAPI
│   └── frontend.py                # Interface Streamlit
├── run.py                         # Script para rodar tudo
├── run_frontend.py                # Script para rodar só o frontend
├── start.bat                      # Script Windows
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
pytest app/tests/ -v
```

## 📝 Licença

© 2026 Email Intelligence Classifier. Todos os direitos reservados.
