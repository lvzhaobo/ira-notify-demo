import axios from "axios";

const api = axios.create({
  baseURL: "/api/v1",
  timeout: 15000,
});

export async function fetchHealth() {
  const { data } = await api.get("/notify/health");
  return data;
}

export async function fetchRules(params) {
  return api.get("/notify/rules", { params });
}

export async function fetchRule(ruleId) {
  const { data } = await api.get(`/notify/rules/${ruleId}`);
  return data;
}

export async function createRule(body) {
  const { data } = await api.post("/notify/rules", body);
  return data;
}

export async function updateRule(ruleId, body) {
  const { data } = await api.patch(`/notify/rules/${ruleId}`, body);
  return data;
}

export async function deleteRule(ruleId) {
  await api.delete(`/notify/rules/${ruleId}`);
}
