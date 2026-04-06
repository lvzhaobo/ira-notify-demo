import React from "react";

export default function DispatchPage() {
  return (
    <div>
      <h2 style={{ marginTop: 0 }}>US-M4-002 · 试发与投递历史</h2>
      <p style={{ color: "#5e6c84" }}>
        占位页：请按 <code>spec/06</code>（若课程提供）与 <code>spec/09</code> 实现试发表单与历史列表，并对接{" "}
        <code>POST /notify/dispatch</code>、<code>GET /notify/deliveries</code>。
      </p>
      <ul>
        <li>注意 <code>dryRun</code> 默认值与展示。</li>
        <li>列表需展示 <code>traceId</code>、<code>status</code>（以定稿 spec 为准）。</li>
      </ul>
    </div>
  );
}
