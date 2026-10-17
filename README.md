# AirSafe Lite

AirSafe Lite mengubah data kualitas udara (AQI) dan indeks UV menjadi skor dampak dan label risiko yang mudah dipahami. Seluruh pengambilan data dilakukan lewat fungsi yang menerima `fetcher`, sehingga proyek ini dapat diuji sepenuhnya dengan fixture deterministik tanpa panggilan jaringan. Skor dan label dihitung dengan aturan tetap berbasis tabel tier, lalu diterjemahkan lapisan AI menjadi saran singkat yang bisa dijelaskan.
