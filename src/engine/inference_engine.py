class InferenceEngine:

    def get_lik_sign_description(self, lik_codes: list) -> dict:
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
        lik_codes = [code.lower() for code in lik_codes]
        return {code: description for code, description in lik_code_list.items() if code in lik_codes}

    def predict(self, data: dict) -> dict:
        top_5_trusted = ['wn-3', 'wn-8', 'wn-2', 'wn-1', 'wn-7']
      
        detected_signs = [s.lower() for s in data.get('lik_codes', [])]
        features = data.get('features', {})

        sign_descriptions = self.get_lik_sign_description(detected_signs)
        signs_text = ", ".join(sign_descriptions.values()) if sign_descriptions else "tanda alam tertentu"
        
        has_trusted_sign = any(s in detected_signs for s in top_5_trusted)
        
        risk_score = 0
        proactive_score = 0

        # A. Level of Interaction (Bobot 3 - Rank #1 SHAP)
        interaction = features.get('level_of_interaction_with_disaster', 0)
        if interaction <= 1: risk_score += 3
        elif interaction >= 3: proactive_score += 3
        

        # B. Age (Bobot 2 - Rank #2 SHAP)
        age = features.get('age', 0)
        if age >= 48: risk_score += 2
        elif 25 <= age <= 47: proactive_score += 2

        # C. Fishing Experience (Bobot 1 - Rank #5 SHAP)
        exp = features.get('fishing_experience', 0)
        if exp > 25: risk_score += 1
        elif 10 <= exp <= 25: proactive_score += 1

        threshold = 4
        
        # A. Kasus Bias Khusus (Wn-7)
        if "wn-7" in detected_signs:
            return {
                "status": "Bias Alert",
                "message": "Peringatan: Tanda Wn-7 terdeteksi. Meskipun sering diabaikan, tanda ini memiliki akurasi Rank #5 dalam sistem kami.",
                "rule_id": "RULE_BIAS_WN7"
            }

        # B. High Risk + Tanda Valid (Gunakan seluruh Top 5)
        if risk_score >= threshold:
            if has_trusted_sign:
                return {
                    "status": "Urgent Warning",
                    "message": f"URGENT! {signs_text} terdeteksi. Tanda alam menunjukkan tingkat kepercayaan tinggi. Berdasarkan profil risiko Anda, mohon SEGERA mitigasi / waspada.",
                    "rule_id": "RULE_URGENT_HIGH_RISK"
                }
            return {
                "status": "Preventive Alert",
                "message": f"Waspada: {signs_text} terdeteksi. Profil Anda menunjukkan risiko tinggi. Tetap pantau kondisi meski tanda alam belum masuk kategori kritis.",
                "rule_id": "RULE_PREVENTIVE"
            }

        # C. Proaktif + Tanda Valid (Gunakan seluruh Top 5)
        if proactive_score >= threshold:
            if has_trusted_sign:
                return {
                    "status": "Confirmation",
                    "message": f"Konfirmasi: {signs_text} terdeteksi. Tanda yang dilaporan terverifikasi secara statistik. Lanjutkan prosedur mitigasi / waspada.",
                    "rule_id": "RULE_CONFIRM_PROACTIVE"
                }
            return {
                "status": "Monitoring",
                "message": f"Info: {signs_text} terdeteksi. Kondisi terpantau normal bagi nelayan proaktif. Tetap waspada secara mandiri.",
                "rule_id": "RULE_MONITOR_PROACTIVE"
            }

        return {
            "status": "General",
            "message": f"{signs_text} terdeteksi.Sistem memantau kondisi. Pastikan Anda memperhatikan perubahan tanda alam di sekitar pesisir.",
            "rule_id": "RULE_DEFAULT"
        }