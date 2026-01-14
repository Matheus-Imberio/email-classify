"""
Testes do módulo NLP.
Testa funções de pré-processamento de texto.
"""

import pytest
from app.nlp.preprocess import (
    preprocess_text,
    remove_punctuation,
    remove_extra_whitespace,
    tokenize_basic,
    remove_stopwords_basic,
    get_nlp_info,
    PORTUGUESE_STOPWORDS
)


class TestRemovePunctuation:
    """Testes da remoção de pontuação."""
    
    def test_basic_punctuation(self):
        """Testa remoção de pontuação básica."""
        text = "Olá, mundo! Como vai?"
        result = remove_punctuation(text)
        assert "," not in result
        assert "!" not in result
        assert "?" not in result
    
    def test_multiple_punctuation(self):
        """Testa múltiplas pontuações."""
        text = "Teste...com...reticências!!!"
        result = remove_punctuation(text)
        assert "." not in result
        assert "!" not in result
    
    def test_empty_string(self):
        """Testa string vazia."""
        result = remove_punctuation("")
        assert result == ""


class TestRemoveExtraWhitespace:
    """Testes da remoção de espaços extras."""
    
    def test_multiple_spaces(self):
        """Testa múltiplos espaços."""
        text = "Olá    mundo"
        result = remove_extra_whitespace(text)
        assert result == "Olá mundo"
    
    def test_tabs_and_newlines(self):
        """Testa tabs e quebras de linha."""
        text = "Olá\t\tmundo\n\naqui"
        result = remove_extra_whitespace(text)
        assert result == "Olá mundo aqui"
    
    def test_leading_trailing_spaces(self):
        """Testa espaços no início e fim."""
        text = "   Olá mundo   "
        result = remove_extra_whitespace(text)
        assert result == "Olá mundo"


class TestTokenizeBasic:
    """Testes da tokenização básica."""
    
    def test_simple_sentence(self):
        """Testa frase simples."""
        text = "Olá mundo aqui"
        tokens = tokenize_basic(text)
        assert tokens == ["Olá", "mundo", "aqui"]
    
    def test_empty_string(self):
        """Testa string vazia."""
        tokens = tokenize_basic("")
        assert tokens == [""]


class TestRemoveStopwordsBasic:
    """Testes da remoção de stopwords."""
    
    def test_remove_common_stopwords(self):
        """Testa remoção de stopwords comuns."""
        tokens = ["olá", "o", "mundo", "e", "a", "vida"]
        result = remove_stopwords_basic(tokens)
        assert "o" not in result
        assert "e" not in result
        assert "a" not in result
        assert "olá" in result
        assert "mundo" in result
        assert "vida" in result
    
    def test_empty_list(self):
        """Testa lista vazia."""
        result = remove_stopwords_basic([])
        assert result == []
    
    def test_all_stopwords(self):
        """Testa lista só com stopwords."""
        tokens = ["o", "a", "e", "de", "para"]
        result = remove_stopwords_basic(tokens)
        assert len(result) == 0


class TestPreprocessText:
    """Testes da função principal de pré-processamento."""
    
    def test_full_preprocessing(self):
        """Testa pré-processamento completo."""
        text = "Olá, MUNDO! Como você está?"
        result = preprocess_text(text, use_lemmatization=False)
        
        # Deve estar em lowercase
        assert result == result.lower()
        # Deve estar sem pontuação
        assert "," not in result
        assert "!" not in result
        assert "?" not in result
    
    def test_empty_text(self):
        """Testa texto vazio."""
        result = preprocess_text("")
        assert result == ""
    
    def test_whitespace_only(self):
        """Testa texto só com espaços."""
        result = preprocess_text("   ")
        assert result == ""
    
    def test_url_removal(self):
        """Testa remoção de URLs."""
        text = "Visite https://www.exemplo.com para mais informações"
        result = preprocess_text(text, use_lemmatization=False)
        assert "https" not in result
        assert "www" not in result
        assert "exemplo.com" not in result
    
    def test_email_removal(self):
        """Testa remoção de emails."""
        text = "Envie para contato@empresa.com.br"
        result = preprocess_text(text, use_lemmatization=False)
        assert "@" not in result
    
    def test_preserves_meaningful_words(self):
        """Testa que palavras significativas são preservadas."""
        text = "Solicito análise do relatório financeiro"
        result = preprocess_text(text, use_lemmatization=False)
        # Palavras importantes devem ser preservadas
        assert "solicito" in result or "analise" in result or "relatorio" in result


class TestPortugueseStopwords:
    """Testes da lista de stopwords."""
    
    def test_common_stopwords_present(self):
        """Verifica se stopwords comuns estão na lista."""
        common = ["de", "a", "o", "que", "e", "para", "com"]
        for word in common:
            assert word in PORTUGUESE_STOPWORDS
    
    def test_not_contains_meaningful_words(self):
        """Verifica que palavras significativas não estão na lista."""
        meaningful = ["relatório", "análise", "solicito", "urgente"]
        for word in meaningful:
            assert word not in PORTUGUESE_STOPWORDS


class TestGetNLPInfo:
    """Testes da função de informações do NLP."""
    
    def test_returns_dict(self):
        """Verifica que retorna dicionário."""
        info = get_nlp_info()
        assert isinstance(info, dict)
    
    def test_contains_required_keys(self):
        """Verifica chaves obrigatórias."""
        info = get_nlp_info()
        assert "spacy_available" in info
        assert "fallback_stopwords_count" in info
    
    def test_stopwords_count(self):
        """Verifica contagem de stopwords."""
        info = get_nlp_info()
        assert info["fallback_stopwords_count"] == len(PORTUGUESE_STOPWORDS)
        assert info["fallback_stopwords_count"] > 0


# ============== Execução Direta ==============

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

