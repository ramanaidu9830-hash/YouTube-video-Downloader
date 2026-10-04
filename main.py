import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI(
    title="YouTube Video Downloader API",
    description="API to extract video info and download links",
    version="1.0.0"
)

# Enable CORS for frontend requests (allows HTML/JS to communicate with API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route to fix "{"detail": "Not Found"}" error
@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "YouTube Downloader API is active!",
        "docs_url": "/docs"
    }

# Main endpoint used by script.js / downloader.html
@app.get("/api/info")
def get_video_info(url: str = Query(..., description="YouTube Video or Shorts URL")):
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "download_url": info.get("url")  # Direct download URL
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")