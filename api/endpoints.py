import sys
import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

# Add the project root directory to the Python path
# This allows imports like 'from numerology.report_builder import ...' when running the script directly.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Go up one level from api/endpoints.py
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from numerology.report_builder import build_report_string
from data_io import save_user_feedback

router = APIRouter()


# --- Pydantic Schemas ---

class ReportRequest(BaseModel):
    name: str
    birth_date: str  # Expected in "YYYY-MM-DD" format


class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str


# --- Routes ---

@router.post("/generate-report")
async def build_report_string(request: Request):
    try:
        user_data = await request.json()
        validated_data = ReportRequest(**user_data)
        report = build_report_string(validated_data.dict())
        return JSONResponse(content=report)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.post("/submit-feedback")
async def submit_feedback(request: Request):
    try:
        feedback_data = await request.json()
        validated = FeedbackRequest(**feedback_data)
        save_user_feedback(validated.user_id, validated.feedback)
        return JSONResponse(content={"status": "Feedback saved"})
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save feedback: {str(e)}")
