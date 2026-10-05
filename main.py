from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

app = FastAPI(title="YouTube Video Downloader API")

# Enable CORS for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COOKIES_FILE = "cookies.txt"

@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "YouTube Downloader API is active!",
        "docs_url": "/docs"
    }

@app.get("/api/info")
def get_video_info(url: str = Query(..., description="YouTube Video URL")):
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'b/bv*+ba/best',
    }

    if os.path.exists(COOKIES_FILE):
        ydl_opts['cookiefile'] = COOKIES_FILE

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            download_url = None

            if info.get('url'):
                download_url = info.get('url')
            elif 'requested_formats' in info and info['requested_formats']:
                download_url = info['requested_formats'][0].get('url')
            elif 'formats' in info and len(info['formats']) > 0:
                valid_formats = [f for f in info['formats'] if f.get('url')]
                if valid_formats:
                    download_url = valid_formats[-1].get('url')

            return {
                "status": "success",
                "title": info.get('title'),
                "duration": info.get('duration'),
                "uploader": info.get('uploader'),
                "download_url": download_url,
                "thumbnail": info.get('thumbnail')
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")