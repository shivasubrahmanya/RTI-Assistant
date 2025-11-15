# RTI Assistant - Backend

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure OpenAI API Key

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your-actual-api-key-here
```

### 3. Train the ML Model

Run the training script to create the `model.pkl` file:

```bash
python train_model.py
```

This will:
- Load the PIO dataset
- Preprocess the text data
- Train a Logistic Regression model with TF-IDF vectorization
- Save the model and vectorizer to `model.pkl`

### 4. Start the FastAPI Server

```bash
uvicorn main:app --reload
```

Or:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /
Health check endpoint

### POST /predict
Predict department from complaint text

**Request:**
```json
{
  "complaint": "My ration card has not been updated for 3 months"
}
```

**Response:**
```json
{
  "predicted_department": "Food and Civil Supplies",
  "confidence": 0.95,
  "pios": [...]
}
```

### POST /generate-letter
Generate RTI letter using OpenAI GPT

**Request:**
```json
{
  "user_issue": "My ration card issue",
  "user_name": "John Doe",
  "user_address": "123 Main St, City",
  "department": "Food and Civil Supplies",
  "pio_authority": "District Supply Officer",
  "authority_name": "Ramesh Kumar",
  "state": "Maharashtra"
}
```

**Response:**
```json
{
  "letter": "Generated RTI letter text..."
}
```

### GET /pios
Get all departments and PIOs

**Response:**
```json
{
  "departments": [...],
  "department_pios": {...}
}
```

## Troubleshooting

- If you get "Model not loaded" error, run `python train_model.py` first
- If letter generation fails, check your OpenAI API key in `.env`
- Ensure all dependencies are installed: `pip install -r requirements.txt`
