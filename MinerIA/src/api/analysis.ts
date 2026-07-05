import { apiClient } from "./apiClient";

export interface AnalysisSummary {
  id: number;
  date: string;
  zone: string;
  category: string;
  riskLevel: string;
  copperGrade: string;
  status: string;
}

export interface AnalysisModelOption {
  id: string;
  name: string;
  description: string;
}

export interface AnalysisDetail {
  id: number;
  date: string;
  zone: string;
  category: string;
  riskLevel: string;
  copperGrade: string;
  aiSummary: string;
  recommendations: string[];
  metadata: Record<string, unknown>;
  imageUrl: string;
  gradcamUrl?: string | null;
  status: string;
}

export interface VideoAnalysisResponse {
  id_video: number;
  video_id: string;
  duracion_total_segundos: number;
  total_frames_analizados: number;
  total_hallazgos: number;
  linea_temporal: TimelineEntry[];
  detalle_hallazgos: TimelineEntry[];
  ruta_video_original: string;
  reporte_pdf: string | null;
}

export interface TimelineEntry {
  segundo: number;
  timestamp: string;
  prediccion: string;
  confianza: number;
  frame_url: string;
  gradcam_url: string | null;
}

export interface QueueItem {
  id: number;
  estado: "pendiente" | "procesando" | "completado" | "error";
  error: string | null;
  fecha_creacion: string;
  fecha_procesamiento: string | null;
}

export interface BatchUploadResponse {
  total: number;
  items: QueueItem[];
}

export async function uploadAnalysis(
  file: File,
  metadata: Record<string, string | number>,
  modelId = "copper"
): Promise<AnalysisDetail> {
  const form = new FormData();
  form.append("file", file);
  form.append("metadata", JSON.stringify(metadata));
  form.append("model_id", modelId);

  const { data } = await apiClient.post("/analysis/upload", form);
  return data;
}

export async function getAnalysisModels(): Promise<AnalysisModelOption[]> {
  const { data } = await apiClient.get("/analysis/models");
  return data;
}

export async function analyzeVideo(file: File): Promise<VideoAnalysisResponse> {
  const form = new FormData();
  form.append("file", file);
  const { data } = await apiClient.post("/v1/analyze-video", form);
  return data;
}

export async function getAnalysisHistory(): Promise<AnalysisSummary[]> {
  const { data } = await apiClient.get("/analysis/history");
  return data;
}

export async function getAnalysisById(
  id: string
): Promise<AnalysisDetail> {
  const { data } = await apiClient.get(`/analysis/${id}`);
  return data;
}

export async function uploadBatch(
  files: File[],
  metadata: Record<string, string | number>,
  modelId = "copper"
): Promise<BatchUploadResponse> {
  const form = new FormData();
  for (const file of files) {
    form.append("files", file);
  }
  form.append("metadata", JSON.stringify(metadata));
  form.append("model_id", modelId);

  const { data } = await apiClient.post("/analysis/upload-batch", form);
  return data;
}

export async function getQueueStatus(): Promise<QueueItem[]> {
  const { data } = await apiClient.get("/analysis/queue");
  return data;
}

// ---------- Dashboard Stats ----------

export interface DashboardStats {
  analisis_hoy: number;
  analisis_semana: number;
  confianza_promedio: number;
  alertas_criticas: number;
  en_cola: number;
  modelos_activos: number;
  actividad_semanal: { fecha: string; total: number }[];
  distribucion_mineral: { nombre: string; total: number }[];
  ultimos_analisis: {
    id: number;
    zone: string;
    copperGrade: string;
    confidence: number;
    riskLevel: string;
    date: string;
  }[];
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const { data } = await apiClient.get("/analysis/stats");
  return data;
}

// ---------- Video History ----------

export interface VideoHistorySummary {
  id_video: number;
  nombre_archivo: string;
  duracion_segundos: number;
  total_frames_analizados: number;
  total_hallazgos: number;
  fecha_analisis: string;
  reporte_pdf: string | null;
}

export interface VideoHistoryDetail {
  id_video: number;
  nombre_archivo: string;
  ruta_video: string;
  duracion_segundos: number;
  total_frames_analizados: number;
  total_hallazgos: number;
  linea_temporal: Array<{
    segundo: number;
    timestamp: string;
    prediccion: string;
    confianza: number;
    frame_url: string;
    gradcam_url: string | null;
  }>;
  detalle_hallazgos: Array<{
    segundo: number;
    timestamp: string;
    prediccion: string;
    confianza: number;
    frame_url: string;
    gradcam_url: string | null;
  }>;
  fecha_analisis: string;
  reporte_pdf: string | null;
}

export async function getVideoHistory(): Promise<VideoHistorySummary[]> {
  const { data } = await apiClient.get("/v1/video-history");
  return data;
}

export async function getVideoDetail(id: number): Promise<VideoHistoryDetail> {
  const { data } = await apiClient.get(`/v1/video-history/${id}`);
  return data;
}

export async function downloadVideoPdf(id: number): Promise<void> {
  const { data, headers } = await apiClient.get(`/v1/video-history/${id}/pdf`, {
    responseType: "blob",
  });
  const disposition = headers["content-disposition"] || "";
  const match = disposition.match(/filename="?(.+?)"?$/);
  const filename = match?.[1] || `reporte_video_${id}.pdf`;
  const url = URL.createObjectURL(data);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

