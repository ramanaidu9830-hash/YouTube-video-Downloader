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
        # Pass cookies file directly to pytubefix
        yt = YouTube(
            video.url,
            cookies="cookies.txt"
        )
        
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if stream is None:
            stream = yt.streams.get_highest_resolution()
            
        if stream is None:
            raise HTTPException(status_code=404, detail="No suitable stream found")

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