from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
import shutil
import os
from src.ingestion import ingest_pdf

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/ingest")
async def ingest_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, "Only PDF files allowed")
    
    os.makedirs("uploads", exist_ok=True)
    pdf_path = f"uploads/{file.filename}"
    
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = ingest_pdf(pdf_path)
    return result

@router.post("/query")
async def query_endpoint(request: QueryRequest):
    from src.retrieval