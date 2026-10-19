"""Modul perhitungan tingkat kepercayaan data berdasarkan jenis dan horizon prakiraan."""


def compute_confidence(data_type, horizon_hours):
    """Kembalikan tuple (tingkat, alasan) kepercayaan data.

    ``"realtime"`` selalu Tinggi. ``"forecast"`` dengan horizon ≤ 24 jam
    memberi Sedang, sedangkan lebih dari 24 jam memberi Rendah. Jenis
    data lain melempar ``ValueError``.
    """
    if data_type == "realtime":
        return (
            "Tinggi",
            "Data realtime diambil dari pengukuran terkini sehingga paling bisa diandalkan.",
        )
    if data_type == "forecast":
        if horizon_hours <= 24:
            return (
                "Sedang",
                "Prakiraan sampai 24 jam masih cukup andal, namun bisa bergeser dari kejadian nyata.",
            )
        return (
            "Rendah",
            "Prakiraan lebih dari 24 jam rawan meleset sehingga kepercayaannya rendah.",
        )
    raise ValueError(f"Jenis data tidak dikenal: {data_type!r}")
