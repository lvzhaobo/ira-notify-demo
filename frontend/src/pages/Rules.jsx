import React, { useEffect, useState } from "react";
import { fetchHealth, fetchRules } from "../api";

export default function RulesPage() {
  const [health, setHealth] = useState(null);
  const [stub, setStub] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const h = await fetchHealth();
        if (!cancelled) setHealth(h);
      } catch (e) {
        if (!cancelled) setErr(e.response?.data || { message: e.message });
      }
      try {
        const r = await fetchRules();
        if (!cancelled) setStub(r.data);
      } catch (e) {
        if (cancelled) return;
        if (e.response?.status === 501) {
          setStub(e.response.data);
        } else {
          setErr(e.response?.data || { message: e.message });
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>US-M4-001 · 规则 CRUD</h2>
      <p style={{ color: "#5e6c84", fontSize: "0.9rem" }}>
        工作坊骨架：下方「健康检查」应成功；列表接口在实现前为 <strong>501 stub</strong>。
      </p>
      <section style={{ background: "#fff", border: "1px solid #dfe1e6", borderRadius: 4, padding: "0.75rem 1rem", marginBottom: "1rem" }}>
        <div style={{ fontSize: "0.75rem", color: "#5e6c84" }}>GET /api/v1/notify/health</div>
        <pre style={{ margin: "0.5rem 0 0", fontSize: "0.8rem", overflow: "auto" }}>{JSON.stringify(health, null, 2)}</pre>
      </section>
      <section style={{ background: "#fff", border: "1px solid #dfe1e6", borderRadius: 4, padding: "0.75rem 1rem" }}>
        <div style={{ fontSize: "0.75rem", color: "#5e6c84" }}>GET /api/v1/notify/rules（预期 501，直至后端实现）</div>
        <pre style={{ margin: "0.5rem 0 0", fontSize: "0.8rem", overflow: "auto" }}>
          {stub ? JSON.stringify(stub, null, 2) : err ? JSON.stringify(err, null, 2) : "加载中…"}
        </pre>
      </section>
    </div>
  );
}
