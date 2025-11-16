import threading
import time
import webview
import uvicorn
import requests

def start_backend():
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=False)

def wait_for_server(url, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except:
            pass
        time.sleep(0.1)
    return False

if __name__ == "__main__":
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()

    # Wait until backend is ready
    backend_url = "http://127.0.0.1:8000/frontend/index.html"
    if wait_for_server("http://127.0.0.1:8000"):
        # Open PyWebView window with frontend
        window = webview.create_window("6G-Valid8", url=backend_url, width=1200, height=800)
        webview.start()
    else:
        print("Backend did not start in time!")