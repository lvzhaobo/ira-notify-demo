import axios from "axios";

const api = axios.create({
  baseURL: "/api/v1",
  timeout: 15000,
});

export async function fetchHealth() {
  const { data } = await api.get("/notify/health");
  return data;
}

export async function fetchRules() {
  return api.get("/notify/rules");
}
