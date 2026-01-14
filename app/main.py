"""
Ponto de entrada principal da aplicação FastAPI.
Configura middleware, CORS, logging e rotas.
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.api.routes import router

# ============== Configuração de Logging ==============

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


# ============== Lifecycle Events ==============

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    Executa código na inicialização e encerramento.
    """
    # Startup
    logger.info("=" * 50)
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Modelo OpenAI: {settings.OPENAI_MODEL}")
    logger.info(f"Debug: {settings.DEBUG}")
    logger.info("=" * 50)
    
    # Download de recursos NLP (se necessário)
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        logger.info("Recursos NLTK carregados")
    except Exception as e:
        logger.warning(f"Não foi possível carregar recursos NLTK: {e}")
    
    yield
    
    # Shutdown
    logger.info("Encerrando aplicação...")


# ============== Criação da Aplicação ==============

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Email Classification",
            "description": "Endpoints para classificação de emails"
        },
        {
            "name": "Status",
            "description": "Endpoints de status e monitoramento"
        }
    ]
)


# ============== Middleware ==============

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Exception Handlers ==============

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para erros de validação Pydantic."""
    logger.warning(f"Erro de validação: {exc.errors()}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "ValidationError",
            "message": "Dados de entrada inválidos",
            "details": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler genérico para exceções não tratadas."""
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "Ocorreu um erro interno no servidor",
            "details": str(exc) if settings.DEBUG else None
        }
    )


# ============== Rotas ==============

# Inclui todas as rotas da API
app.include_router(router, prefix="/api/v1", tags=["Email Classification"])


# Rota raiz
@app.get("/", tags=["Status"])
async def root():
    """Rota raiz com informações básicas da API."""
    return {
        "message": f"Bem-vindo à {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


# ============== Execução Direta ==============

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )

