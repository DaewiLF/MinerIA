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
  status: string;
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
