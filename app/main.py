from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import resume_optimizer
from app.core.config import settings
from fastapi.responses import HTMLResponse
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(
    resume_optimizer.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["resume-optimizer"])

# Serve the HTML file
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join("app/static", "optimizer_portal.html")) as f:
        return HTMLResponse(content=f.read(), status_code=200)
    