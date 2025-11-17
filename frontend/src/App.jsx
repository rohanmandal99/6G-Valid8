import { useEffect, useState } from "react";

function App() {
  const [status, setStatus] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then(res => res.json())
      .then(data => setStatus(data.status))
      .catch(err => setStatus("Cannot connect to backend"));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>6G-Valid8</h1>
      <p>Backend: {status}</p>
    </div>
  );
}

export default App;