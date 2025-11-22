import React from "react";
export default function Header(){
  return (
    <div className="header" style={{display:"flex",alignItems:"center",justifyContent:"space-between"}}>
      <div style={{fontWeight:600}}>6G-Valid8</div>
      <div className="small-muted">Local dev</div>
    </div>
  );
}