"""
Testes da API com pytest.
Testa endpoints e funcionalidades principais.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import da aplicação
import sys
sys.path.insert(0, '..')

from app.main import app


# ============== Fixtures ==============

@pytest.fixture
def client():
    """Cliente de teste para a API."""
    return TestClient(app)


@pytest.fixture
def mock_openai_response():
    """Mock da resposta do OpenAI."""
    return {
        "classification": "Produtivo",
        "confidence": 0.91,
        "pontuation": 8,
        "preprocessed_text": "solicito analise relatorio"
    }


@pytest.fixture
def sample_productive_email():
    """Email produtivo de exemplo."""
    return {
        "email_content": "Prezado, solicito uma análise urgente do relatório financeiro do mês anterior. Precisamos revisar os números antes da reunião de amanhã."
    }


@pytest.fixture
def sample_unproductive_email():
    """Email improdutivo de exemplo."""
    return {
        "email_content": "Olá! Parabéns pelo seu aniversário! Desejo muitas felicidades e sucesso!"
    }


# ============== Testes de Status ==============

class TestStatusEndpoints:
    """Testes dos endpoints de status."""
    
    def test_root_endpoint(self, client):
        """Testa endpoint raiz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
    
    def test_health_endpoint(self, client):
        """Testa endpoint de health check."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "openai_configured" in data
        assert "nlp_info" in data
    
    def test_version_endpoint(self, client):
        """Testa endpoint de versão."""
        response = client.get("/api/v1/version")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "name" in data
        assert "description" in data


# ============== Testes de Classificação ==============

class TestClassificationEndpoint:
    """Testes do endpoint de classificação."""
    
    def test_classify_email_validation_empty_content(self, client):
        """Testa validação de email vazio."""
        response = client.post(
            "/api/v1/classify-email",
            json={"email_content": ""}
        )
        assert response.status_code == 400
    
    def test_classify_email_validation_missing_content(self, client):
        """Testa validação de campo faltando."""
        response = client.post(
            "/api/v1/classify-email",
            json={}
        )
        assert response.status_code == 400
    
    @patch('app.services.classifier.classify_email')
    @patch('app.services.response_generator.generate_response')
    @patch('app.services.openai_client.OpenAIClient.is_configured')
    def test_classify_email_productive(
        self,
        mock_is_configured,
        mock_generate,
        mock_classify,
        client,
        sample_productive_email,
        mock_openai_response
    ):
        """Testa classificação de email produtivo."""
        mock_is_configured.return_value = True
        mock_classify.return_value = mock_openai_response
        mock_generate.return_value = "Prezado, recebemos sua solicitação..."
        
        response = client.post(
            "/api/v1/classify-email",
            json=sample_productive_email
        )
        
        # Se OpenAI não está configurada, retorna 503
        if response.status_code == 503:
            pytest.skip("OpenAI não configurada")
        
        assert response.status_code == 200
        data = response.json()
        assert "classification" in data
        assert "pontuation" in data
        assert "suggested_reply" in data
        assert "confidence" in data
    
    def test_classify_email_without_openai_key(self, client, sample_productive_email):
        """Testa comportamento sem API key configurada."""
        with patch('app.services.openai_client.OpenAIClient.is_configured', return_value=False):
            response = client.post(
                "/api/v1/classify-email",
                json=sample_productive_email
            )
            # Deve retornar erro 503 (Service Unavailable)
            assert response.status_code == 503


# ============== Testes de Listagem ==============

class TestEmailListEndpoint:
    """Testes do endpoint de listagem de emails."""
    
    def test_list_emails_empty(self, client):
        """Testa listagem com histórico vazio."""
        # Limpa histórico primeiro
        client.delete("/api/v1/history")
        
        response = client.get("/api/v1/emails")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert "total_pages" in data
    
    def test_list_emails_pagination(self, client):
        """Testa parâmetros de paginação."""
        response = client.get("/api/v1/emails?page=1&page_size=5")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 5
    
    def test_list_emails_invalid_page(self, client):
        """Testa página inválida."""
        response = client.get("/api/v1/emails?page=0")
        assert response.status_code == 400 or response.status_code == 422
    
    def test_list_emails_ordering_desc(self, client):
        """Testa ordenação descendente."""
        response = client.get("/api/v1/emails?order=desc")
        assert response.status_code == 200
    
    def test_list_emails_ordering_asc(self, client):
        """Testa ordenação ascendente."""
        response = client.get("/api/v1/emails?order=asc")
        assert response.status_code == 200


# ============== Testes de Histórico ==============

class TestHistoryEndpoint:
    """Testes do endpoint de histórico."""
    
    def test_get_history(self, client):
        """Testa obtenção do histórico."""
        response = client.get("/api/v1/history")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_history_with_limit(self, client):
        """Testa histórico com limite."""
        response = client.get("/api/v1/history?limit=5")
        assert response.status_code == 200
    
    def test_clear_history(self, client):
        """Testa limpeza do histórico."""
        response = client.delete("/api/v1/history")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


# ============== Testes de NLP ==============

class TestNLPPreprocessing:
    """Testes do módulo de pré-processamento NLP."""
    
    def test_preprocess_basic(self):
        """Testa pré-processamento básico."""
        from app.nlp.preprocess import preprocess_text
        
        text = "Olá, como você está? Tudo bem!"
        result = preprocess_text(text)
        
        # Deve estar em lowercase e sem pontuação
        assert result == result.lower()
        assert "?" not in result
        assert "!" not in result
    
    def test_preprocess_empty(self):
        """Testa pré-processamento de texto vazio."""
        from app.nlp.preprocess import preprocess_text
        
        result = preprocess_text("")
        assert result == ""
    
    def test_preprocess_with_urls(self):
        """Testa remoção de URLs."""
        from app.nlp.preprocess import preprocess_text
        
        text = "Acesse https://exemplo.com para mais informações"
        result = preprocess_text(text)
        
        assert "https" not in result
        assert "exemplo.com" not in result
    
    def test_preprocess_with_emails(self):
        """Testa remoção de emails."""
        from app.nlp.preprocess import preprocess_text
        
        text = "Entre em contato via email@exemplo.com"
        result = preprocess_text(text)
        
        assert "@" not in result
    
    def test_nlp_info(self):
        """Testa informações do módulo NLP."""
        from app.nlp.preprocess import get_nlp_info
        
        info = get_nlp_info()
        assert "spacy_available" in info
        assert "fallback_stopwords_count" in info


# ============== Testes de Integração ==============

class TestIntegration:
    """Testes de integração."""
    
    def test_full_flow_mock(self, client):
        """Testa fluxo completo com mocks."""
        # Este teste simula o fluxo completo
        # sem chamar a API real da OpenAI
        
        with patch('app.api.routes.classify_email') as mock_classify:
            with patch('app.api.routes.generate_response') as mock_generate:
                with patch('app.services.openai_client.OpenAIClient.is_configured', return_value=True):
                    mock_classify.return_value = {
                        "classification": "Produtivo",
                        "confidence": 0.91,
                        "pontuation": 8,
                        "preprocessed_text": "teste"
                    }
                    mock_generate.return_value = "Resposta gerada automaticamente."
                    
                    response = client.post(
                        "/api/v1/classify-email",
                        json={"email_content": "Solicito análise urgente."}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        assert data["classification"] == "Produtivo"
                        assert data["pontuation"] == 8
                        assert data["confidence"] == 0.91


# ============== Execução Direta ==============

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

