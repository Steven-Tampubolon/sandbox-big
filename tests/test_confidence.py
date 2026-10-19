"""Tes perhitungan tingkat kepercayaan data berdasarkan jenis dan horizon prakiraan."""

import pytest

from scoring.confidence import compute_confidence


@pytest.mark.parametrize(
    "horizon_hours",
    [
        pytest.param(0, id="horizon-0"),
        pytest.param(6, id="horizon-6"),
        pytest.param(24, id="horizon-24"),
    ],
)
def test_data_realtime_berkepercayaan_tinggi(horizon_hours):
    """Data realtime selalu memberi tingkat Tinggi beserta alasannya."""
    tingkat, alasan = compute_confidence("realtime", horizon_hours)
    assert tingkat == "Tinggi"
    assert isinstance(alasan, str) and alasan


@pytest.mark.parametrize(
    "horizon_hours",
    [
        pytest.param(0, id="horizon-0"),
        pytest.param(1, id="horizon-1"),
        pytest.param(12, id="horizon-12"),
        pytest.param(24, id="horizon-24"),
    ],
)
def test_prakiraan_maksimal_24_jam_berkepercayaan_sedang(horizon_hours):
    """Prakiraan dengan horizon ≤ 24 jam memberi tingkat Sedang beserta alasannya."""
    tingkat, alasan = compute_confidence("forecast", horizon_hours)
    assert tingkat == "Sedang"
    assert isinstance(alasan, str) and alasan


@pytest.mark.parametrize(
    "horizon_hours",
    [
        pytest.param(25, id="horizon-25"),
        pytest.param(48, id="horizon-48"),
        pytest.param(72, id="horizon-72"),
    ],
)
def test_prakiraan_lebih_24_jam_berkepercayaan_rendah(horizon_hours):
    """Prakiraan dengan horizon > 24 jam memberi tingkat Rendah beserta alasannya."""
    tingkat, alasan = compute_confidence("forecast", horizon_hours)
    assert tingkat == "Rendah"
    assert isinstance(alasan, str) and alasan


@pytest.mark.parametrize(
    "data_type",
    [
        pytest.param("historis", id="jenis-historis"),
        pytest.param("", id="jenis-kosong"),
        pytest.param("REALTIME", id="jenis-huruf-besar"),
    ],
)
def test_jenis_data_tidak_dikenal_melempar_value_error(data_type):
    """Jenis data di luar realtime/forecast melempar ValueError."""
    with pytest.raises(ValueError):
        compute_confidence(data_type, 3)
