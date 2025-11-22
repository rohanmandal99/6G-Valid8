// Landing page of the tool
import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import UploadLog from "./components/UploadLog";
import Dashboard from "./components/dashboard/Dashboard";

export default function App(){
  const [parsedData, setParsedData] = useState(null);
  const [page, setPage] = useState("home");
  const [aiSummary, setAiSummary] = useState(null);
  const [loadingAI, setLoadingAI] = useState(false);

  const handleParsed = (data) => {
    setParsedData(data);
    setAiSummary(null);
    setPage("results");
  };

  const requestAISummary = async (parsed) => {
    if(!parsed) return;
    setLoadingAI(true);
    setAiSummary(null);
    try {
      const payload = { events: parsed.events || [], procedures: parsed.procedures || {} };
      const res = await fetch("http://127.0.0.1:8000/llm/analyze", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload),
      });
      const json = await res.json();
      // backend returns {"summary": {...}}
      setAiSummary(json.summary ?? json);
    } catch (err){
      console.error("LLM error", err);
      setAiSummary({
        observations: [{ description: "Failed to get AI summary (backend error)" }],
        triage_suggestions: [],
        anomalies: [],
        recommendations: []
      });
    } finally {
      setLoadingAI(false);
    }
  };

  return (
    <div className="app-root">
      <Sidebar onNavigate={setPage} active={page}/>
      <div className="main-area">
        <Header />
        <main className="content">
          {page === "home" && (
            <div style={{display:"grid", gridTemplateColumns:"1fr 420px", gap:"1rem"}}>
              <section className="hero-card">
                <h2 className="h1">6G-Valid8: AI Assisted Wireless Validation Platform</h2>
                <p className="small-muted">Upload 5G NR protocol logs (.txt, .log, .pu). The tool parses PHY/MAC/RRC/NAS events, detects complex wireless procedures and offers AI-assisted triage suggestions.</p>
                <ul className="small-muted">
                  <li>Parse PHY / MAC / RRC events</li>
                  <li>Procedure extraction (RA/ Handover/ BWP Switching)</li>
                  <li>LLM-assisted explainable triage</li>
                </ul>
              </section>

              <aside className="card">
                <UploadLog onParsed={handleParsed} />
              </aside>
            </div>
          )}

          {page === "results" && parsedData && (
            <Dashboard
              parsed={parsedData}
              aiSummary={aiSummary}
              requestAISummary={() => requestAISummary(parsedData)}
              onBack={() => setPage("home")}
              loadingAI={loadingAI}
            />
          )}

          {page === "results" && !parsedData && (
            <div className="card notice">No parsed data available. Upload a log to see results.</div>
          )}
        </main>
      </div>
    </div>
  );
}