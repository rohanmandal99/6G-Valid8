import React from "react";
export default function SummaryCards({ parsed }){
  // quick counts
  const total = parsed?.events?.length ?? 0;
  const ues = new Set((parsed?.events||[]).map(e => e.component)).size;

  return (
    <div className="grid-3">
      <div className="card">
        <h3>Overview</h3>
        <div className="small-muted">Events</div>
        <div style={{fontWeight:700,fontSize:"1.25rem"}}>{total}</div>
        <div className="small-muted">Components detected: {ues}</div>
      </div>

      <div className="card">
        <h3>Procedures</h3>
        <div className="small-muted">RA</div>
        <div style={{fontWeight:700}}>—</div>
        <div className="small-muted">More procedure cards will appear here</div>
      </div>

      <div className="card">
        <h3>UE Config</h3>
        <div className="small-muted">Center frequency / BW / SCS</div>
        <div style={{fontWeight:700}}>—</div>
      </div>
    </div>
  );
}