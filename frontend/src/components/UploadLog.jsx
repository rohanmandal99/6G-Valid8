import React, { useRef, useState } from "react";

export default function UploadLog({ onParsed }){
  const inputRef = useRef();
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const onSelect = () => inputRef.current?.click();

  const handleChange = async (e) => {
    const file = e.target.files?.[0];
    if(!file) return;
    setFileName(file.name);
    setMsg("");
    setLoading(true);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/parse/logfile", {
        method: "POST",
        body: form
      });
      if(!res.ok) throw new Error("Upload failed");
      const data = await res.json();
      setMsg("Upload successful");
      onParsed(data.parsed || data); // backend returns { parsed: ... } or direct parsed
    } catch (err) {
      console.error(err);
      setMsg("Upload failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3 style={{marginTop:0}}>Upload Log</h3>
      <p className="small-muted">Accepts .txt .log .pu</p>

      <input ref={inputRef} onChange={handleChange} type="file" accept=".txt,.log,.pu" style={{display:"none"}} />

      <div style={{display:"flex",gap:8,alignItems:"center"}}>
        <button className="upload-btn" onClick={onSelect} disabled={loading}>
          {loading ? "Uploading…" : "Select & Upload Log"}
        </button>
        <div style={{minWidth:220}}>
          <div className="small-muted">{fileName || "No file chosen"}</div>
          <div className="small-muted" style={{fontSize:".85rem"}}>{msg}</div>
        </div>
      </div>
    </div>
  );
}