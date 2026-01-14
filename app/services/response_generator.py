"""
Serviço de geração de respostas automáticas.
Utiliza GPT para criar respostas profissionais para emails.
"""

import logging
from typing import Optional

from app.services.openai_client import get_openai_client

# Configuração de logging
logger = logging.getLogger(__name__)

# Template do prompt de geração de resposta
RESPONSE_PROMPT_TEMPLATE = """Você é um assistente corporativo de uma empresa do setor financeiro.

Crie uma resposta educada, profissional, clara e objetiva para o email abaixo.

A resposta deve:
- Ser cordial e profissional
- Ser clara e direta
- Ter no máximo 150 palavras
- Usar linguagem formal em português brasileiro
- Incluir saudação inicial e despedida

Categoria do email: {classification}
Pontuação de produtividade: {pontuation}/10

Email original:
"{email_content}"

Gere apenas a resposta, sem comentários adicionais."""


async def generate_response(
    email_content: str,
    classification: str,
    pontuation: int = 5,
    custom_instructions: Optional[str] = None
) -> str:
    """
    Gera uma resposta automática profissional para um email.
    
    Args:
        email_content: Conteúdo do email original
        classification: Classificação do email (Produtivo/Improdutivo)
        pontuation: Pontuação de produtividade (0-10)
        custom_instructions: Instruções adicionais opcionais
        
    Returns:
        Texto da resposta sugerida
    """
    logger.info(f"Gerando resposta para email {classification}")
    
    # Prepara o prompt
    prompt = RESPONSE_PROMPT_TEMPLATE.format(
        classification=classification,
        pontuation=pontuation,
        email_content=email_content
    )
    
    # Adiciona instruções customizadas se fornecidas
    if custom_instructions:
        prompt += f"\n\nInstruções adicionais: {custom_instructions}"
    
    # Chama o GPT
    client = get_openai_client()
    
    messages = [
        {
            "role": "system",
            "content": (
                "Você é um assistente corporativo experiente do setor financeiro. "
                "Suas respostas são sempre profissionais, cordiais e objetivas. "
                "Você escreve em português brasileiro formal."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    # Temperatura um pouco mais alta para respostas mais naturais
    response = client.chat_completion(
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    
    logger.info(f"Resposta gerada. Tamanho: {len(response)} caracteres")
    
    return response.strip()


async def generate_quick_reply(
    email_content: str,
    classification: str
) -> str:
    """
    Gera uma resposta rápida e curta para um email.
    
    Args:
        email_content: Conteúdo do email original
        classification: Classificação do email
        
    Returns:
        Resposta curta (até 50 palavras)
    """
    logger.info("Gerando resposta rápida")
    
    client = get_openai_client()
    
    prompt = f"""Crie uma resposta muito curta (máximo 50 palavras) para este email.
Seja profissional e direto.

Categoria: {classification}

Email: "{email_content}"

Resposta:"""
    
    messages = [
        {
            "role": "system",
            "content": "Você é um assistente que escreve respostas curtas e profissionais."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    response = client.chat_completion(
        messages=messages,
        temperature=0.5,
        max_tokens=100
    )
    
    return response.strip()

