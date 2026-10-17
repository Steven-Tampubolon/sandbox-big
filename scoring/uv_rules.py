"""Modul pemetaan indeks UV ke kategori dan label risiko kulit sesuai Tabel B."""


def label_uv_risk(uv):
    """Kembalikan tuple (kategori, label) risiko kulit untuk indeks UV.

    Mengikuti Tabel B: batas bawah tier inklusif dan batas atas eksklusif
    (misalnya UV 3 masuk ke U1, bukan U0). UV negatif melempar ``ValueError``.
    """
    if uv < 0:
        raise ValueError("Indeks UV tidak boleh negatif")
    if uv < 3:
        return ("U0 Rendah", "Rendah")
    if uv < 6:
        return ("U1 Sedang", "Rendah–Sedang")
    if uv < 8:
        return ("U2 Tinggi", "Sedang")
    if uv < 11:
        return ("U3 Sangat tinggi", "Tinggi")
    return ("U4 Ekstrem", "Kritis")
