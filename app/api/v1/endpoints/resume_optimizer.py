from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.schemas.resume_optimizer import JobDescription, OptimizationQuery, OptimizationResponse
from app.models.resume_optimizer import DocumentProcessor
from app.models.llm_manager import get_llm_manager
import logging
import tempfile
import os
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()
doc_processor = DocumentProcessor()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        await doc_processor.process_resume(temp_file_path)
        
        os.unlink(temp_file_path)
        return {"message": "Resume processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/add-job-description")
async def add_job_description(job_desc: JobDescription):
    try:
        await doc_processor.process_job_description(job_desc.text)
        return {"message": "Job description processed successfully"}
    except Exception as e:
        logger.error(f"Optimization error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/optimize", response_model=OptimizationResponse)
async def optimize_resume(query: OptimizationQuery):
    try:
        response = await doc_processor.optimize_resume(query.query)
        return OptimizationResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/optimize-batch")
async def optimize_resume_batch(queries: List[OptimizationQuery]):
    try:
        responses = await doc_processor.llm_manager.generate_batch_responses(
            [query.query for query in queries]
        )
        return [OptimizationResponse(response=response) for response in responses]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/test-llm")
async def test_llm():
    try:
        llm_manager = get_llm_manager()
        response = await llm_manager.generate_response("Say hello and introduce yourself in one sentence.")
        return {"response": response}
    except Exception as e:
        logger.error(f"Test LLM error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-optimization")
async def test_optimization():
    test_resume = """
    EXPERIENCE
    Software Engineer, ABC Tech
    • Led development of customer-facing application
    • Worked on backend systems
    • Managed team projects
    """
    
    test_job = """
    Senior Software Engineer
    Requirements:
    • 5+ years experience in full-stack development
    • Experience leading teams and projects
    • Strong backend development skills
    """
    
    try:
        # Process test data
        await doc_processor.process_resume(test_resume)
        await doc_processor.process_job_description(test_job)
        
        # Test optimization
        response = await doc_processor.optimize_resume(
            "Provide specific recommendations for improving these bullet points."
        )
        
        return {"test_response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))