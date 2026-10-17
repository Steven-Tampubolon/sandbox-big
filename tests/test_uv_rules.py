"""Tes pemetaan indeks UV ke kategori dan label risiko kulit sesuai Tabel B."""

import pytest

from scoring.uv_rules import label_uv_risk


@pytest.mark.parametrize(
    ("uv", "kategori", "label"),
    [
        pytest.param(0, "U0 Rendah", "Rendah", id="U0-batas-bawah-0"),
        pytest.param(2.9, "U0 Rendah", "Rendah", id="U0-batas-atas-2.9"),
        pytest.param(3, "U1 Sedang", "Rendah–Sedang", id="U1-batas-bawah-3"),
        pytest.param(5.9, "U1 Sedang", "Rendah–Sedang", id="U1-batas-atas-5.9"),
        pytest.param(6, "U2 Tinggi", "Sedang", id="U2-batas-bawah-6"),
        pytest.param(7.9, "U2 Tinggi", "Sedang", id="U2-batas-atas-7.9"),
        pytest.param(8, "U3 Sangat tinggi", "Tinggi", id="U3-batas-bawah-8"),
        pytest.param(10.9, "U3 Sangat tinggi", "Tinggi", id="U3-batas-atas-10.9"),
        pytest.param(11, "U4 Ekstrem", "Kritis", id="U4-batas-bawah-11"),
        pytest.param(15, "U4 Ekstrem", "Kritis", id="U4-contoh-tinggi-15"),
    ],
)
def test_batas_tier_u0_sampai_u4_sesuai_tabel_b(uv, kategori, label):
    """Nilai batas tiap tier U0–U4 dipetakan ke kategori dan label Tabel B."""
    assert label_uv_risk(uv) == (kategori, label)


@pytest.mark.parametrize(
    "uv",
    [
        pytest.param(-0.5, id="negatif-pecahan"),
        pytest.param(-3, id="negatif-bulat"),
    ],
)
def test_uv_negatif_melempar_value_error(uv):
    """Indeks UV negatif melempar ValueError."""
    with pytest.raises(ValueError):
        label_uv_risk(uv)
