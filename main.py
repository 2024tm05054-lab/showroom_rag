from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from datetime import datetime
import shutil

app = FastAPI(title="Automotive Service RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    total_chunks: int

class HealthResponse(BaseModel):
    status: str
    indexed_docs: int
    chunk_count: int
    uptime: str

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy - ready for PDF ingest",
        indexed_docs=0,
        chunk_count=0,
        uptime=str(datetime.now())
    )

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files allowed")
    
    os.makedirs("uploads", exist_ok=True)
    pdf_path = f"uploads/{file.filename}"
    
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "status": "success",
        "filename": file.filename,
        "message": f"PDF saved to {pdf_path}. RAG processing coming soon.",
        "next_step": "Query /query endpoint after full implementation"
    }

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    return {
        "answer": "RAG query endpoint ready. Ingest PDF first via /ingest",
        "sources": [],
        "total_chunks": 0
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
