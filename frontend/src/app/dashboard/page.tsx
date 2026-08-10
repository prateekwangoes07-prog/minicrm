"use client";

import React, { useEffect, useState } from "react";
import AppLayout from "@/components/layout/AppLayout";
import { dashboardApi } from "@/lib/api/dashboard";
import { DashboardSummaryResponse } from "@/types";
import { Building2, Users2, UserSquare2, LineChart, Target } from "lucide-react";

export default function DashboardPage() {
  const [data, setData] = useState<DashboardSummaryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSummary = async () => {
    try {
      const summary = await dashboardApi.summary();
      setData(summary);
    } catch (err: any) {
      setError(err.message || "Failed to load dashboard statistics.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  if (isLoading) {
    return (
      <AppLayout>
        <div className="flex h-64 items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
        </div>
      </AppLayout>
    );
  }

  if (error || !data) {
    return (
      <AppLayout>
        <div className="rounded-lg bg-red-950/30 border border-red-800 p-6 text-center text-red-400">
          <p className="font-semibold">Error Loading Dashboard</p>
          <p className="text-sm mt-1">{error || "Something went wrong"}</p>
          <button onClick={fetchSummary} className="mt-4 px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded-lg text-sm font-medium">
            Try Again
          </button>
        </div>
      </AppLayout>
    );
  }

  const statCards = [
    { name: "Total Companies", value: data.total_companies, icon: Building2, color: "text-blue-400 bg-blue-950/40 border-blue-900" },
    { name: "Total Employees", value: data.total_employees, icon: Users2, color: "text-purple-400 bg-purple-950/40 border-purple-900" },
    { name: "Total Customers", value: data.total_customers, icon: UserSquare2, color: "text-teal-400 bg-teal-950/40 border-teal-900" },
    { name: "Total Leads", value: data.total_leads, icon: LineChart, color: "text-indigo-400 bg-indigo-950/40 border-indigo-900" },
    { name: "Conversion Rate", value: `${(data.lead_conversion_rate * 100).toFixed(1)}%`, icon: Target, color: "text-emerald-400 bg-emerald-950/40 border-emerald-900" },
  ];

  const statuses = [
    { label: "New", value: data.leads_by_status.new, color: "border-blue-800/50 bg-blue-950/20 text-blue-400" },
    { label: "Contacted", value: data.leads_by_status.contacted, color: "border-amber-800/50 bg-amber-950/20 text-amber-400" },
    { label: "Qualified", value: data.leads_by_status.qualified, color: "border-purple-800/50 bg-purple-950/20 text-purple-400" },
    { label: "Proposal", value: data.leads_by_status.proposal, color: "border-pink-800/50 bg-pink-950/20 text-pink-400" },
    { label: "Won", value: data.leads_by_status.won, color: "border-emerald-800/50 bg-emerald-950/20 text-emerald-400" },
    { label: "Lost", value: data.leads_by_status.lost, color: "border-rose-800/50 bg-rose-950/20 text-rose-400" },
  ];

  return (
    <AppLayout>
      <div className="space-y-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Dashboard Summary</h1>
          <p className="text-zinc-400 text-sm mt-1">Real-time MiniCRM performance metrics and analytics.</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5">
          {statCards.map((card) => (
            <div key={card.name} className={`p-6 rounded-xl border border-zinc-800 bg-zinc-900/50 shadow-sm flex items-center justify-between gap-4`}>
              <div className="space-y-1">
                <p className="text-xs font-medium text-zinc-400">{card.name}</p>
                <p className="text-2xl font-semibold text-white">{card.value}</p>
              </div>
              <div className={`p-3 rounded-lg border ${card.color.split(" ").slice(1).join(" ")}`}>
                <card.icon className={`h-5 w-5 ${card.color.split(" ")[0]}`} />
              </div>
            </div>
          ))}
        </div>

        {/* Breakdown Section */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          {/* Leads by Status */}
          <div className="p-6 rounded-xl border border-zinc-800 bg-zinc-900/30">
            <h3 className="text-base font-semibold text-white mb-6">Leads by Status</h3>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
              {statuses.map((status) => (
                <div key={status.label} className={`p-4 rounded-xl border text-center ${status.color}`}>
                  <p className="text-xs opacity-75 font-medium">{status.label}</p>
                  <p className="text-xl font-bold mt-1">{status.value}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Lead Assignments */}
          <div className="p-6 rounded-xl border border-zinc-800 bg-zinc-900/30">
            <h3 className="text-base font-semibold text-white mb-6">Employee Lead Assignments</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-zinc-800">
                <thead>
                  <tr className="text-left text-xs font-semibold text-zinc-400">
                    <th className="pb-3">Employee</th>
                    <th className="pb-3 text-right">Assigned Leads</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800 text-sm">
                  {data.leads_assigned_to_employees.length === 0 ? (
                    <tr>
                      <td colSpan={2} className="py-4 text-center text-zinc-500 text-xs">
                        No employees registered or assigned.
                      </td>
                    </tr>
                  ) : (
                    data.leads_assigned_to_employees.map((emp, index) => (
                      <tr key={emp.employee_id || index} className="text-zinc-300">
                        <td className="py-3 flex items-center gap-2">
                          <div className="h-6 w-6 rounded-full bg-indigo-950 flex items-center justify-center text-[10px] text-indigo-300 font-medium">
                            {emp.employee_email?.substring(0, 2).toUpperCase()}
                          </div>
                          <span>{emp.employee_email}</span>
                        </td>
                        <td className="py-3 text-right font-medium text-white">{emp.lead_count}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
