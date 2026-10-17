"""Tes smoke: memastikan ketiga paket proyek dapat di-import."""


def test_paket_ingestion_bisa_diimport():
    """Paket ingestion harus dapat di-import."""
    import ingestion


def test_paket_scoring_bisa_diimport():
    """Paket scoring harus dapat di-import."""
    import scoring


def test_paket_ai_layer_bisa_diimport():
    """Paket ai_layer harus dapat di-import."""
    import ai_layer
