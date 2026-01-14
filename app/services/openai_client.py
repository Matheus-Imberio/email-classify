"""
Cliente OpenAI com retry e timeout configuráveis.
Centraliza a comunicação com a API da OpenAI.
"""

import logging
from typing import Optional
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from app.config import settings

# Configuração de logging
logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    Cliente singleton para comunicação com a API da OpenAI.
    Implementa retry automático e timeout configurável.
    """
    
    _instance: Optional["OpenAIClient"] = None
    
    def __new__(cls) -> "OpenAIClient":
        """Implementa padrão Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa o cliente OpenAI."""
        if self._initialized:
            return
            
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.timeout = settings.OPENAI_TIMEOUT
        self.max_retries = settings.OPENAI_MAX_RETRIES
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY não configurada. O serviço não funcionará.")
        
        self.client = OpenAI(
            api_key=self.api_key,
            timeout=self.timeout
        )
        
        self._initialized = True
        logger.info(f"Cliente OpenAI inicializado. Modelo: {self.model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((APIConnectionError, RateLimitError)),
        before_sleep=lambda retry_state: logger.warning(
            f"Tentativa {retry_state.attempt_number} falhou. Tentando novamente..."
        )
    )
    def chat_completion(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        model: Optional[str] = None
    ) -> str:
        """
        Realiza uma chamada de chat completion à API da OpenAI.
        
        Args:
            messages: Lista de mensagens no formato da API
            temperature: Criatividade da resposta (0-2)
            max_tokens: Máximo de tokens na resposta
            model: Modelo a ser usado (usa padrão se não especificado)
            
        Returns:
            Texto da resposta gerada
            
        Raises:
            APIError: Erro na API da OpenAI
        """
        try:
            response = self.client.chat.completions.create(
                model=model or self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            
            logger.debug(
                f"Resposta recebida. Tokens usados: "
                f"prompt={response.usage.prompt_tokens}, "
                f"completion={response.usage.completion_tokens}"
            )
            
            return content.strip() if content else ""
            
        except APIError as e:
            logger.error(f"Erro na API OpenAI: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao chamar OpenAI: {e}")
            raise
    
    def is_configured(self) -> bool:
        """
        Verifica se o cliente está configurado corretamente.
        
        Returns:
            True se a API key está configurada
        """
        return bool(self.api_key)
    
    def get_model_info(self) -> dict:
        """
        Retorna informações sobre a configuração atual.
        
        Returns:
            Dicionário com informações do modelo
        """
        return {
            "model": self.model,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "configured": self.is_configured()
        }


# Função auxiliar para obter instância do cliente
def get_openai_client() -> OpenAIClient:
    """
    Retorna a instância singleton do cliente OpenAI.
    
    Returns:
        Instância do OpenAIClient
    """
    return OpenAIClient()

