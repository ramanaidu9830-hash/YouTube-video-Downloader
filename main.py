from fastapi import FastAPI, HTTPException, Query
import yt_dlp
import os

app = FastAPI(title="YouTube Video Downloader API")

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

    # Ultra-flexible format rule to ensure YouTube Shorts match instantly
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

            # 1. Check direct url field
            if info.get('url'):
                download_url = info.get('url')

            # 2. Check requested_formats (video/audio split)
            elif 'requested_formats' in info and info['requested_formats']:
                download_url = info['requested_formats'][0].get('url')

            # 3. Check formats list fallback
            elif 'formats' in info and len(info['formats']) > 0:
                # Get the last format entry that contains a valid url
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