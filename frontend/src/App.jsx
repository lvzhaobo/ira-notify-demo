import React from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import RulesPage from "./pages/Rules";
import DispatchPage from "./pages/Dispatch";
import ChannelsPage from "./pages/Channels";

const navStyle = ({ isActive }) => ({
  padding: "0.5rem 0.75rem",
  textDecoration: "none",
  color: isActive ? "#0c66e4" : "#5e6c84",
  fontWeight: isActive ? 600 : 400,
  borderBottom: isActive ? "2px solid #0c66e4" : "2px solid transparent",
});

export default function App() {
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <header
        style={{
          background: "#fff",
          borderBottom: "1px solid #dfe1e6",
          padding: "0.75rem 1rem",
        }}
      >
        <div style={{ fontWeight: 700, marginBottom: "0.5rem" }}>M4 Notify · 工作坊骨架</div>
        <nav style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
          <NavLink to="/rules" style={navStyle}>
            规则
          </NavLink>
          <NavLink to="/dispatch" style={navStyle}>
            试发 / 历史
          </NavLink>
          <NavLink to="/channels" style={navStyle}>
            渠道测试
          </NavLink>
        </nav>
      </header>
      <main style={{ flex: 1, padding: "1rem", maxWidth: 960, margin: "0 auto", width: "100%" }}>
        <Routes>
          <Route path="/" element={<RulesPage />} />
          <Route path="/rules" element={<RulesPage />} />
          <Route path="/dispatch" element={<DispatchPage />} />
          <Route path="/channels" element={<ChannelsPage />} />
        </Routes>
      </main>
    </div>
  );
}
