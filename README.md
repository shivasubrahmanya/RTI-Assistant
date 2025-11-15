# RTI Assistant

A complete end-to-end web application that helps users file RTI (Right to Information) requests in India by:
1. Predicting the correct department using machine learning
2. Identifying the appropriate Public Information Officer (PIO)
3. Generating formal RTI letters using OpenAI GPT

## Tech Stack

**Frontend:**
- React with TypeScript
- Tailwind CSS for styling
- Axios for API calls
- Lucide React for icons

**Backend:**
- FastAPI (Python)
- Scikit-learn (TF-IDF + Logistic Regression)
- OpenAI GPT-4o-mini for letter generation
- Pandas for data handling

## Features

- Natural language complaint input
- AI-powered department prediction
- Automated PIO identification
- GPT-generated formal RTI letters
- Copy and download functionality
- Responsive, production-ready design

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure OpenAI API key in `.env`:
```bash
OPENAI_API_KEY=your-api-key-here
```

4. Train the ML model:
```bash
python train_model.py
```

5. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Backend will run at `http://localhost:8000`

### Frontend Setup

1. Navigate to project root directory

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

Frontend will run at `http://localhost:5173`

## Usage

1. **Enter Complaint**: Describe your issue in natural language
2. **View Prediction**: See the predicted department and available PIOs
3. **Fill Details**: Enter your name and address
4. **Generate Letter**: AI creates a formal RTI letter
5. **Copy/Download**: Save your letter for submission

## Project Structure

```
rti-assistant/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── train_model.py          # ML model training
│   ├── utils.py                # Helper functions
│   ├── model.pkl               # Trained model (generated)
│   ├── PIO_Final_Synthetic_60000_fresh.csv
│   ├── requirements.txt
│   ├── .env
│   └── README.md
├── src/
│   ├── components/
│   │   ├── Home.jsx           # Complaint input
│   │   ├── LetterForm.jsx     # User details form
│   │   └── LetterDisplay.jsx  # Letter display
│   ├── App.tsx                # Main app
│   ├── api.js                 # API client
│   └── index.css
└── README.md
```

## API Endpoints

- `POST /predict` - Predict department from complaint
- `POST /generate-letter` - Generate RTI letter
- `GET /pios` - List all departments and PIOs

## Requirements

- Python 3.8+
- Node.js 18+
- OpenAI API key

## Development Notes

- The ML model uses TF-IDF vectorization and Logistic Regression
- Training dataset includes 50 sample complaints across various departments
- OpenAI API is used for generating formal RTI letters
- CORS is enabled for local development

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## License

MIT
