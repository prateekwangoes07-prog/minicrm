import { apiClient } from "./client";
import { User } from "@/types";

export const authApi = {
  login: (data: any) => apiClient.post<{ access_token: string }>("/auth/login", data),
  signup: (data: any) => apiClient.post<User>("/auth/signup", data),
  logout: () => apiClient.post<{ message: string }>("/auth/logout"),
  me: () => apiClient.get<User>("/auth/me"),
};
