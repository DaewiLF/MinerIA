import { apiClient } from "./apiClient";

export interface LoginPayload {
  email: string;
  password: string;
  role: "admin" | "analyst";
}

export interface LoginResponse {
  token: string;
  user: {
    id: number;
    email: string;
    role: string;
    name: string;
  };
}

export async function loginApi(data: LoginPayload): Promise<LoginResponse> {
  const resp = await apiClient.post<LoginResponse>("/auth/login", data);
  return resp.data;
}
