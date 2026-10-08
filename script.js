async function downloadVideo() {
    const urlInput = document.getElementById("videoUrl");
    const resultDiv = document.getElementById("result");

    if (!urlInput || !urlInput.value.trim()) {
        alert("Please enter a valid YouTube URL");
        return;
    }

    const videoUrl = urlInput.value.trim();
    resultDiv.innerHTML = "<p style='color: #ffc107;'>Processing video... Please wait (10-20 sec)</p>";

    // Render URL with /get_video_info route matching your live backend
    const backendUrl = `https://youtube-video-downloader-1-h8vj.onrender.com/get_video_info?url=${encodeURIComponent(videoUrl)}`;

    try {
        const response = await fetch(backendUrl);

        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }

        const data = await response.json();

        resultDiv.innerHTML = `
            <div style="text-align: center; margin-top: 15px;">
                <img src="${data.thumbnail || ''}" width="250" style="border-radius: 8px;" alt="Thumbnail" />
                <h3 style="color: white; margin: 10px 0;">${data.title || 'YouTube Video'}</h3>
                <a href="${data.download_url}" target="_blank" download style="
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #00d2ff;
                    color: black;
                    text-decoration: none;
                    font-weight: bold;
                    border-radius: 5px;
                    margin-top: 10px;
                ">Download Video</a>
            </div>
        `;

    } catch (error) {
        console.error("Fetch Error:", error);
        resultDiv.innerHTML = `<p style="color: #ff4d4d;">Failed to fetch video: ${error.message}</p>`;
    }
}