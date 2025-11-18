import { createContext } from "react";
import type { LoginResponse } from "../api/auth";

export interface AuthContextType {
  user: LoginResponse["user"] | null;
  token: string | null;
  login: (data: LoginResponse) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  login: () => {},
  logout: () => {},
});
