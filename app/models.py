"""
Modelos Pydantic para validação de dados.
Define os schemas de request e response da API.
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


# ============== Request Models ==============

class EmailClassifyRequest(BaseModel):
    """Request para classificação de email."""
    
    email_content: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="Texto completo do email a ser classificado",
        examples=["Prezado, gostaria de solicitar uma análise do relatório financeiro do mês anterior."]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email_content": "Prezado, gostaria de solicitar uma análise do relatório financeiro do mês anterior. Aguardo retorno."
            }
        }


# ============== Response Models ==============

class EmailClassifyResponse(BaseModel):
    """Response da classificação de email."""
    
    classification: Literal["Produtivo", "Improdutivo"] = Field(
        ...,
        description="Classificação do email"
    )
    pontuation: int = Field(
        ...,
        ge=0,
        le=10,
        description="Pontuação de produtividade (0-10)"
    )
    suggested_reply: str = Field(
        ...,
        description="Resposta sugerida gerada pelo GPT"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Nível de confiança da classificação (0-1)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "classification": "Produtivo",
                "pontuation": 8,
                "suggested_reply": "Olá, recebemos sua solicitação e já estamos analisando. Em breve retornaremos com mais informações.",
                "confidence": 0.91
            }
        }


class EmailHistoryItem(BaseModel):
    """Item do histórico de emails."""
    
    id: str = Field(..., description="ID único do email")
    email_content: str = Field(..., description="Conteúdo do email")
    classification: Literal["Produtivo", "Improdutivo"]
    pontuation: int = Field(..., ge=0, le=10)
    suggested_reply: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "email-001",
                "email_content": "Solicito análise urgente do contrato...",
                "classification": "Produtivo",
                "pontuation": 9,
                "suggested_reply": "Prezado, recebemos sua solicitação...",
                "confidence": 0.95,
                "created_at": "2026-01-14T10:30:00"
            }
        }


class EmailListResponse(BaseModel):
    """Response da listagem de emails paginada."""
    
    items: list[EmailHistoryItem] = Field(..., description="Lista de emails")
    total: int = Field(..., description="Total de emails")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")
    total_pages: int = Field(..., description="Total de páginas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "page_size": 10,
                "total_pages": 10
            }
        }


class HealthResponse(BaseModel):
    """Response do health check."""
    
    status: str = Field(..., description="Status do serviço")
    openai_configured: bool = Field(..., description="Se a API OpenAI está configurada")
    nlp_info: dict = Field(..., description="Informações do módulo NLP")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "openai_configured": True,
                "nlp_info": {
                    "spacy_available": True,
                    "model": "pt_core_news_sm"
                }
            }
        }


class VersionResponse(BaseModel):
    """Response da versão da API."""
    
    version: str = Field(..., description="Versão da API")
    name: str = Field(..., description="Nome da aplicação")
    description: str = Field(..., description="Descrição da aplicação")
    
    class Config:
        json_schema_extra = {
            "example": {
                "version": "1.0.0",
                "name": "Email Classifier API",
                "description": "API para classificação de emails usando GPT e NLP"
            }
        }


class ErrorResponse(BaseModel):
    """Response de erro padrão."""
    
    error: str = Field(..., description="Tipo do erro")
    message: str = Field(..., description="Mensagem descritiva do erro")
    details: Optional[dict] = Field(None, description="Detalhes adicionais")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "O campo email_content é obrigatório",
                "details": None
            }
        }

