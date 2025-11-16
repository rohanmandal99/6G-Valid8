async function loadStatus() {
    try {
        const res = await fetch("http://127.0.0.1:8000/");
        const data = await res.json();

        document.getElementById("app").innerText =
            "Backend: " + data.status;
    } catch (e) {
        document.getElementById("app").innerText =
            "Cannot connect to backend";
    }
}

loadStatus();