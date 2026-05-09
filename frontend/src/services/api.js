import axios from "axios";

const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8001";

export const api = axios.create({
  baseURL: BASE,
  timeout: 60_000,
});

export async function uploadDataset(file) {
  const fd = new FormData();
  fd.append("file", file);
  const { data } = await api.post("/upload", fd, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function askAgent(query, context = null) {
  const { data } = await api.post("/query", { query, context });
  return data;
}
