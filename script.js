document.addEventListener("DOMContentLoaded", () => {
    const downloadBtn = document.querySelector("button");
    const urlInput = document.querySelector("input");

    downloadBtn.addEventListener("click", async () => {
        const videoUrl = urlInput.value;

        if (!videoUrl) {
            alert("Please paste a valid YouTube URL!");
            return;
        }

        downloadBtn.innerText = "Downloading...";
        downloadBtn.disabled = true;

        try {
            const response = await fetch("http://127.0.0.1:8000/download", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url: videoUrl })
            });

            const result = await response.json();

            if (response.ok) {
                alert("Download Complete!");
            } else {
                alert("Error: " + result.detail);
            }
        } catch (error) {
            alert("Server ki connect avvaledu. FastAPI server run avutundo ledo chuskondi.");
        } finally {
            downloadBtn.innerText = "Download";
            downloadBtn.disabled = false;
        }
    });
});