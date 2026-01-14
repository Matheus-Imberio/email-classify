"""
Serviço de classificação de emails.
Utiliza GPT para classificar emails como Produtivo ou Improdutivo.
"""

import logging
import re
from typing import Tuple

from app.services.openai_client import get_openai_client
from app.nlp.preprocess import preprocess_text

# Configuração de logging
logger = logging.getLogger(__name__)

# Prompt de classificação estruturado
CLASSIFICATION_PROMPT = """Classifique o email abaixo como PRODUTIVO ou IMPRODUTIVO.

Critérios:
- PRODUTIVO: exige ação, resposta, análise, suporte ou acompanhamento.
- IMPRODUTIVO: agradecimentos, felicitações, mensagens sociais, sem ação necessária.

Email:
"{email_content}"

Responda no seguinte formato JSON:
{{"classification": "Produtivo" ou "Improdutivo", "confidence": valor entre 0.0 e 1.0, "pontuation": valor inteiro de 0 a 10}}

Onde:
- classification: a classificação do email
- confidence: seu nível de confiança na classificação (0.0 = sem confiança, 1.0 = certeza absoluta)
- pontuation: pontuação de produtividade (0 = totalmente improdutivo, 10 = extremamente produtivo)

Responda APENAS com o JSON, sem texto adicional."""


def extract_classification_data(response: str) -> dict:
    """
    Extrai dados de classificação da resposta do GPT.
    
    Args:
        response: Resposta do GPT
        
    Returns:
        Dicionário com classification, confidence e pontuation
    """
    import json
    
    # Tenta parsear como JSON primeiro
    try:
        # Remove possíveis caracteres extras
        cleaned = response.strip()
        if cleaned.startswith("```"):
            # Remove markdown code blocks
            cleaned = re.sub(r'```json?\s*', '', cleaned)
            cleaned = re.sub(r'```\s*$', '', cleaned)
        
        data = json.loads(cleaned)
        
        classification = data.get("classification", "Improdutivo")
        confidence = float(data.get("confidence", 0.5))
        pontuation = int(data.get("pontuation", 5))
        
        # Normaliza a classificação
        if "produtivo" in classification.lower():
            if "improdutivo" in classification.lower():
                classification = "Improdutivo"
            else:
                classification = "Produtivo"
        else:
            classification = "Improdutivo"
        
        # Garante ranges válidos
        confidence = max(0.0, min(1.0, confidence))
        pontuation = max(0, min(10, pontuation))
        
        return {
            "classification": classification,
            "confidence": confidence,
            "pontuation": pontuation
        }
        
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        logger.warning(f"Falha ao parsear JSON, usando fallback: {e}")
        
        # Fallback: tenta extrair da resposta de texto
        response_lower = response.lower()
        
        if "produtivo" in response_lower and "improdutivo" not in response_lower:
            classification = "Produtivo"
            pontuation = 7
        else:
            classification = "Improdutivo"
            pontuation = 3
        
        return {
            "classification": classification,
            "confidence": 0.5,
            "pontuation": pontuation
        }


async def classify_email(
    email_content: str,
    use_preprocessing: bool = True
) -> dict:
    """
    Classifica um email como Produtivo ou Improdutivo usando GPT.
    
    Args:
        email_content: Conteúdo do email a ser classificado
        use_preprocessing: Se True, aplica pré-processamento NLP
        
    Returns:
        Dicionário com:
        - classification: "Produtivo" ou "Improdutivo"
        - confidence: Nível de confiança (0.0 a 1.0)
        - pontuation: Pontuação de 0 a 10
        - preprocessed_text: Texto pré-processado (se aplicado)
    """
    logger.info(f"Classificando email. Tamanho: {len(email_content)} caracteres")
    
    # Pré-processamento NLP
    preprocessed = ""
    if use_preprocessing:
        preprocessed = preprocess_text(email_content)
        logger.debug(f"Texto pré-processado: {preprocessed[:100]}...")
    
    # Usa o texto original para classificação (GPT precisa do contexto completo)
    # mas podemos usar o pré-processado para análise adicional
    prompt = CLASSIFICATION_PROMPT.format(email_content=email_content)
    
    # Chama o GPT
    client = get_openai_client()
    
    messages = [
        {
            "role": "system",
            "content": "Você é um assistente especializado em análise de emails corporativos."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    response = client.chat_completion(
        messages=messages,
        temperature=0.3,  # Baixa temperatura para classificação consistente
        max_tokens=200
    )
    
    logger.debug(f"Resposta do GPT: {response}")
    
    # Extrai dados da resposta
    result = extract_classification_data(response)
    result["preprocessed_text"] = preprocessed
    
    logger.info(
        f"Classificação concluída: {result['classification']} "
        f"(confiança: {result['confidence']:.2f}, pontuação: {result['pontuation']})"
    )
    
    return result

