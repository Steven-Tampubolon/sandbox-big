"""Modul untuk menggabungkan data kondisi lingkungan."""


from datetime import datetime, timezone
from ingestion.errors import IngestionError


def get_current_conditions(aqi_fetcher, uv_fetcher, now=None):
    """Gabungkan hasil AQI dan UV ke dalam satu skema output ingestion.

    Bila salah satu sumber gagal, melempar ``IngestionError``.
    """
    if now is None:
        now = lambda: datetime.now(timezone.utc)

    # Menggunakan fetcher yang sudah dibungkus fungsi fetch_aqi/fetch_uv
    # Namun berdasarkan spesifikasi Tugas 1, get_current_conditions menerima aqi_fetcher 
    # dan uv_fetcher. Jika ini adalah callable yang mengembalikan data mentah, 
    # kita harus memanggil fetch_aqi dan fetch_uv di sini.
    
    from ingestion.aqi import fetch_aqi
    from ingestion.uv import fetch_uv

    try:
        aqi_data = fetch_aqi(aqi_fetcher)
    except IngestionError:
        raise IngestionError("AQI tidak tersedia")

    try:
        uv_data = fetch_uv(uv_fetcher)
    except IngestionError:
        raise IngestionError("UV tidak tersedia")

    return {
        "aqi": aqi_data["aqi"],
        "aqi_forecast": aqi_data["aqi_forecast"],
        "uv_index": uv_data["uv_index"],
        "uv_time": uv_data["uv_time"],
        "fetched_at": now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
