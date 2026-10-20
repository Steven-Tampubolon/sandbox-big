import os
import json

SYSTEM_PROMPT = "Kamu menerjemahkan data kualitas udara menjadi saran singkat untuk {role}. Jawab HANYA dengan JSON berisi kunci: ringkasan (string), tingkat_risiko (string), angka (objek dengan aqi dan skor persis seperti input). Jangan mengubah angka."

class ValidationError(Exception):
    """Kesalahan validasi hasil terjemahan AI."""
    pass

def get_api_key():
    """Membaca LLM_API_KEY dari lingkungan."""
    key = os.environ.get("LLM_API_KEY")
    if not key:
        raise RuntimeError("LLM_API_KEY tidak ditemukan di lingkungan")
    return key

def call_translation_layer(role, data, client):
    """
    Menerjemahkan data scoring menjadi saran teks menggunakan LLM client.
    
    Args:
        role (str): Peran pengguna (hanya 'pelari').
        data (dict): Berisi 'aqi' dan 'skor'.
        client (callable): Fungsi client LLM.
        
    Returns:
        dict: Hasil terjemahan ter-parse.
    """
    if role != "pelari":
        raise ValueError("Role tidak didukung")

    system_prompt = SYSTEM_PROMPT.format(role=role)
    user_prompt = json.dumps(data)

    for attempt in range(3):
        try:
            response_text = client(system_prompt, user_prompt)
            result = json.loads(response_text)
            
            # Validasi struktur dan angka
            if (
                "ringkasan" in result and 
                "tingkat_risiko" in result and 
                "angka" in result and 
                result["angka"].get("aqi") == data["aqi"] and 
                result["angka"].get("skor") == data["skor"]
            ):
                return result
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
            
    raise ValidationError("Gagal mendapatkan terjemahan valid setelah 3 percobaan")
