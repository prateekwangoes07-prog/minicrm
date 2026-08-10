import { apiClient } from "./client";
import { User } from "@/types";

export const employeesApi = {
  list: () => apiClient.get<User[]>("/employees"),
  get: (id: string) => apiClient.get<User>(`/employees/${id}`),
  create: (data: any) => apiClient.post<User>("/employees", data),
  update: (id: string, data: any) => apiClient.put<User>(`/employees/${id}`, data),
  delete: (id: string) => apiClient.delete<void>(`/employees/${id}`),
};
