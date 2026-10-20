"""Modul pemetaan AQI ke skor dampak kesehatan dan label risiko sesuai Tabel A."""

import math

# Batas AQI dan rentang skor tiap tier sesuai Tabel A:
# (batas_bawah_aqi, batas_atas_aqi, skor_bawah, skor_atas, label)
_BATAS_TIER = [
    (0, 50, 0.0, 20.0, "Rendah"),
    (51, 100, 20.0, 40.0, "Rendah–Sedang"),
    (101, 150, 40.0, 55.0, "Sedang"),
    (151, 200, 55.0, 70.0, "Tinggi"),
    (201, 300, 70.0, 85.0, "Tinggi"),
    (301, 500, 85.0, 100.0, "Kritis"),
]


def score_aqi_impact(aqi):
    """Kembalikan tuple (skor, label) dampak kesehatan untuk nilai AQI.

    AQI dibulatkan ke bawah untuk menentukan tier (50.9 dihitung 50) dan
    skor dihitung dengan interpolasi linear di dalam rentang tier, lalu
    dibulatkan ke satu desimal. AQI negatif melempar ``ValueError``;
    AQI di atas 500 diberi skor 100.0.
    """
    if aqi < 0:
        raise ValueError("AQI tidak boleh negatif")

    aqi_bulat = math.floor(aqi)
    if aqi_bulat > 500:
        return (100.0, "Kritis")

    for batas_bawah, batas_atas, skor_bawah, skor_atas, label in _BATAS_TIER:
        if aqi_bulat <= batas_atas:
            posisi = (aqi_bulat - batas_bawah) / (batas_atas - batas_bawah)
            skor = round(skor_bawah + posisi * (skor_atas - skor_bawah), 1)
            return (skor, label)
