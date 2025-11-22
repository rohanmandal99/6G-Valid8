import React from "react";

function renderContent(data, emptyMsg){
  if(!data) return <p className="small-muted">{emptyMsg}</p>;
  if(typeof data === "string") return <pre className="pre">{data}</pre>;
  return <pre className="pre">{JSON.stringify(data, null, 2)}</pre>;
}

export default function AISummary({ summary }){
  if(!summary) return null;

  return (
    <div className="card">
      <h3>AI-Assisted Summary</h3>

      <div style={{marginTop:8}}>
        <strong>Observations</strong>
        {renderContent(summary.observations, "No observations available")}
      </div>

      <div style={{marginTop:8}}>
        <strong>Triage Suggestions</strong>
        {renderContent(summary.triage_suggestions, "No triage suggestions available")}
      </div>

      <div style={{marginTop:8}}>
        <strong>Anomalies</strong>
        {renderContent(summary.anomalies, "No anomalies detected")}
      </div>

      <div style={{marginTop:8}}>
        <strong>Recommendations</strong>
        {renderContent(summary.recommendations, "No recommendations available")}
      </div>
    </div>
  );
}