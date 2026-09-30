document.addEventListener("DOMContentLoaded", () => {
    const downloadBtn = document.getElementById("downloadBtn") || document.querySelector("button");
    const urlInput = document.getElementById("videoUrl") || document.querySelector("input[type='text']");
    const statusMessage = document.getElementById("statusMessage") || document.getElementById("error") || createStatusElement();

    function createStatusElement() {
        const el = document.createElement("div");
        el.id = "statusMessage";
        el.style.marginTop = "15px";
        el.style.fontWeight = "bold";
        if (downloadBtn && downloadBtn.parentNode) {
            downloadBtn.parentNode.appendChild(el);
        }
        return el;
    }

    if (downloadBtn) {
        downloadBtn.addEventListener("click", async (e) => {
            e.preventDefault();
            
            const videoUrl = urlInput ? urlInput.value.trim() : "";
            if (!videoUrl) {
                statusMessage.style.color = "red";
                statusMessage.innerText = "Please enter a valid YouTube URL!";
                return;
            }

            statusMessage.style.color = "#333";
            statusMessage.innerText = "Processing video... Please wait.";
            downloadBtn.disabled = true;

            try {
                const response = await fetch("https://youtube-video-downloader-1-h8vj.onrender.com/download", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ url: videoUrl }),
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => null);
                    const errorMessage = errorData && errorData.detail ? errorData.detail : "Download failed. Check URL or cookies.";
                    throw new Error(errorMessage);
                }

                statusMessage.style.color = "green";
                statusMessage.innerText = "Download starting...";

                // Handle binary file download
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = downloadUrl;
                
                // Get filename from response header or default
                const contentDisposition = response.headers.get("content-disposition");
                let filename = "video.mp4";
                if (contentDisposition && contentDisposition.includes("filename=")) {
                    filename = contentDisposition.split("filename=")[1].replace(/["']/g, "");
                }
                
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(downloadUrl);

                statusMessage.innerText = "Download completed successfully!";
            } catch (err) {
                statusMessage.style.color = "red";
                statusMessage.innerText = `Error: ${err.message}`;
            } finally {
                downloadBtn.disabled = false;
            }
        });
    }
});