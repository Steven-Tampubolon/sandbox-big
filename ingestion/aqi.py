"""Modul pengambilan data AQI dari sumber eksternal melalui fetcher."""


from ingestion.errors import IngestionError


def fetch_aqi(fetcher):
    """Ambil data AQI saat ini dan prakiraannya melalui fetcher yang diberikan.

    ``fetcher()`` mengembalikan dict berbentuk seperti ``aqi_response.json``.
    Mengembalikan ``{"aqi": int, "aqi_forecast": [{"time": str, "aqi": int}, ...]}``.
    Melempar ``IngestionError("AQI tidak tersedia")`` bila ``fetcher`` melempar
    ``TimeoutError``/``ConnectionError`` atau data tidak punya kunci yang dibutuhkan.
    """
    try:
        data = fetcher()
    except (TimeoutError, ConnectionError) as exc:
        raise IngestionError("AQI tidak tersedia") from exc

    try:
        hasil = {
            "aqi": data["current"]["aqi"],
            "aqi_forecast": [
                {"time": titik["time"], "aqi": titik["aqi"]}
                for titik in data["forecast"]
            ],
        }
    except (KeyError, TypeError) as exc:
        raise IngestionError("AQI tidak tersedia") from exc

    return hasil
