"""
Rotas da API REST.
Define todos os endpoints da aplicação.
"""

import logging
import uuid
from datetime import datetime
from typing import Optional
from math import ceil

from fastapi import APIRouter, HTTPException, Query
from cachetools import TTLCache

from app.config import settings
from app.models import (
    EmailClassifyRequest,
    EmailClassifyResponse,
    EmailHistoryItem,
    EmailListResponse,
    HealthResponse,
    VersionResponse,
    ErrorResponse
)
from app.services.classifier import classify_email
from app.services.response_generator import generate_response
from app.services.openai_client import get_openai_client
from app.nlp.preprocess import get_nlp_info

# Configuração de logging
logger = logging.getLogger(__name__)

# Router principal
router = APIRouter()

# Cache em memória para resultados
# Chave: hash do email_content, Valor: resultado da classificação
result_cache: TTLCache = TTLCache(
    maxsize=settings.CACHE_MAX_SIZE,
    ttl=settings.CACHE_TTL
)

# Armazenamento em memória para histórico (mock)
email_history: list[EmailHistoryItem] = []


def get_cache_key(email_content: str) -> str:
    """Gera chave de cache baseada no conteúdo do email."""
    return str(hash(email_content))


# ============== Endpoints Principais ==============

@router.post(
    "/classify-email",
    response_model=EmailClassifyResponse,
    responses={
        200: {"description": "Email classificado com sucesso"},
        400: {"model": ErrorResponse, "description": "Erro de validação"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"},
        503: {"model": ErrorResponse, "description": "Serviço OpenAI indisponível"}
    },
    summary="Classificar Email",
    description="Classifica um email como Produtivo ou Improdutivo e gera uma resposta sugerida."
)
async def classify_email_endpoint(request: EmailClassifyRequest) -> EmailClassifyResponse:
    """
    Classifica um email e gera uma resposta automática.
    
    O processo inclui:
    1. Pré-processamento NLP do texto
    2. Classificação via GPT (Produtivo/Improdutivo)
    3. Geração de resposta sugerida via GPT
    4. Armazenamento no histórico
    
    Args:
        request: Conteúdo do email a ser classificado
        
    Returns:
        Classificação, pontuação, resposta sugerida e confiança
    """
    logger.info(f"Recebida requisição para classificar email. Tamanho: {len(request.email_content)} chars")
    
    # Verifica se OpenAI está configurada
    client = get_openai_client()
    if not client.is_configured():
        logger.error("API OpenAI não configurada")
        raise HTTPException(
            status_code=503,
            detail="Serviço OpenAI não configurado. Defina OPENAI_API_KEY."
        )
    
    # Verifica cache
    cache_key = get_cache_key(request.email_content)
    if cache_key in result_cache:
        logger.info("Resultado encontrado em cache")
        return result_cache[cache_key]
    
    try:
        # Classifica o email
        classification_result = await classify_email(request.email_content)
        
        # Gera resposta sugerida
        suggested_reply = await generate_response(
            email_content=request.email_content,
            classification=classification_result["classification"],
            pontuation=classification_result["pontuation"]
        )
        
        # Monta resposta
        response = EmailClassifyResponse(
            classification=classification_result["classification"],
            pontuation=classification_result["pontuation"],
            suggested_reply=suggested_reply,
            confidence=classification_result["confidence"]
        )
        
        # Salva no cache
        result_cache[cache_key] = response
        
        # Salva no histórico
        history_item = EmailHistoryItem(
            id=str(uuid.uuid4()),
            email_content=request.email_content[:500],  # Limita tamanho no histórico
            classification=response.classification,
            pontuation=response.pontuation,
            suggested_reply=response.suggested_reply,
            confidence=response.confidence,
            created_at=datetime.now()
        )
        email_history.append(history_item)
        
        logger.info(f"Email classificado como {response.classification} (pontuação: {response.pontuation})")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar email: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar email: {str(e)}"
        )


@router.get(
    "/emails",
    response_model=EmailListResponse,
    summary="Listar Emails",
    description="Lista emails classificados, ordenados por pontuação (mais produtivos primeiro)."
)
async def list_emails(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Ordenação: desc (mais produtivos primeiro) ou asc")
) -> EmailListResponse:
    """
    Lista todos os emails classificados com paginação.
    
    Os emails são ordenados por pontuação de produtividade:
    - desc: do mais produtivo para o menos produtivo
    - asc: do menos produtivo para o mais produtivo
    
    Args:
        page: Número da página (começando em 1)
        page_size: Quantidade de itens por página
        order: Direção da ordenação (desc ou asc)
        
    Returns:
        Lista paginada de emails com metadados
    """
    logger.info(f"Listando emails. Página: {page}, Tamanho: {page_size}, Ordem: {order}")
    
    # Ordena por pontuação
    sorted_history = sorted(
        email_history,
        key=lambda x: x.pontuation,
        reverse=(order == "desc")
    )
    
    # Paginação
    total = len(sorted_history)
    total_pages = ceil(total / page_size) if total > 0 else 1
    
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    items = sorted_history[start_idx:end_idx]
    
    return EmailListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


# ============== Endpoints de Status ==============

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verifica o status de saúde da aplicação."
)
async def health_check() -> HealthResponse:
    """
    Verifica se a aplicação está funcionando corretamente.
    
    Retorna:
    - Status geral do serviço
    - Se a API OpenAI está configurada
    - Informações do módulo NLP
    """
    client = get_openai_client()
    nlp_info = get_nlp_info()
    
    return HealthResponse(
        status="healthy",
        openai_configured=client.is_configured(),
        nlp_info=nlp_info
    )


@router.get(
    "/version",
    response_model=VersionResponse,
    summary="Versão da API",
    description="Retorna informações da versão da API."
)
async def get_version() -> VersionResponse:
    """Retorna a versão atual da API."""
    return VersionResponse(
        version=settings.APP_VERSION,
        name=settings.APP_NAME,
        description=settings.APP_DESCRIPTION
    )


@router.get(
    "/history",
    response_model=list[EmailHistoryItem],
    summary="Histórico de Emails (Mock)",
    description="Retorna o histórico completo de emails classificados."
)
async def get_history(
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Limite de resultados")
) -> list[EmailHistoryItem]:
    """
    Retorna o histórico de emails classificados.
    
    Este é um endpoint de mock que retorna os dados armazenados em memória.
    Em produção, seria conectado a um banco de dados.
    
    Args:
        limit: Número máximo de itens a retornar
        
    Returns:
        Lista de emails classificados
    """
    if limit:
        return email_history[:limit]
    return email_history


@router.delete(
    "/history",
    summary="Limpar Histórico",
    description="Limpa todo o histórico de emails (apenas para desenvolvimento)."
)
async def clear_history() -> dict:
    """Limpa o histórico de emails em memória."""
    email_history.clear()
    result_cache.clear()
    logger.info("Histórico e cache limpos")
    return {"message": "Histórico limpo com sucesso", "status": "ok"}

