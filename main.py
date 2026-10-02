from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pytubefix import YouTube
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Video(BaseModel):
    url: str

@app.post("/download")
def download_video(video: Video):
    try:
        cookie_path = os.path.abspath("cookies.txt")
        
        # pytubefix accepts cookiefile (not cookies)
        if os.path.exists(cookie_path):
            yt = YouTube(
                video.url,
                cookiefile=cookie_path,
                client='WEB'
            )
        else:
            yt = YouTube(video.url, client='WEB')

        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if stream is None:
            stream = yt.streams.get_highest_resolution()

        if stream is None:
            raise HTTPException(status_code=404, detail="No suitable video stream found")

        download_folder = "downloads"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        download_path = stream.download(output_path=download_folder)
        filename = os.path.basename(download_path)

        return FileResponse(
            path=download_path, 
            filename=filename, 
            media_type='video/mp4'
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))