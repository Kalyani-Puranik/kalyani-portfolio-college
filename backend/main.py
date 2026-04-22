
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from routers import blogs, projects, contact, analytics, auth, github, spotify, photos

app = FastAPI(
    title="Kalyani Portfolio API",
    description="Backend API powering Kalyani's personal portfolio",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    #lifespan=lifespan,
)

app.include_router(github.router, prefix="/github", tags=["GitHub"])

# ── MIDDLEWARE ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ── ROUTERS ────────────────────────────────────────────
app.include_router(auth.router,      prefix="/auth",      tags=["Auth"])
app.include_router(blogs.router,     prefix="/blogs",     tags=["Blogs"])
app.include_router(projects.router,  prefix="/projects",  tags=["Projects"])
app.include_router(contact.router,   prefix="/contact",   tags=["Contact"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(github.router,    prefix="/github",    tags=["GitHub"])
app.include_router(spotify.router,   prefix="/spotify",   tags=["Spotify"])
app.include_router(photos.router,    prefix="/photos",    tags=["Photos"])


# ── HEALTH CHECK ───────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "✨ Kalyani's portfolio API is alive",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy", "service": "kalyani-portfolio"}


# ── RESUME DOWNLOAD ────────────────────────────────────
from fastapi.responses import FileResponse

@app.get("/resume/download", tags=["Resume"])
async def download_resume():
    file_path = "static/Kalyani_Resume.pdf"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename="Kalyani_Resume.pdf", media_type="application/pdf")
    return {"error": "Resume not found. Please upload it to static/Kalyani_Resume.pdf"}
