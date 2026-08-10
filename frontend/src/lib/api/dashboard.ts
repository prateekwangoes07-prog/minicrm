import { apiClient } from "./client";
import { DashboardSummaryResponse } from "@/types";

export const dashboardApi = {
  summary: () => apiClient.get<DashboardSummaryResponse>("/dashboard/summary"),
};
