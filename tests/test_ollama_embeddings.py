"""Tests for Ollama embedding provider."""

import pytest
from unittest.mock import MagicMock, patch

from mempalace.embeddings import OllamaEmbeddingFunction


class TestOllamaEmbeddingFunction:
    """OllamaEmbeddingFunction unit tests."""

    def test_init_default_values(self):
        """Test default initialization values."""
        ef = OllamaEmbeddingFunction()
        assert ef.model == "qwen3-embedding"
        assert ef.base_url == "http://localhost:11434"
        assert ef.timeout == 30.0

    def test_init_custom_values(self):
        """Test custom initialization values."""
        ef = OllamaEmbeddingFunction(
            model="nomic-embed-text",
            base_url="http://192.168.1.100:11434",
            timeout=60.0,
        )
        assert ef.model == "nomic-embed-text"
        assert ef.base_url == "http://192.168.1.100:11434"
        assert ef.timeout == 60.0

    def test_init_env_url(self, monkeypatch):
        """Test base_url from environment variable."""
        monkeypatch.setenv("OLLAMA_BASE_URL", "http://custom:8080")
        ef = OllamaEmbeddingFunction()
        assert ef.base_url == "http://custom:8080"

    def test_call_single_string(self):
        """Test embedding generation with single string."""
        ef = OllamaEmbeddingFunction()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "embeddings": [[0.1, 0.2, 0.3, 0.4]]
        }

        with patch.object(ef._session, "post", return_value=mock_response):
            result = ef("hello world")

        assert len(result) == 1
        assert result[0] == [0.1, 0.2, 0.3, 0.4]

    def test_call_multiple_strings(self):
        """Test embedding generation with multiple strings."""
        ef = OllamaEmbeddingFunction()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "embeddings": [[0.1, 0.2], [0.3, 0.4]]
        }

        with patch.object(ef._session, "post", return_value=mock_response):
            result = ef(["text one", "text two"])

        assert len(result) == 2
        assert result[0] == [0.1, 0.2]
        assert result[1] == [0.3, 0.4]

    def test_call_empty_list(self):
        """Test embedding generation with empty list returns empty."""
        ef = OllamaEmbeddingFunction()
        result = ef([])
        assert result == []

    def test_call_api_error(self):
        """Test that API errors are raised properly."""
        import requests

        ef = OllamaEmbeddingFunction()

        with patch.object(ef._session, "post", side_effect=requests.RequestException("Connection refused")):
            with pytest.raises(requests.RequestException, match="Ollama embedding request failed"):
                ef("hello")

    def test_call_invalid_response_format(self):
        """Test that invalid response format raises ValueError."""
        ef = OllamaEmbeddingFunction()
        mock_response = MagicMock()
        mock_response.json.return_value = {"invalid": "format"}

        with patch.object(ef._session, "post", return_value=mock_response):
            with pytest.raises(ValueError, match="Unexpected Ollama response format"):
                ef("hello")

    def test_call_mismatched_embeddings_count(self):
        """Test that mismatched embeddings count raises ValueError."""
        ef = OllamaEmbeddingFunction()
        mock_response = MagicMock()
        # Response has 1 embedding but we sent 2 texts
        mock_response.json.return_value = {
            "embeddings": [[0.1, 0.2]]
        }

        with patch.object(ef._session, "post", return_value=mock_response):
            with pytest.raises(ValueError, match="Unexpected Ollama response format"):
                ef(["text one", "text two"])

    def test_repr(self):
        """Test string representation."""
        ef = OllamaEmbeddingFunction(model="test-model")
        repr_str = repr(ef)
        assert "OllamaEmbeddingFunction" in repr_str
        assert "test-model" in repr_str


class TestOllamaIntegration:
    """Integration tests for Ollama embedding with config."""

    def test_backend_creation_with_ollama_config(self, tmp_path):
        """Test that backend correctly uses Ollama when configured."""
        from mempalace.config import MempalaceConfig

        # Create config with ollama provider
        config_dir = tmp_path / ".mempalace"
        config_dir.mkdir()
        config_file = config_dir / "config.json"
        config_file.write_text(
            '{"embedding_provider": "ollama", "ollama_model": "test-model", "ollama_base_url": "http://test:11434"}'
        )

        # Create a fresh config instance pointing to the temp dir
        config = MempalaceConfig(config_dir=str(config_dir))

        # Verify config values
        assert config.embedding_provider == "ollama"
        assert config.ollama_model == "test-model"
        assert config.ollama_base_url == "http://test:11434"
