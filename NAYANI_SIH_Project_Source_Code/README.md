# NAYANI – AI-Assisted Screening for Diabetic Retinopathy

SIH 2026 prototype.

Pipeline: Image Upload -> Quality Check -> AI Model -> XAI Heatmap -> Severity Report -> Referral Priority.

Stack: React + Vite frontend, FastAPI backend, OpenCV/Pillow image processing.

## Backend
cd backend
python -m venv venv
Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

## Frontend
cd frontend
npm install
npm run dev

Frontend: http://localhost:5173
Backend: http://127.0.0.1:8000

IMPORTANT: The included model is a deterministic prototype fallback, not a clinically validated diagnostic model. Replace it with a trained and validated model before any clinical use.
