from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .engine.inference_engine import InferenceEngine

app = FastAPI(title="Hybrid SHAP Model API", version="1.1")
engine = InferenceEngine()

class PredictionInput(BaseModel):
    beach_location: str = Field(..., description="Lokasi pantai (contoh: 'pantai_lampuuk')")
    lik_codes: list[str] = Field(..., description="Daftar kode tanda alam (contoh: ['wn-1', 'wn-3'])")
    is_active_warning: bool = Field(..., description="Apakah ada tanda alam yang sedang aktif aktif")
    active_warning: list[str] = Field(..., description="Daftar kode tanda alam yang sedang aktif(contoh: ['wn-1', 'wn-3'])")

    class Config:
        json_schema_extra = {
            "example": {
                "beach_location": "pantai_lampuuk",
                "lik_codes": ["wn-1", "wn-7"],
                "is_active_warning": True,
                "active_warning": ["wn-8"]
            }
        }

@app.get("/")
def home():
    return {"message": "Sistem Peringatan Dini Nelayan Berbasis Pengetahuan Lokal aktif."}

@app.post("/predict")
def predict_risk(input_data: PredictionInput):
    """
    Endpoint untuk mendapatkan analisis risiko perilaku dan validitas tanda alam.
    """
    system_input = {"lik_codes": input_data.lik_codes, "is_active_warning": input_data.is_active_warning, "active_warning": input_data.active_warning}

    if input_data.beach_location.lower() == "pantai_lampuuk":
        community_rules = {
            "rules": engine.pantai_lampuuk_rules
        }
        data_for_engine = system_input | community_rules
    elif input_data.beach_location.lower() == "pantai_lhoknga": 
        community_rules = {
            "rules": engine.pantai_lhoknga_rules
        }
        data_for_engine = system_input | community_rules
    elif input_data.beach_location.lower() == "pantai_ulee_lheue":
        community_rules = {
            "rules": engine.pantai_ulee_lheue_rules
        }
        data_for_engine = system_input | community_rules
    elif input_data.beach_location.lower() == "pantai_depok":
        community_rules = {
            "rules": engine.pantai_depok_rules
        }
        data_for_engine = system_input | community_rules
    elif input_data.beach_location.lower() == "pantai_samas":
        community_rules = {
            "rules": engine.pantai_samas_rules
        }
        data_for_engine = system_input | community_rules
    else: 
        raise HTTPException(status_code=400, detail="Lokasi pantai tidak valid. Pilih salah satu: pantai_lampuuk, pantai_lhoknga, pantai_ulee_lheue, pantai_depok, pantai_samas.")
    
    try:
        result = engine.predict(data_for_engine)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))