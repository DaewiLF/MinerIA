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

export interface AnalysisDetail {
  id: number;
  date: string;
  zone: string;
  category: string;
  riskLevel: string;
  copperGrade: string;
  aiSummary: string;
  recommendations: string[];
  metadata: Record<string, string | number>;
  imageUrl: string;
  status: string;
}

export interface VideoFinding {
  segundo_del_video: number;
  timestamp: string;
  confianza: number;
  frame_asociado: string;
}

export interface VideoAnalysisResponse {
  video_id: string;
  duracion_total_segundos: number;
  total_hallazgos: number;
  detalle_hallazgos: VideoFinding[];
  ruta_video_original: string;
}

export async function uploadAnalysis(
  file: File,
  metadata: Record<string, string | number>
): Promise<AnalysisDetail> {
  const form = new FormData();
  form.append("file", file);
  form.append("metadata", JSON.stringify(metadata));

  const { data } = await apiClient.post("/analysis/upload", form);
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
