import { apiClient } from "./client";
import { Customer } from "@/types";

export const customersApi = {
  list: () => apiClient.get<Customer[]>("/customers"),
  get: (id: string) => apiClient.get<Customer>(`/customers/${id}`),
  create: (data: any) => apiClient.post<Customer>("/customers", data),
  update: (id: string, data: any) => apiClient.put<Customer>(`/customers/${id}`, data),
  delete: (id: string) => apiClient.delete<void>(`/customers/${id}`),
};
