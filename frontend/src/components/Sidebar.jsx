import React, { useState } from "react";

export default function Sidebar({ onNavigate, active }) {
  const [collapsed, setCollapsed] = useState(false);

  const buttonStyle = (isActive) => ({
    display: "flex",
    alignItems: "center",
    margin: "8px 0",
    background: "transparent",
    color: isActive ? "#fff" : "#111111",
    border: "none",
    cursor: "pointer",
    fontWeight: isActive ? "1500" : "500",
    background: isActive ? "#3b82f6" : "transparent",
    textAlign: "left",
    fontSize: "15px", 
    padding: "7px 12px",
    whiteSpace: "nowrap",
    width: "100%", 
    textOverflow: "ellipsis",
    borderRadius: 5, 
    overflow: "hidden",
    transition: "background 0.2s, color 0.2s"
  });

  return (
    <div
      className="sidebar"
      style={{
        backgroundColor: "#cccccc",
        padding: 20,
        //height: "100vh",
        width: collapsed ? 60 : 200,
        transition: "width 0.3s",
        overflow: "hidden",
      }}
    >
      <div style={{ display: "flex", justifyContent: collapsed ? "center" : "space-between", alignItems: "center" }}>
        <h3 style={{ marginTop: 0, color: "#111827", display: collapsed ? "none" : "block" }}>6G-Valid8</h3>
        <button
          onClick={() => setCollapsed(!collapsed)}
          style={{ background: "transparent", border: "none", cursor: "pointer" }}
        >
          {collapsed ? "➡️" : "⬅️"}
        </button>
      </div>

      <nav style={{ marginTop: 20 }}>
        <button onClick={() => onNavigate("home")} style={buttonStyle(active === "home")}>
          {collapsed ? "🏠" : "Home"}
        </button>
        <button onClick={() => onNavigate("results")} style={buttonStyle(active === "results")}>
          {collapsed ? "📄" : "Results"}
        </button>
      </nav>
    </div>
  );
}