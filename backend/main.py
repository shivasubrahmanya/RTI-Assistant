from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
from typing import List, Optional
from utils import preprocess_text, get_pios_for_department, generate_rti_letter_gpt
from contextlib import asynccontextmanager
import traceback


# ===========================================================
# Global Variables
# ===========================================================
model_data = None
df = None


# ===========================================================
# Lifespan Event (Replaces @app.on_event)
# ===========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_data, df

    # Load model
    try:
        with open('model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        print("✅ Model loaded successfully.")
    except FileNotFoundError:
        print("⚠️ Warning: model.pkl not found. Please run train_model.py first.")
        model_data = None
    except Exception as e:
        print(f"❌ Error loading model.pkl: {e}")
        model_data = None

    # Load dataset
    try:
        df = pd.read_csv('PIO_Final_Synthetic_60000_fresh.csv')
        print(f"✅ Dataset loaded: {len(df)} rows.")
    except FileNotFoundError:
        print("❌ Error: Dataset file not found.")
        df = None
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        df = None

    yield
    print("🔻 Shutting down RTI Assistant API...")


# ===========================================================
# Initialize FastAPI App
# ===========================================================
app = FastAPI(title="RTI Assistant API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===========================================================
# Schemas
# ===========================================================
class PredictRequest(BaseModel):
    complaint: str
    keywords: Optional[str] = ""


class PredictResponse(BaseModel):
    predicted_department: str
    predicted_authority: str
    confidence_department: float
    confidence_authority: float
    pios: List[dict]


class GenerateLetterRequest(BaseModel):
    user_issue: str
    user_name: str
    user_address: str
    department: str
    pio_authority: Optional[str] = None
    authority_name: Optional[str] = None
    state: Optional[str] = None


class GenerateLetterResponse(BaseModel):
    letter: str


# ===========================================================
# Routes
# ===========================================================
@app.get("/")
async def root():
    return {
        "message": "RTI Assistant API is running",
        "version": "2.0",
        "endpoints": ["/predict", "/generate-letter", "/pios"]
    }


@app.post("/predict", response_model=PredictResponse)
async def predict_department_and_authority(request: PredictRequest):
    """Predict both Department and Authority from a user complaint"""
    if model_data is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Run train_model.py first.")
    if df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded.")

    try:
        # Prepare input text
        combined_text = (request.complaint + " " + (request.keywords or "")).strip().lower()
        cleaned_text = preprocess_text(combined_text)

        # Extract components
        vectorizer = model_data.get('vectorizer')
        model_dept = model_data.get('department_model')
        model_auth = model_data.get('authority_model')

        # Validate model objects
        if not vectorizer or not model_dept or not model_auth:
            raise HTTPException(status_code=500, detail="Model file is missing one or more trained components.")

        # Ensure vectorizer is fitted
        if not hasattr(vectorizer, 'idf_'):
            raise HTTPException(status_code=500, detail="Vectorizer not fitted. Retrain the model.")

        # Vectorize text
        text_vectorized = vectorizer.transform([cleaned_text])

        # Predict
        predicted_department = model_dept.predict(text_vectorized)[0]
        predicted_authority = model_auth.predict(text_vectorized)[0]

        # Confidence
        prob_dept = float(max(model_dept.predict_proba(text_vectorized)[0]))
        prob_auth = float(max(model_auth.predict_proba(text_vectorized)[0]))

        # Related PIOs
        pios = get_pios_for_department(predicted_department, df)

        return PredictResponse(
            predicted_department=predicted_department,
            predicted_authority=predicted_authority,
            confidence_department=prob_dept,
            confidence_authority=prob_auth,
            pios=pios[:5]
        )

    except Exception as e:
        print("❌ Prediction Error Traceback:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/generate-letter", response_model=GenerateLetterResponse)
async def generate_letter(request: GenerateLetterRequest):
    """Generate RTI letter using GPT and PIO details"""
    if df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded.")

    try:
        pio_info = {
            'Department': request.department,
            'PIO_Authority': request.pio_authority or 'Public Information Officer',
            'Authority_Name': request.authority_name or 'Concerned Authority',
            'State': request.state or 'India'
        }

        # Auto-select default PIO if missing
        if not request.pio_authority:
            dept_pios = get_pios_for_department(request.department, df)
            if dept_pios:
                pio_info = dept_pios[0]

        # Generate letter
        letter = generate_rti_letter_gpt(
            user_issue=request.user_issue,
            pio_info=pio_info,
            user_name=request.user_name,
            user_address=request.user_address
        )

        return GenerateLetterResponse(letter=letter)

    except Exception as e:
        print("❌ Letter Generation Error Traceback:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Letter generation error: {str(e)}")


@app.get("/pios")
async def get_all_pios():
    """Get sample PIOs for all departments"""
    if df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded.")

    try:
        departments = sorted(df['Department'].unique().tolist())
        dept_pios = {dept: get_pios_for_department(dept, df)[:3] for dept in departments}
        return {"departments": departments, "department_pios": dept_pios}
    except Exception as e:
        print("❌ Fetch PIO Error Traceback:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching PIOs: {str(e)}")


# ===========================================================
# Run Server
# ===========================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
