import { useState, useEffect } from "react";
import { AuthContext } from "./AuthContext";
import type { LoginResponse } from "../api/auth";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<LoginResponse["user"] | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedUser = localStorage.getItem("user");

    // evitar warning de eslint (setState dentro del effect)
    if (savedToken && savedUser) {
      setTimeout(() => {
        setToken(savedToken);
        setUser(JSON.parse(savedUser));
      }, 0);
    }
  }, []);

  const login = (data: LoginResponse) => {
    setUser(data.user);
    setToken(data.token);

    localStorage.setItem("token", data.token);
    localStorage.setItem("user", JSON.stringify(data.user));
  };

  const logout = () => {
    setUser(null);
    setToken(null);

    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
