import pytest
import os
from ai_layer.translator import call_translation_layer, get_api_key, ValidationError

def test_get_api_key_success(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    assert get_api_key() == "test-key"

def test_get_api_key_missing(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="LLM_API_KEY tidak ditemukan"):
        get_api_key()

def test_translator_success():
    data = {"aqi": 50, "skor": 20.0}
    def mock_client(sys, user):
        return '{"ringkasan": "Udara baik", "tingkat_risiko": "Rendah", "angka": {"aqi": 50, "skor": 20.0}}'
    
    result = call_translation_layer("pelari", data, mock_client)
    assert result["ringkasan"] == "Udara baik"
    assert result["angka"] == data

def test_translator_retry_then_success():
    data = {"aqi": 50, "skor": 20.0}
    calls = []
    def mock_client(sys, user):
        calls.append(1)
        if len(calls) == 1:
            return '{"ringkasan": "Salah", "tingkat_risiko": "Rendah", "angka": {"aqi": 99, "skor": 20.0}}'
        return '{"ringkasan": "Benar", "tingkat_risiko": "Rendah", "angka": {"aqi": 50, "skor": 20.0}}'
    
    result = call_translation_layer("pelari", data, mock_client)
    assert len(calls) == 2
    assert result["ringkasan"] == "Benar"

def test_translator_always_fails():
    data = {"aqi": 50, "skor": 20.0}
    calls = []
    def mock_client(sys, user):
        calls.append(1)
        return '{"ringkasan": "Salah", "tingkat_risiko": "Rendah", "angka": {"aqi": 99, "skor": 20.0}}'
    
    with pytest.raises(ValidationError):
        call_translation_layer("pelari", data, mock_client)
    assert len(calls) == 3

def test_translator_broken_json():
    data = {"aqi": 50, "skor": 20.0}
    calls = []
    def mock_client(sys, user):
        calls.append(1)
        return '{"ringkasan": "Broken' # Invalid JSON
    
    with pytest.raises(ValidationError):
        call_translation_layer("pelari", data, mock_client)
    assert len(calls) == 3

def test_translator_invalid_role():
    data = {"aqi": 50, "skor": 20.0}
    def mock_client(sys, user):
        return '{}'
    
    with pytest.raises(ValueError, match="Role tidak didukung"):
        call_translation_layer("pendaki", data, mock_client)
