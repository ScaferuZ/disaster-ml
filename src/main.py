from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .engine.inference_engine import InferenceEngine

app = FastAPI(title="Hybrid SHAP Model API", version="1.1")
engine = InferenceEngine()

class PredictionInput(BaseModel):
    lik_codes: list[str] = Field(..., description="Daftar kode tanda alam (contoh: ['wn-1', 'wn-3'])")
    beach_location: str = Field(..., description="Lokasi pantai (contoh: 'pantai_lampuuk')")

    class Config:
        json_schema_extra = {
            "example": {
                "lik_codes": ["wn-1", "wn-7"],
                "beach_location": "pantai_lampuuk"
            }
        }

@app.get("/")
def home():
    return {"message": "Sistem Peringatan Dini Nelayan (Hybrid SHAP) aktif."}

@app.post("/predict")
def predict_risk(input_data: PredictionInput):
    """
    Endpoint untuk mendapatkan analisis risiko perilaku dan validitas tanda alam.
    """
    lik_code_list = {"lik_codes": input_data.lik_codes}

    if input_data.beach_location.lower() == "pantai_lampuuk":
        features_for_engine = {
            "features": engine.pantai_lampuuk_characteristics_input
        }
        data_for_engine = lik_code_list | features_for_engine
    elif input_data.beach_location.lower() == "pantai_lhoknga": 
        features_for_engine = {
            "features": engine.pantai_lhoknga_characteristics_input
        }
        data_for_engine = lik_code_list | features_for_engine
    elif input_data.beach_location.lower() == "pantai_ulee_lheue":
        features_for_engine = {
            "features": engine.pantai_ulee_lheue_characteristics_input
        }
        data_for_engine = lik_code_list | features_for_engine
    elif input_data.beach_location.lower() == "pantai_depok":
        features_for_engine = {
            "features": engine.pantai_depok_characteristics_input
        }
        data_for_engine = lik_code_list | features_for_engine
    elif input_data.beach_location.lower() == "pantai_samas":
        features_for_engine = {
            "features": engine.pantai_samas_characteristics_input
        }
        data_for_engine = lik_code_list | features_for_engine
    else: 
        raise HTTPException(status_code=400, detail="Lokasi pantai tidak valid. Pilih salah satu: pantai_lampuuk, pantai_lhoknga, pantai_ulee_lheue, pantai_depok, pantai_samas.")
    
    try:
        result = engine.predict(data_for_engine)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))