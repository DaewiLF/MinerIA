const API_BASE = (import.meta.env.VITE_API_URL ?? "http://localhost:8000").replace(/\/+$/, "");

export function toAbsoluteUrl(path: string | null | undefined): string | undefined {
  if (!path) return undefined;
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  const separator = path.startsWith("/") ? "" : "/";
  return `${API_BASE}${separator}${path}`;
}
