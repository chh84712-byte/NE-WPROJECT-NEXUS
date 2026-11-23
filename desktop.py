
import threading
import time
import webview
import uvicorn

def start_server():
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        log_level="warning"
    )

if __name__ == "__main__":
    server_thread = threading.Thread(
        target=start_server,
        daemon=True
    )
    server_thread.start()

    time.sleep(2)

    webview.create_window(
        "NEXUS AI",
        "http://127.0.0.1:8000",
        width=1200,
        height=800,
        min_size=(700, 500),
        background_color="#080812"
    )

    webview.start()
