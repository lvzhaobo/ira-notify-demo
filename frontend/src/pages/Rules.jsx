import React, { useEffect, useState } from "react";
import { fetchHealth, fetchRules } from "../api";

export default function RulesPage() {
  const [health, setHealth] = useState(null);
  const [rulesPayload, setRulesPayload] = useState(null);
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
        const { data } = await fetchRules({ limit: 20 });
        if (!cancelled) setRulesPayload(data);
      } catch (e) {
        if (!cancelled) setErr(e.response?.data || { message: e.message });
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const items = rulesPayload?.items ?? [];
  const listOk = rulesPayload && Array.isArray(items);

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>US-M4-001 · 规则 CRUD</h2>
      <p style={{ color: "#5e6c84", fontSize: "0.9rem" }}>
        健康检查应成功；列表接口应对齐 <code>spec/09</code>（<code>items / nextCursor / hasMore</code>）。
      </p>
      <section style={{ background: "#fff", border: "1px solid #dfe1e6", borderRadius: 4, padding: "0.75rem 1rem", marginBottom: "1rem" }}>
        <div style={{ fontSize: "0.75rem", color: "#5e6c84" }}>GET /api/v1/notify/health</div>
        <pre style={{ margin: "0.5rem 0 0", fontSize: "0.8rem", overflow: "auto" }}>{JSON.stringify(health, null, 2)}</pre>
      </section>
      <section style={{ background: "#fff", border: "1px solid #dfe1e6", borderRadius: 4, padding: "0.75rem 1rem" }}>
        <div style={{ fontSize: "0.75rem", color: "#5e6c84" }}>GET /api/v1/notify/rules</div>
        <pre style={{ margin: "0.5rem 0 0", fontSize: "0.8rem", overflow: "auto" }}>
          {err
            ? JSON.stringify(err, null, 2)
            : listOk
              ? JSON.stringify(rulesPayload, null, 2)
              : "加载中…"}
        </pre>
        {listOk && (
          <p style={{ margin: "0.75rem 0 0", fontSize: "0.85rem", color: "#5e6c84" }}>
            当前共 <strong>{items.length}</strong> 条规则（演示页仅展示 JSON，完整表单可在后续迭代补充）。
          </p>
        )}
      </section>
    </div>
  );
}
