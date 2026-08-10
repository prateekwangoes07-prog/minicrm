import { apiClient } from "./client";
import { Lead } from "@/types";

export interface LeadFilter {
  company_id?: string;
  customer_id?: string;
  assigned_to?: string;
  status?: string;
}

export const leadsApi = {
  list: (filters?: LeadFilter) => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, val]) => {
        if (val) params.append(key, val);
      });
    }
    const query = params.toString() ? `?${params.toString()}` : "";
    return apiClient.get<Lead[]>(`/leads${query}`);
  },
  get: (id: string) => apiClient.get<Lead>(`/leads/${id}`),
  create: (data: any) => apiClient.post<Lead>("/leads", data),
  update: (id: string, data: any) => apiClient.put<Lead>(`/leads/${id}`, data),
  delete: (id: string) => apiClient.delete<void>(`/leads/${id}`),
};
