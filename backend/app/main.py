import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    description="Deterministic AST code analysis and repository architecture mapping."
)

# Enable CORS for local React/Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our analysis routes
app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}


# In the production Docker image, serve the built Vite app from this same
# origin. When running the API directly during development, keep its root
# health message and let Vite serve the frontend on its own port.
frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if os.environ.get("SERVE_FRONTEND") == "1" and frontend_dist.is_dir():
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
else:
    @app.get("/")
    def read_root():
        return {"message": "Codebase Mapper Backend is running successfully!"}
