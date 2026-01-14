"""
Configurações da aplicação.
Carrega variáveis de ambiente e define constantes do sistema.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """
    Configurações centralizadas da aplicação.
    Valores são carregados de variáveis de ambiente ou .env
    """
    
    # API Info
    APP_NAME: str = "Email Classifier API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API para classificação de emails usando GPT e NLP"
    DEBUG: bool = False
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_TIMEOUT: int = 30
    OPENAI_MAX_RETRIES: int = 3
    
    # Cache
    CACHE_TTL: int = 3600  # 1 hora em segundos
    CACHE_MAX_SIZE: int = 1000
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna instância cacheada das configurações.
    Usar lru_cache evita recarregar o .env a cada requisição.
    """
    return Settings()


# Instância global para uso direto
settings = get_settings()

