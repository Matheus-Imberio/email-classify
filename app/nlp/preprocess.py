"""
Módulo de pré-processamento NLP.
Aplica técnicas de processamento de linguagem natural no texto dos emails.
"""

import re
import string
import logging
from typing import Optional

# Configuração de logging
logger = logging.getLogger(__name__)

# Flag para verificar se spaCy está disponível
SPACY_AVAILABLE = False
nlp = None

try:
    import spacy
    # Tenta carregar o modelo em português
    try:
        nlp = spacy.load("pt_core_news_sm")
        SPACY_AVAILABLE = True
        logger.info("Modelo spaCy pt_core_news_sm carregado com sucesso")
    except OSError:
        # Se não encontrar o modelo em português, tenta o inglês
        try:
            nlp = spacy.load("en_core_web_sm")
            SPACY_AVAILABLE = True
            logger.warning("Modelo pt_core_news_sm não encontrado. Usando en_core_web_sm")
        except OSError:
            logger.warning("Nenhum modelo spaCy encontrado. Usando processamento básico.")
except ImportError:
    logger.warning("spaCy não instalado. Usando processamento básico.")


# Stopwords em português (fallback se spaCy não estiver disponível)
PORTUGUESE_STOPWORDS = {
    "a", "ao", "aos", "aquela", "aquelas", "aquele", "aqueles", "aquilo",
    "as", "até", "com", "como", "da", "das", "de", "dela", "delas", "dele",
    "deles", "depois", "do", "dos", "e", "ela", "elas", "ele", "eles", "em",
    "entre", "era", "eram", "essa", "essas", "esse", "esses", "esta", "estas",
    "este", "estes", "eu", "foi", "foram", "há", "isso", "isto", "já", "lhe",
    "lhes", "lo", "mas", "me", "mesmo", "meu", "meus", "minha", "minhas",
    "muito", "na", "nas", "não", "nem", "no", "nos", "nossa", "nossas",
    "nosso", "nossos", "num", "numa", "o", "os", "ou", "para", "pela",
    "pelas", "pelo", "pelos", "por", "qual", "quando", "que", "quem", "se",
    "seja", "sem", "seu", "seus", "só", "sua", "suas", "também", "te", "tem",
    "temos", "tenho", "ter", "teu", "teus", "tu", "tua", "tuas", "um", "uma",
    "você", "vocês", "vos", "à", "às", "é"
}


def remove_punctuation(text: str) -> str:
    """
    Remove pontuação do texto.
    
    Args:
        text: Texto de entrada
        
    Returns:
        Texto sem pontuação
    """
    # Mantém espaços entre palavras ao remover pontuação
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    return text.translate(translator)


def remove_extra_whitespace(text: str) -> str:
    """
    Remove espaços em branco extras.
    
    Args:
        text: Texto de entrada
        
    Returns:
        Texto com espaços normalizados
    """
    return ' '.join(text.split())


def tokenize_basic(text: str) -> list[str]:
    """
    Tokenização básica por espaço.
    
    Args:
        text: Texto de entrada
        
    Returns:
        Lista de tokens
    """
    return text.split()


def remove_stopwords_basic(tokens: list[str]) -> list[str]:
    """
    Remove stopwords usando lista predefinida.
    
    Args:
        tokens: Lista de tokens
        
    Returns:
        Lista de tokens sem stopwords
    """
    return [token for token in tokens if token.lower() not in PORTUGUESE_STOPWORDS]


def lemmatize_with_spacy(text: str) -> str:
    """
    Lematiza texto usando spaCy.
    
    Args:
        text: Texto de entrada
        
    Returns:
        Texto lematizado
    """
    if not SPACY_AVAILABLE or nlp is None:
        return text
    
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(lemmas)


def preprocess_text(text: str, use_lemmatization: bool = True) -> str:
    """
    Função principal de pré-processamento NLP.
    
    Aplica as seguintes transformações:
    1. Lowercase
    2. Remoção de pontuação
    3. Remoção de stopwords
    4. Tokenização
    5. Lematização (se disponível)
    
    Args:
        text: Texto original do email
        use_lemmatization: Se True, aplica lematização (requer spaCy)
        
    Returns:
        Texto pré-processado
    """
    if not text or not text.strip():
        logger.warning("Texto vazio recebido para pré-processamento")
        return ""
    
    logger.debug(f"Iniciando pré-processamento. Tamanho original: {len(text)} caracteres")
    
    # 1. Lowercase
    processed = text.lower()
    
    # 2. Remoção de URLs e emails
    processed = re.sub(r'http\S+|www\S+|https\S+', '', processed)
    processed = re.sub(r'\S+@\S+', '', processed)
    
    # 3. Remoção de números (opcional, mantém contexto)
    # processed = re.sub(r'\d+', '', processed)
    
    # 4. Remoção de pontuação
    processed = remove_punctuation(processed)
    
    # 5. Remoção de espaços extras
    processed = remove_extra_whitespace(processed)
    
    if SPACY_AVAILABLE and use_lemmatization:
        # Usar spaCy para tokenização, stopwords e lematização
        processed = lemmatize_with_spacy(processed)
    else:
        # Processamento básico sem spaCy
        tokens = tokenize_basic(processed)
        tokens = remove_stopwords_basic(tokens)
        processed = ' '.join(tokens)
    
    # Limpeza final
    processed = remove_extra_whitespace(processed)
    
    logger.debug(f"Pré-processamento concluído. Tamanho final: {len(processed)} caracteres")
    
    return processed


def get_nlp_info() -> dict:
    """
    Retorna informações sobre o módulo NLP.
    
    Returns:
        Dicionário com informações do processamento NLP
    """
    return {
        "spacy_available": SPACY_AVAILABLE,
        "model": nlp.meta.get("name", "unknown") if nlp else None,
        "language": nlp.meta.get("lang", "unknown") if nlp else None,
        "fallback_stopwords_count": len(PORTUGUESE_STOPWORDS)
    }

