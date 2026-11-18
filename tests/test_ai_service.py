"""
Unit tests for AI Service provider resolution and fallbacks.
"""

import pytest
from ai.ai_service import AIService, PROVIDER_GEMINI, PROVIDER_OPENAI


def test_provider_detection_from_model():
    """Verify that models automatically map to the right provider."""
    assert AIService.detect_provider_from_model("gemini-1.5-flash") == PROVIDER_GEMINI
    assert AIService.detect_provider_from_model("gemini-2.0-flash") == PROVIDER_GEMINI
    assert AIService.detect_provider_from_model("gpt-4o") == PROVIDER_OPENAI
    assert AIService.detect_provider_from_model("gpt-4o-mini") == PROVIDER_OPENAI


def test_provider_and_model_resolution():
    """Verify default model assignment per provider."""
    service = AIService()
    
    # Defaults
    prov, model = service.resolve_provider_and_model(provider="gemini")
    assert prov == "gemini"
    assert "gemini" in model

    prov, model = service.resolve_provider_and_model(provider="openai")
    assert prov == "openai"
    assert "gpt" in model

    # Model inferred provider
    prov, model = service.resolve_provider_and_model(model="gpt-4o")
    assert prov == "openai"
    assert model == "gpt-4o"


def test_missing_key_informative_error():
    """Verify that missing API keys throw a clear actionable error."""
    service = AIService(gemini_api_key="", openai_api_key="")
    
    with pytest.raises(ValueError) as excinfo:
        service.get_gemini_client()
    assert "GEMINI_API_KEY" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        service.get_openai_client()
    assert "OPENAI_API_KEY" in str(excinfo.value)
