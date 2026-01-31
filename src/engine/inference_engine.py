class InferenceEngine:

    def get_lik_sign_description(self, lik_codes: list) -> list:
        """
        Return list of dictionaries containing code and description for each detected LIK sign.
        """
        lik_code_list = {
            "wn-1": "Awan tampak turun ke bawah membentuk gumpalan 3 kali",
            "wn-2": "Awan bergumpal dalam beberapa kelompok yang tampak saling mendekat atau menyatu",
            "wn-3": "Kilat muncul di salah satu sisi langit ataupun saling berbalas antara dua sisi",
            "wn-4": "Gelombang laut berubah pola dari kecil dan sering hingga besar dan rapat",
            "wn-5": "Lumba-lumba mendekati perahu, seolah menggiring perahu",
            "wn-6": "Burung camar terbang tergesa sambil bersuara keras",
            "wn-7": "Pada masa peralihan angin barat ke angin timur",
            "wn-8": "Langit mendung namun tidak terlalu gelap",
            "wn-9": "Hujan atau langit tertutup awan tebal, saat angin timur",
            "wn-10": "Cuaca cerah tanpa awan, saat angin barat",
            "wn-11": "Suara dentuman terdengar 1 atau 7 kali",
            "wn-12": "Banyak bintang di malam hari berkelap kelip, saat angin barat",
            "wn-13": "Bintang tidak terlihat di malam hari, saat angin timur",
            "wn-14": "Bintang terlihat mendekati atau sejajar dengan bulan",
            "wn-15": "Kecoak berterbangan di dalam kapal",
            "wn-16": "Bulan terlihat di antara penjepit bintang Kalajengking",
            "wn-17": "Paus muncul ke permukaan laut dan mengibaskan ekornya",
            "wn-18": "Penyu naik ke permukaan laut dan mengeluarkan suara"
        }
        return [{"code": code.upper(), "description": lik_code_list[code.lower()]} 
                for code in lik_codes if code.lower() in lik_code_list]

    def predict(self, data: dict) -> dict:
        # 1. Konfigurasi Basis Aturan (Tipping Points)
        top_5_trusted = ['wn-1', 'wn-2', 'wn-3', 'wn-7', 'wn-8']
        
        detected_codes = [s.lower() for s in data.get('lik_codes', [])]
        features = data.get('features', {})
        
        # 2. Evaluasi Profil Risiko Perilaku (Behavior Rules)
        met_rules = []
        if features.get('level_of_interaction_with_disaster', 0) <= 2.50:
            met_rules.append("Pengalaman Interaksi dengan Bencana Rendah (<= 2.50)")
        if features.get('age', 0) >= 47.50:
            met_rules.append("Usia Senior (>= 47.50)")
        if features.get('usage_duration', 0) <= 16.50:
            met_rules.append("Durasi Penggunaan Tanda Alam Rendah (<= 16.50)")
        if features.get('frequency_of_usage', 0) <= 6.50:
            met_rules.append("Frekuensi Penggunaan Tanda Alam Rendah (<= 6.50)")
        if features.get('fishing_experience', 0) >= 6.50:
            met_rules.append("Pengalaman Melaut Tinggi (>= 6.50)")

        is_high_risk = len(met_rules) > 0

        # 3. Analisis Validitas Sinyal (Trust Index)
        trusted_detected = [s.upper() for s in detected_codes if s in top_5_trusted]
        has_trusted_sign = len(trusted_detected) > 0
        
        # 4. Penyusunan Deskripsi Objektif
        if is_high_risk:
            desc = f"User diklasifikasikan berisiko tinggi karena memenuhi aturan behavior: {', '.join(met_rules)}."
        else:
            desc = "User tidak memenuhi kriteria risiko tinggi pada profil demografis/behavior."

        if (len(detected_codes) >= 3):
            is_high_risk = True
            desc += " Harap berhati-hati, lebih dari 3 tanda alam terdeteksi."

        if has_trusted_sign:
            desc += f" Terdeteksi tanda alam dengan tingkat kepercayaan tinggi: {', '.join(trusted_detected)}."
        else:
            desc += " Tanda alam yang terdeteksi tidak termasuk dalam kategori peringkat tingkat kepercayaan utama."

        # 5. Final Output JSON
        return {
            "is_high_risk": is_high_risk,
            "description": desc,
            "detected_signs": self.get_lik_sign_description(detected_codes)
        }