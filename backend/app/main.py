from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import analysis, generation, publish, export

app = FastAPI(title="YouTube AI Automation API", version="1.0.0")

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api")
app.include_router(generation.router, prefix="/api")
app.include_router(publish.router, prefix="/api")
app.include_router(export.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to the YouTube AI Automation API"}
