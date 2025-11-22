import React from "react";

export default function ActionBar({ onRequest, loading }){
  return (
    <div style={{marginTop:12, display:"flex", justifyContent:"center"}}>
      <button className="btn-primary" onClick={onRequest} disabled={loading}>
        {loading ? "Processing AI..." : "Generate AI Summary"}
      </button>
    </div>
  );
}