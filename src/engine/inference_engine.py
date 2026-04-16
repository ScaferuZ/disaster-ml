import pandas as pd
from pathlib import Path

class InferenceEngine:

    def __init__(self):
        self.df_community = pd.read_csv(Path(__file__).parent / 'community_rule_categorization.csv')

        self.rules = {
            'level_of_interaction_with_disaster': 1.50,
            'frequency_of_usage': 5.50,
            'usage_duration': 17.50,
            'number_of_lik_combination': 1.50,
            'number_of_experience_with_disaster': 1.50,
        }

        self.pantai_lampuuk_rules = {
            'Overall Category': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lampuuk', 'Overall Category'].iloc[0],
            'Level of Interaction with Disaster Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lampuuk', 'Level of Interaction with Disaster Status'].iloc[0],
            'Frequency of Usage Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lampuuk', 'Frequency of Usage Status'].iloc[0],
            'Usage Duration Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lampuuk', 'Usage Duration Status'].iloc[0],
            'Number of Known LIK Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lampuuk', 'Number of LIK Combination Status'].iloc[0],
            'Number of Experience with Disaster Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lampuuk', 'Number of Experience with Disaster Status'].iloc[0],
        }    

        self.pantai_depok_rules = {
            'Overall Category': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai depok', 'Overall Category'].iloc[0],
            'Level of Interaction with Disaster Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lampuuk', 'Level of Interaction with Disaster Status'].iloc[0],
            'Frequency of Usage Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai depok', 'Frequency of Usage Status'].iloc[0],
            'Usage Duration Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai depok', 'Usage Duration Status'].iloc[0],
            'Number of Known LIK Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai depok', 'Number of LIK Combination Status'].iloc[0],
            'Number of Experience with Disaster Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai depok', 'Number of Experience with Disaster Status'].iloc[0],
        }    

        self.pantai_lhoknga_rules = {
            'Overall Category': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lhoknga', 'Overall Category'].iloc[0],
            'Level of Interaction with Disaster Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lhoknga', 'Level of Interaction with Disaster Status'].iloc[0],
            'Frequency of Usage Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lhoknga', 'Frequency of Usage Status'].iloc[0],
            'Usage Duration Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lhoknga', 'Usage Duration Status'].iloc[0],
            'Number of Known LIK Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lhoknga', 'Number of LIK Combination Status'].iloc[0],
            'Number of Experience with Disaster Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai lhoknga', 'Number of Experience with Disaster Status'].iloc[0],
        }    

        self.pantai_ulee_lheue_rules = {
            'Overall Category': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai ulee lheue', 'Overall Category'].iloc[0],
            'Level of Interaction with Disaster Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai ulee lheue', 'Level of Interaction with Disaster Status'].iloc[0],
            'Frequency of Usage Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai ulee lheue', 'Frequency of Usage Status'].iloc[0],
            'Usage Duration Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai ulee lheue', 'Usage Duration Status'].iloc[0],
            'Number of Known LIK Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai ulee lheue', 'Number of LIK Combination Status'].iloc[0],
            'Number of Experience with Disaster Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai ulee lheue', 'Number of Experience with Disaster Status'].iloc[0],
        }    

        self.pantai_samas_rules = {
            'Overall Category': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai samas', 'Overall Category'].iloc[0],
            'Level of Interaction with Disaster Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai samas', 'Level of Interaction with Disaster Status'].iloc[0],
            'Frequency of Usage Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai samas', 'Frequency of Usage Status'].iloc[0],
            'Usage Duration Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai samas', 'Usage Duration Status'].iloc[0],
            'Number of Known LIK Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai samas', 'Number of LIK Combination Status'].iloc[0],
            'Number of Experience with Disaster Status': self.df_community.loc[self.df_community['Mapped Beach'] == 'pantai samas', 'Number of Experience with Disaster Status'].iloc[0],
        }                                                       

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
        top_5_trusted = ['wn-2', 'wn-8', 'wn-1', 'wn-3', 'wn-7']
        
        detected_codes = [s.lower() for s in data.get('lik_codes', [])]
        rules = data.get('rules', {})
        
        # 2. Evaluasi Profil Risiko Perilaku (Behavior Rules)
        met_rules = []
        if rules.get('Level of Interaction with Disaster Status', 0) == 'Unsafe':
            met_rules.append("Pengalaman Interaksi dengan Bencana Rendah")
        if rules.get('Frequency of Usage Status', 0) == 'Unsafe':
            met_rules.append("Frekuensi Penggunaan Tanda Alam Rendah")
        if rules.get('Usage Duration Status', 0) == 'Unsafe':
            met_rules.append("Durasi Penggunaan Tanda Alam Rendah")
        if rules.get('Number of Known LIK Status', 0) == 'Unsafe':
            met_rules.append("Pengetahuan Tanda Alam Lokal Kurang")
        if rules.get('Number of Experience with Disaster Status', 0) == 'Unsafe':
            met_rules.append("Pengalaman Langsung dengan Bencana Rendah")

        community_risk_behaviour = rules['Overall Category']

        # 3. Analisis Validitas Sinyal (Trust Index)
        trusted_detected = [s.upper() for s in detected_codes if s in top_5_trusted]
        has_trusted_sign = len(trusted_detected) > 0
        
        # 4. Penyusunan Deskripsi Objektif
        if community_risk_behaviour == 'Unsafe':
            desc = f"Komunitas diklasifikasikan berisiko tinggi karena terdeteksi karakteristik: {', '.join(met_rules)}."
        else:
            desc = "Komunitas tidak memenuhi kriteria risiko tinggi pada profil demografis/behavior."

        if (len(detected_codes) >= 3):
            is_high_risk = True
            desc += " Harap berhati-hati, terdeteksi 3 atau lebih tanda alam pengetahuan lokal."

        if has_trusted_sign:
            desc += f" Terdeteksi tanda alam dengan tingkat kepercayaan tinggi: {', '.join(trusted_detected)}."
        else:
            desc += " Tanda alam yang terdeteksi tidak termasuk dalam kategori peringkat tingkat kepercayaan utama."

        # 5. Final Output JSON
        return {
            "community_risk_behaviour": community_risk_behaviour,
            "description": desc,
            "detected_signs": self.get_lik_sign_description(detected_codes)
        }