"""Modul pengambilan data UV dari sumber eksternal melalui fetcher."""


from ingestion.errors import IngestionError


def fetch_uv(fetcher):
    """Ambil data UV saat ini melalui fetcher yang diberikan.

    ``fetcher()`` mengembalikan dict berbentuk seperti ``uv_response.json``.
    Mengembalikan ``{"uv_index": float, "uv_time": str}``.
    Melempar ``IngestionError("UV tidak tersedia")`` bila ``fetcher`` melempar
    ``TimeoutError``/``ConnectionError`` atau data tidak punya kunci yang dibutuhkan.
    """
    try:
        data = fetcher()
    except (TimeoutError, ConnectionError) as exc:
        raise IngestionError("UV tidak tersedia") from exc

    try:
        hasil = {
            "uv_index": data["uv"]["index"],
            "uv_time": data["uv"]["time"],
        }
    except (KeyError, TypeError) as exc:
        raise IngestionError("UV tidak tersedia") from exc

    return hasil
