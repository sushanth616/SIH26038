from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uuid, shutil
from services.pipeline import run_pipeline

BASE = Path(__file__).resolve().parent
UPLOAD_DIR = BASE / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="NAYANI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

@app.get("/")
def root():
    return {"name": "NAYANI", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/screen")
async def screen_retina(file: UploadFile = File(...)):
    allowed={".jpg",".jpeg",".png",".webp"}
    ext=Path(file.filename or "").suffix.lower()
    if ext not in allowed:
        raise HTTPException(400,"Please upload JPG, JPEG, PNG or WEBP image.")
    job_id=uuid.uuid4().hex
    saved=UPLOAD_DIR/f"{job_id}{ext}"
    with saved.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        result=run_pipeline(saved)
        result["image_url"]=f"/uploads/{saved.name}"
        result["job_id"]=job_id
        return result
    except Exception as exc:
        saved.unlink(missing_ok=True)
        raise HTTPException(500,f"Screening failed: {exc}")
