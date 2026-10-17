"""Tes untuk modul ingestion AQI (fetch_aqi) tanpa panggilan jaringan."""

import json
from pathlib import Path

import pytest

from ingestion.aqi import fetch_aqi
from ingestion.errors import IngestionError

FIXTURE_AQI = Path(__file__).parent / "fixtures" / "aqi_response.json"


def muat_fixture_aqi():
    """Muat isi fixture aqi_response.json sebagai dict."""
    return json.loads(FIXTURE_AQI.read_text(encoding="utf-8"))


def test_sukses_dari_fixture():
    """fetch_aqi mengembalikan AQI 87 dan dua titik prakiraan (95 dan 120) dari fixture."""
    hasil = fetch_aqi(muat_fixture_aqi)

    assert hasil == {
        "aqi": 87,
        "aqi_forecast": [
            {"time": "2026-10-20T06:00:00Z", "aqi": 95},
            {"time": "2026-10-21T06:00:00Z", "aqi": 120},
        ],
    }


def test_timeout_dari_fetcher_dibungkus_ingestion_error():
    """TimeoutError dari fetcher dibungkus menjadi IngestionError."""

    def fetcher_timeout():
        raise TimeoutError("waktu habis")

    with pytest.raises(IngestionError, match="AQI tidak tersedia"):
        fetch_aqi(fetcher_timeout)


def test_koneksi_gagal_dibungkus_ingestion_error():
    """ConnectionError dari fetcher dibungkus menjadi IngestionError."""

    def fetcher_gagal():
        raise ConnectionError("koneksi gagal")

    with pytest.raises(IngestionError, match="AQI tidak tersedia"):
        fetch_aqi(fetcher_gagal)


@pytest.mark.parametrize(
    "data",
    [
        pytest.param({"station": "JKT-01"}, id="kunci-current-hilang"),
        pytest.param(
            {"station": "JKT-01", "current": {"time": "2026-10-19T05:00:00Z"}},
            id="kunci-aqi-hilang",
        ),
        pytest.param({"current": {"aqi": 87}}, id="kunci-forecast-hilang"),
        pytest.param(
            {"current": {"aqi": 87}, "forecast": [{"time": "2026-10-20T06:00:00Z"}]},
            id="kunci-aqi-prakiraan-hilang",
        ),
    ],
)
def test_data_rusak_kunci_hilang_dibungkus_ingestion_error(data):
    """Data tanpa kunci yang dibutuhkan melempar IngestionError."""
    with pytest.raises(IngestionError, match="AQI tidak tersedia"):
        fetch_aqi(lambda: data)
