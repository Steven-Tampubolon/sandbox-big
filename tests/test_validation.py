"""Tes validasi pemetaan scoring terhadap episode ekstrem dan tier menengah.

Fixture ``episode_ekstrem.json`` adalah data ILUSTRASI, bukan data historis
nyata. Tes di berkas ini memvalidasi pemetaan Tabel A dan Tabel B pada modul
scoring terhadap nilai episode tersebut, bukan keakuratan data historis.
"""

import json
from pathlib import Path

from scoring.aqi_rules import score_aqi_impact
from scoring.uv_rules import label_uv_risk

FIXTUR_PATH = Path(__file__).parent / "fixtures" / "episode_ekstrem.json"


def test_validates_against_extreme_episode():
    """Episode ekstrem (AQI 320, UV 11.5) dipetakan ke label Kritis dengan skor 86.4."""
    # Fixture ini hanya ilustrasi: tes memvalidasi pemetaan tabel,
    # bukan data historis nyata.
    episode = json.loads(FIXTUR_PATH.read_text(encoding="utf-8"))
    assert episode["aqi"] == 320
    assert episode["uv_index"] == 11.5

    skor, label = score_aqi_impact(episode["aqi"])
    assert skor == 86.4
    assert label == "Kritis"

    _, label_uv = label_uv_risk(episode["uv_index"])
    assert label_uv == "Kritis"


def test_kejadian_tier_menengah_aqi_160():
    """Kejadian tier menengah (AQI 160) dipetakan ke label Tinggi dengan skor 57.8."""
    skor, label = score_aqi_impact(160)
    assert skor == 57.8
    assert label == "Tinggi"
