from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .models import ClinicalNote, ClinicalResponse, MethodUsed
from .extractor import ClinicalExtractor
from .llm_service import llm_primary_analysis
import time
from pathlib import Path

app = FastAPI(title="🏥 Clinical Note AI")
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

extractor = ClinicalExtractor()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_path = FRONTEND_DIR / "index.html"
    return index_path.read_text(encoding="utf-8")

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0"}

@app.post("/extract", response_model=ClinicalResponse)
async def extract_clinical_data(note: ClinicalNote):
    start_time = time.time()
    
    # LLM first → Rule-based precision
    llm_result = await llm_primary_analysis(note.text)
    
    # Add precise vitals/meds
    precision_data = extractor.extract_vitals_meds(note.text)
    llm_result["vitals"] = precision_data["vitals"]
    llm_result["medications"] = precision_data["medications"]
    
    # Healthcare AI personality
    casual_keywords = ['how are you', 'hi', 'hello', 'vasanth']
    if any(keyword in note.text.lower() for keyword in casual_keywords):
        llm_result["message"] = "👋 I'm Clinical Note AI! Paste clinical notes to extract SOAP structure."
        method_used = MethodUsed.healthcare_ai
    else:
        llm_result["message"] = "✅ Clinical note processed successfully"
        method_used = MethodUsed.llm_primary
    
    # Summary + confidence
    summary = f"Patient: {llm_result.get('subjective', 'N/A')[:50]}... | Assessment: {llm_result.get('assessment', 'N/A')}"
    confidence = 0.92  # LLM baseline
    
    return ClinicalResponse(
        structured_data=llm_result,
        summary=summary,
        confidence_score=round(confidence, 2),
        processing_time_ms=round((time.time() - start_time) * 1000, 1),
        method_used=method_used,
        message=llm_result["message"]
    )
