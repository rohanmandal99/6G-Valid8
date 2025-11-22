import React from "react";

export default function EventsTable({ events }){
  if(!events || events.length === 0) return <div className="notice">No events parsed.</div>;

  return (
    <table className="table">
      <thead>
        <tr>
          <th>Time</th>
          <th>Component</th>
          <th>Type</th>
          <th>Message</th>
          <th>Metrics</th>
        </tr>
      </thead>
      <tbody>
        {events.slice(0,200).map((e,idx) => (
          <tr key={idx}>
            <td>{e.ts ?? "-"}</td>
            <td>{e.component ?? "-"}</td>
            <td>{e.event_type ?? "-"}</td>
            <td style={{maxWidth:420}} className="pre">{e.message ?? e.msg ?? "-"}</td>
            <td>{e.metrics ? JSON.stringify(e.metrics) : "-"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}