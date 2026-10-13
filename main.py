from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlparse
import yt_dlp

app = FastAPI(title="YouTube Video Information API")

# Allow requests from your Netlify website
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://unique-speculoos-b6ea0a.netlify.app"
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "YouTube Downloader API is running!"
    }


@app.get("/get_video_info")
def get_video_info(url: str):

    # Check empty URL
    if not url or not url.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a YouTube URL"
        )

    url = url.strip()

    # Validate the URL
    try:
        parsed_url = urlparse(url)
        hostname = (parsed_url.hostname or "").lower()

        allowed_hosts = {
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtu.be",
            "www.youtube-nocookie.com",
        }

        if hostname not in allowed_hosts:
            raise HTTPException(
                status_code=400,
                detail="Please enter a valid YouTube URL"
            )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid URL"
        )

    # Get video information only; do not download the video
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "skip_download": True,
        "socket_timeout": 20,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                url,
                download=False
            )

            return {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "video_id": info.get("id"),
                "webpage_url": info.get("webpage_url"),
            }

    except Exception as e:
        error_message = str(e)

        print("YouTube extraction error:", error_message)

        if "Sign in to confirm" in error_message:
            raise HTTPException(
                status_code=502,
                detail=(
                    "YouTube requires authentication for this request. "
                    "Try again later or use an authorized video source."
                )
            )

        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve video information."
        )