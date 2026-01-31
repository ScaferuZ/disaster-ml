# Dokumentasi Skenario Pengujian API (Hybrid SHAP)
Gunakan kumpulan JSON di bawah ini untuk menguji endpoint /predict pada API. Seluruh skenario didasarkan pada ambang batas matematis (tipping points) yang diekstraksi dari analisis dan pemodelan rule based SHAP.

## Skenario 1: User High Risk & Tanda dalam Trust Index
Contoh Kondisi: User memiliki usia senior (>= 47.50) dan melaporkan tanda alam dengan validitas tinggi (WN-3).

Ekspektasi: is_user_high_risk: true dan tanda terdeteksi sebagai Trust Index tinggi.

```JSON
{
  "lik_codes": ["wn-3"],
  "level_of_interaction_with_disaster": 5.0,
  "age": 50.0,
  "usage_duration": 20.0,
  "min_frequency_of_usage": 15.0,
  "fishing_experience": 5.0
}
```

## Skenario 2: User High Risk & Tanda Tidak dalam Trust Index
Contoh Kondisi: User memiliki interaksi rendah dengan bencana (<= 2.50) dan melaporkan tanda alam umum (WN-5).

Ekspektasi: is_user_high_risk: true namun tanda alam bukan kategori Trust Index utama.

```JSON
{
  "lik_codes": ["wn-5"],
  "level_of_interaction_with_disaster": 2.0,
  "age": 30.0,
  "usage_duration": 20.0,
  "min_frequency_of_usage": 15.0,
  "fishing_experience": 5.0
}
```

## Skenario 3: User Safe & Tanda dalam Trust Index
Contoh Kondisi: Profil user tidak memenuhi satu pun kriteria risiko tinggi, melaporkan tanda validitas tinggi (WN-8).

Ekspektasi: is_user_high_risk: false dan tanda terdeteksi sebagai Trust Index tinggi.

```JSON
{
  "lik_codes": ["wn-8"],
  "level_of_interaction_with_disaster": 5.0,
  "age": 30.0,
  "usage_duration": 24.0,
  "min_frequency_of_usage": 12.0,
  "fishing_experience": 4.0
}
```

## Skenario 4: User Safe & Tanda Tidak dalam Trust Index
Contoh Kondisi: Profil user aman/waspada, melaporkan tanda alam umum (WN-6).

Ekspektasi: is_user_high_risk: false dan tanda alam bukan kategori utama.

```JSON
{
  "lik_codes": ["wn-6"],
  "level_of_interaction_with_disaster": 5.0,
  "age": 28.0,
  "usage_duration": 20.0,
  "min_frequency_of_usage": 10.0,
  "fishing_experience": 3.0
}
```

## Skenario 5: User High Risk & Terdeteksi > 3 Tanda (Termasuk Trust Index)
Contoh Kondisi: User memiliki durasi penggunaan rendah (<= 16.50) dan melaporkan banyak tanda alam (WN-1, WN-2, WN-3, WN-4).

Ekspektasi: is_user_high_risk: true dengan deskripsi tanda jamak (multimodal).

```JSON
{
  "lik_codes": ["wn-1", "wn-2", "wn-3", "wn-4"],
  "level_of_interaction_with_disaster": 5.0,
  "age": 35.0,
  "usage_duration": 10.0,
  "min_frequency_of_usage": 10.0,
  "fishing_experience": 5.0
}
```

## Skenario 6: User High Risk & Terdeteksi > 3 Tanda (Tidak Ada Trust Index)
Contoh Kondisi: User memiliki pengalaman melaut tinggi (>= 6.50) dan melaporkan banyak tanda alam umum (WN-4, WN-6, WN-9, WN-11).

Ekspektasi: is_user_high_risk: true namun tanpa deteksi tanda Trust Index tinggi.

```JSON
{
  "lik_codes": ["wn-4", "wn-6", "wn-9", "wn-11"],
  "level_of_interaction_with_disaster": 5.0,
  "age": 30.0,
  "usage_duration": 20.0,
  "min_frequency_of_usage": 10.0,
  "fishing_experience": 15.0
}
```

## Skenario 7: User Safe & Terdeteksi > 3 Tanda (Termasuk Trust Index)
Conntoh Kondisi: User proaktif, melaporkan banyak tanda alam (WN-2, WN-7, WN-12, WN-15).

Ekspektasi: is_user_high_risk: true tetapi memiliki urgensi dari sisi banyaknya tanda (multimodal).

```JSON
{
  "lik_codes": ["wn-2", "wn-7", "wn-12", "wn-15"],
  "level_of_interaction_with_disaster": 6.0,
  "age": 25.0,
  "usage_duration": 24.0,
  "min_frequency_of_usage": 15.0,
  "fishing_experience": 2.0
}
```

## Skenario 8: User Safe & Terdeteksi > 3 Tanda (Tidak Ada Trust Index)
Contoh Kondisi: User proaktif, melaporkan banyak tanda alam umum (WN-5, WN-10, WN-14, WN-17).

Ekspektasi: is_user_high_risk: true dan tidak ada tanda Trust Index tinggi terdeteksi.

```JSON
{
  "lik_codes": ["wn-5", "wn-10", "wn-14", "wn-17"],
  "level_of_interaction_with_disaster": 8.0,
  "age": 24.0,
  "usage_duration": 30.0,
  "min_frequency_of_usage": 20.0,
  "fishing_experience": 1.0
}
```

## Catatan Implementasi untuk Developer
**is_user_high_risk**: Jika bernilai true, pengembang disarankan untuk memicu Extra Warning pada antarmuka pengguna.

**Thresholding**: Semua parameter numerik menggunakan angka float untuk mengakomodasi titik balik matematis yang presisi dari model SHAP.

**Multimodal Detection**: Deteksi lebih dari 3 tanda alam (seperti skenario 5-8) secara teknis meningkatkan level bahaya meskipun profil user aman.