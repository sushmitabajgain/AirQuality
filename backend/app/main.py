from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.aqhi import router as aqhi_router

app = FastAPI(title="Alberta AQHI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite React frontend
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aqhi_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"ok": True}