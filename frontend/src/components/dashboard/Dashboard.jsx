import React, { useEffect, useRef } from "react";
import SummaryCards from "./SummaryCards";
import EventsTable from "./EventsTable";
import AISummary from "./AISummary";
import ActionBar from "./ActionBar";

export default function Dashboard({ parsed, aiSummary, requestAISummary, onBack, loadingAI }){
  const summaryRef = useRef();

  useEffect(()=>{ if(aiSummary) summaryRef.current?.scrollIntoView({behavior:"smooth"}); }, [aiSummary]);

  return (
    <div>
      <button onClick={onBack} className="btn-secondary" style={{marginBottom:12}}>← Back</button>
      <h1 className="h1">Log Analysis Dashboard</h1>

      <SummaryCards parsed={parsed} />

      <h2 style={{marginTop:18}}>Parsed Events</h2>
      <div className="card" style={{marginTop:8}}>
        <EventsTable events={parsed?.events || []} />
      </div>

      <ActionBar onRequest={() => requestAISummary(parsed)} loading={loadingAI} />

      <div ref={summaryRef} style={{marginTop:18}}>
        <AISummary summary={aiSummary} />
      </div>
      
    </div>
  );
}