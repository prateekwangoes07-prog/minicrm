export type UserRole = "admin" | "employee";

export interface User {
  id: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
  role: UserRole;
  is_active: boolean;
  is_email_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface Company {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  industry: string | null;
  website: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Customer {
  id: string;
  company_id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string | null;
  address: string | null;
  notes: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Lead {
  id: string;
  company_id: string;
  customer_id: string | null;
  assigned_to: string | null;
  name: string;
  email: string | null;
  phone: string | null;
  requirement: string | null;
  status: "new" | "contacted" | "qualified" | "proposal" | "won" | "lost";
  source: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface DashboardLeadStatus {
  new: number;
  contacted: number;
  qualified: number;
  proposal: number;
  won: number;
  lost: number;
}

export interface EmployeeLeadCount {
  employee_id: string | null;
  employee_email: string | null;
  lead_count: number;
}

export interface DashboardSummaryResponse {
  total_companies: number;
  total_employees: number;
  total_customers: number;
  total_leads: number;
  leads_by_status: DashboardLeadStatus;
  lead_conversion_rate: number;
  leads_assigned_to_employees: EmployeeLeadCount[];
}
