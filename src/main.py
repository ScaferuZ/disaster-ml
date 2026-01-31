from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .engine.inference_engine import InferenceEngine

app = FastAPI(title="Hybrid SHAP Model API", version="1.1")
engine = InferenceEngine()

class PredictionInput(BaseModel):
    lik_codes: list[str] = Field(..., description="Daftar kode tanda alam (contoh: ['wn-1', 'wn-3'])")
    level_of_interaction_with_disaster: float = Field(..., ge=0, le=10, description="Skor interaksi (0-10)")
    age: float = Field(..., ge=0, description="Usia dalam tahun")
    usage_duration: float = Field(..., ge=0, description="Durasi penggunaan tanda alam dalam tahun")
    min_frequency_of_usage: float = Field(..., ge=0, description="Frekuensi penggunaan tanda alam dalam sebulan")
    fishing_experience: float = Field(..., ge=0, description="Pengalaman melaut dalam tahun")

    class Config:
        json_schema_extra = {
            "example": {
                "lik_codes": ["wn-1", "wn-7"],
                "level_of_interaction_with_disaster": 2.0,   # High Risk (<= 2.50)
                "age": 50.0,                                # High Risk (>= 47.50)
                "usage_duration": 10.0,                     # High Risk (<= 16.50)
                "min_frequency_of_usage": 5.0,              # High Risk (<= 6.50)
                "fishing_experience": 15.0                  # High Risk (>= 6.50)
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

    data_for_engine = {
        "lik_codes": input_data.lik_codes,
        "features": {
            "level_of_interaction_with_disaster": input_data.level_of_interaction_with_disaster,
            "age": input_data.age,
            "usage_duration": input_data.usage_duration,
            "frequency_of_usage": input_data.min_frequency_of_usage,
            "fishing_experience": input_data.fishing_experience
        }
    }
    
    try:
        result = engine.predict(data_for_engine)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))