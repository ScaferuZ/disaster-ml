from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .engine.inference_engine import InferenceEngine

app = FastAPI(title="Hybrid SHAP Model API", version="1.0")
engine = InferenceEngine()

class PredictionInput(BaseModel):
    level_of_interaction: int = Field(..., ge=0, le=10, description="Skor interaksi (0-10)")
    age: int = Field(..., ge=0, description="Usia dalam tahun")
    fishing_experience: int = Field(..., ge=0, description="Pengalaman melaut dalam tahun")
    lik_codes: list[str] = Field(..., description="Daftar kode tanda alam (contoh: ['wn-1', 'wn-8'])")

    class Config:
        json_schema_extra = {
            "example": {
                "level_of_interaction": 0, # Threshold High Risk <= 1
                "age": 55,                 # Threshold High Risk >= 48
                "fishing_experience": 30,  # Threshold Overconfidence > 25
                "lik_codes": ["wn-1", "wn-8"]
            }
        }

@app.get("/")
def home():
    return {"message": "Sistem Peringatan Dini Nelayan (Hybrid SHAP) aktif."}

@app.post("/predict")
def predict_risk(input_data: PredictionInput):
    """
    Endpoint untuk mendapatkan pesan peringatan berdasarkan profil dan tanda alam.
    """
    data_for_engine = {
        "lik_codes": input_data.lik_codes,
        "features": {
            "level_of_interaction_with_disaster": input_data.level_of_interaction,
            "age": input_data.age,
            "fishing_experience": input_data.fishing_experience
        }
    }
    
    try:
        result = engine.predict(data_for_engine)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))