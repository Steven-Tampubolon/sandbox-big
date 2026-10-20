"""Tes pemetaan AQI ke skor dampak kesehatan dan label risiko sesuai Tabel A."""

import pytest

from scoring.aqi_rules import score_aqi_impact


@pytest.mark.parametrize(
    ("aqi", "skor", "label"),
    [
        pytest.param(0, 0.0, "Rendah", id="acuan-0"),
        pytest.param(25, 10.0, "Rendah", id="acuan-25"),
        pytest.param(50, 20.0, "Rendah", id="acuan-50"),
        pytest.param(51, 20.0, "Rendah–Sedang", id="acuan-51"),
        pytest.param(75, 29.8, "Rendah–Sedang", id="acuan-75"),
        pytest.param(100, 40.0, "Rendah–Sedang", id="acuan-100"),
        pytest.param(101, 40.0, "Sedang", id="acuan-101"),
        pytest.param(125, 47.3, "Sedang", id="acuan-125"),
        pytest.param(150, 55.0, "Sedang", id="acuan-150"),
        pytest.param(151, 55.0, "Tinggi", id="acuan-151"),
        pytest.param(175, 62.3, "Tinggi", id="acuan-175"),
        pytest.param(200, 70.0, "Tinggi", id="acuan-200"),
        pytest.param(201, 70.0, "Tinggi", id="acuan-201"),
        pytest.param(250, 77.4, "Tinggi", id="acuan-250"),
        pytest.param(300, 85.0, "Tinggi", id="acuan-300"),
        pytest.param(301, 85.0, "Kritis", id="acuan-301"),
        pytest.param(400, 92.5, "Kritis", id="acuan-400"),
        pytest.param(500, 100.0, "Kritis", id="acuan-500"),
        pytest.param(800, 100.0, "Kritis", id="acuan-800"),
    ],
)
def test_nilai_acuan_menghasilkan_skor_dan_label_persis(aqi, skor, label):
    """Seluruh nilai acuan di Keputusan teknis menghasilkan skor dan label persis."""
    assert score_aqi_impact(aqi) == (skor, label)


@pytest.mark.parametrize(
    ("aqi", "label"),
    [
        pytest.param(0, "Rendah", id="A0-batas-bawah"),
        pytest.param(50, "Rendah", id="A0-batas-atas"),
        pytest.param(51, "Rendah–Sedang", id="A1-batas-bawah"),
        pytest.param(100, "Rendah–Sedang", id="A1-batas-atas"),
        pytest.param(101, "Sedang", id="A2-batas-bawah"),
        pytest.param(150, "Sedang", id="A2-batas-atas"),
        pytest.param(151, "Tinggi", id="A3-batas-bawah"),
        pytest.param(200, "Tinggi", id="A3-batas-atas"),
        pytest.param(201, "Tinggi", id="A4-batas-bawah"),
        pytest.param(300, "Tinggi", id="A4-batas-atas"),
        pytest.param(301, "Kritis", id="A5-batas-bawah"),
        pytest.param(500, "Kritis", id="A5-batas-atas"),
    ],
)
def test_label_tier_a0_sampai_a5_pada_batasnya(aqi, label):
    """Label tiap tier A0–A5 benar pada batas bawah dan batas atas tier itu."""
    assert score_aqi_impact(aqi)[1] == label


def test_aqi_pecahan_dibulatkan_ke_bawah():
    """AQI 50.9 dihitung sebagai 50 (tier A0, skor 20.0, label Rendah)."""
    assert score_aqi_impact(50.9) == score_aqi_impact(50)
    assert score_aqi_impact(50.9) == (20.0, "Rendah")


@pytest.mark.parametrize(
    "aqi",
    [
        pytest.param(-0.5, id="negatif-pecahan"),
        pytest.param(-1, id="negatif-bulat"),
    ],
)
def test_aqi_negatif_melempar_value_error(aqi):
    """AQI negatif melempar ValueError."""
    with pytest.raises(ValueError):
        score_aqi_impact(aqi)
