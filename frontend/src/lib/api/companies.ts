import { apiClient } from "./client";
import { Company } from "@/types";

export const companiesApi = {
  list: () => apiClient.get<Company[]>("/companies"),
  get: (id: string) => apiClient.get<Company>(`/companies/${id}`),
  create: (data: any) => apiClient.post<Company>("/companies", data),
  update: (id: string, data: any) => apiClient.put<Company>(`/companies/${id}`, data),
  delete: (id: string) => apiClient.delete<void>(`/companies/${id}`),
};
