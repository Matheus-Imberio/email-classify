# 📧 Email Intelligence

Sistema completo para classificação automática de emails usando **GPT** e técnicas de **NLP**, com interface web moderna em **Streamlit**.

![Status](https://img.shields.io/badge/Status-Ativo-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)

---

## 🚀 Funcionalidades

- 🤖 **Classificação Inteligente** - Classifica emails como `Produtivo` ou `Improdutivo` usando IA
- ✍️ **Geração de Respostas** - Cria respostas automáticas profissionais
- 📊 **Pontuação de Produtividade** - Escala de 0-10 com nível de confiança
- 🔍 **Pré-processamento NLP** - Processamento de texto com spaCy
- 💾 **Cache em Memória** - Evita processamento duplicado
- 📜 **Histórico** - Acompanhe todos os emails classificados
- 🎨 **Interface Web** - Frontend moderno e intuitivo

---

## 📋 Pré-requisitos

- **Python 3.10+**
- **Chave de API da OpenAI** ([Obter aqui](https://platform.openai.com/api-keys))

---

## 🛠️ Instalação Local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/email-classifier.git
cd email-classifier
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. (Opcional) Baixe o modelo spaCy para português

```bash
python -m spacy download pt_core_news_sm
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua-chave-da-openai-aqui
OPENAI_MODEL=gpt-4o-mini
DEBUG=false
```

> ⚠️ **Importante:** Nunca compartilhe sua chave da OpenAI! O arquivo `.env` já está no `.gitignore`.

---

## ▶️ Como Executar Localmente

### Opção 1: Script Windows (Mais fácil)

```bash
start.bat
```

Abre duas janelas automaticamente: uma com o backend e outra com o frontend.

---

### Opção 2: Script Python

```bash
python run.py
```

Inicia backend e frontend simultaneamente.

---

### Opção 3: Executar Separadamente (Recomendado para desenvolvimento)

**Terminal 1 - Backend (API):**
```bash
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend (Interface):**
```bash
streamlit run app/frontend.py
```

---

### Opção 4: Docker

```bash
# Configure a variável de ambiente
export OPENAI_API_KEY=sua-chave-aqui   # Linux/Mac
set OPENAI_API_KEY=sua-chave-aqui      # Windows

# Execute com Docker Compose
docker-compose up -d
```

---

## 🌐 Acessar a Aplicação

Após iniciar, acesse:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| 🎨 **Frontend** | http://localhost:8501 | Interface do usuário |
| 📡 **Backend API** | http://localhost:8000 | API REST |
| 📚 **Documentação** | http://localhost:8000/docs | Swagger UI interativo |
| 📖 **ReDoc** | http://localhost:8000/redoc | Documentação alternativa |

---


## 🔌 API Endpoints

### `POST /api/v1/classify-email`

Classifica um email e gera resposta sugerida.

**Request:**
```json
{
  "email_content": "Prezado, solicito uma análise urgente do relatório financeiro."
}
```

**Response:**
```json
{
  "classification": "Produtivo",
  "pontuation": 8,
  "suggested_reply": "Prezado, recebemos sua solicitação e estamos analisando...",
  "confidence": 0.91
}
```

---

### `GET /api/v1/emails`

Lista emails classificados com paginação.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `page` | int | 1 | Número da página |
| `page_size` | int | 10 | Itens por página |
| `order` | string | desc | `desc` ou `asc` |

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
email-classifier/
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
│   ├── main.py                    # Aplicação FastAPI (Backend)
│   └── frontend.py                # Interface Streamlit (Frontend)
│
├── railway.json                   # Config Railway (Backend)
├── railway-frontend.json          # Config Railway (Frontend)
├── start_frontend.sh              # Script inicialização frontend
├── run.py                         # Rodar backend + frontend
├── run_frontend.py                # Rodar só o frontend
├── start.bat                      # Script Windows
│
├── requirements.txt               # Dependências Python
├── Dockerfile                     # Container Docker
├── docker-compose.yml             # Orquestração Docker
├── .env.example                   # Exemplo de variáveis
├── .gitignore
└── README.md
```

---

## ⚙️ Variáveis de Ambiente

| Variável | Obrigatório | Padrão | Descrição |
|----------|-------------|--------|-----------|
| `OPENAI_API_KEY` | ✅ Sim | - | Chave da API OpenAI |
| `OPENAI_MODEL` | Não | `gpt-4o-mini` | Modelo GPT a usar |
| `OPENAI_TIMEOUT` | Não | `30` | Timeout em segundos |
| `DEBUG` | Não | `false` | Modo debug |
| `API_URL` | Não* | `http://localhost:8000/api/v1` | URL do backend (para frontend) |
| `PORT` | Não | `8080` | Porta do servidor |

> *Obrigatório no frontend em produção

---

## 🧪 Testes

```bash
# Instale dependências de teste
pip install pytest pytest-asyncio httpx

# Execute os testes
pytest app/tests/ -v
```

---

## 🐛 Solução de Problemas

### Erro: "OPENAI_API_KEY não configurada"
- Verifique se o arquivo `.env` existe e contém a chave
- Ou defina a variável de ambiente diretamente

### Erro 502 no Railway
- Verifique os logs em **"View logs"**
- Certifique-se que o `PORT` está definido nas variáveis
- Verifique se o `railway-frontend.json` está correto

### Frontend não conecta ao Backend
- Verifique se a variável `API_URL` está correta
- Certifique-se que o backend está rodando

### Builds lentos no Railway
- Planos gratuitos têm menor prioridade
- Tente em horários de menor tráfego (manhã cedo)

---
