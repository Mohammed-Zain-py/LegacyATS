from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from backend.legacy_parser import extract_text_from_pdf
from backend.gemini_evaluator import evaluate_resume_with_llm

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="LegacyATS Gatekeeper Engine", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def add_digital_signature(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Engine-Auth"] = "ZAIN-LEGACY-ATS-2026-CORE"
    response.headers["X-Developer"] = "Zain - Built for the students"
    return response

@app.post("/analyze")
@limiter.limit("5/minute")
async def analyze_resume(
    request: Request, 
    file: UploadFile = File(...),
    job_description: str = Form(...),
    api_key: str = Form("")
):
    if not api_key:
        return JSONResponse(status_code=400, content={
            "status": "error",
            "score": 0,
            "feedback": "Missing Gemini Authorization Key."
        })

    file_bytes = await file.read()
    parser_result = extract_text_from_pdf(file_bytes)
    
    if parser_result["status"] == "error":
        return JSONResponse(status_code=400, content={
            "status": "error",
            "score": 0,
            "feedback": parser_result["message"]
        })
    
    llm_result = evaluate_resume_with_llm(
        raw_text=parser_result["extracted_text"], 
        job_description=job_description, 
        api_key=api_key
    )
    
    return {
        "status": "success",
        "score": llm_result.get("score", 0),
        "feedback": llm_result.get("feedback", "No feedback generated."),
        "found_keywords": llm_result.get("found_keywords", []),
        "missing_keywords": llm_result.get("missing_keywords", []),
        "optimized_corrections": llm_result.get("optimized_corrections", "")
    }

@app.post("/mock-demo")
@limiter.limit("10/minute")
async def mock_demo(request: Request):
    """Simulates a corrupted multi-column parse for recruiter onboarding."""
    return {
        "status": "rejected",
        "score": 32,
        "feedback": (
            "CRITICAL MINIMUM THRESHOLD FAILURE: Left-hand layout column collided with right-hand headers. "
            "Extracted keywords mapped 'Languages' into 'Project Timelines'. "
            "Parsing matrix failed to detect chronological progression. System profile flagged as un-indexable."
        ),
        "raw_text": "Mohammed Zain md.zain.1293@gmail.com PROJECTS:Speech-DrivenNLU EDUCATION:BEAIML2022-2026 CGPA:8.0SKILLS:Python,SQLTimeline:November2025 Builta voice-driven webapp"
    }