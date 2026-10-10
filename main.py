from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "YouTube Downloader API is running!"}


@app.get("/get_video_info")
def get_video_info(url: str):

    if not url:
        raise HTTPException(
            status_code=400,
            detail="YouTube URL is required"
        )

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            return {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "download_url": info.get("url"),
            }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )