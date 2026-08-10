"use client";

import React, { useEffect, useState } from "react";
import AppLayout from "@/components/layout/AppLayout";
import { useAuth } from "@/hooks/useAuth";
import { leadsApi } from "@/lib/api/leads";
import { companiesApi } from "@/lib/api/companies";
import { customersApi } from "@/lib/api/customers";
import { employeesApi } from "@/lib/api/employees";
import { Lead, Company, Customer, User as Employee } from "@/types";
import { Plus, Edit2, Trash2, X, RefreshCw, Filter } from "lucide-react";

const LEAD_STATUSES = ["new", "contacted", "qualified", "proposal", "won", "lost"];

export default function LeadsPage() {
  const { user } = useAuth();
  const [leads, setLeads] = useState<Lead[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [filterCompanyId, setFilterCompanyId] = useState("");
  const [filterCustomerId, setFilterCustomerId] = useState("");
  const [filterAssignedTo, setFilterAssignedTo] = useState("");
  const [filterStatus, setFilterStatus] = useState("");

  // Form states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [requirement, setRequirement] = useState("");
  const [status, setStatus] = useState("new");
  const [source, setSource] = useState("");
  const [notes, setNotes] = useState("");
  const [companyId, setCompanyId] = useState("");
  const [customerId, setCustomerId] = useState("");
  const [assignedTo, setAssignedTo] = useState("");
  const [formError, setFormError] = useState<string | null>(null);

  const isAdmin = user?.role === "admin";

  const fetchLeads = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const filters = {
        company_id: filterCompanyId || undefined,
        customer_id: filterCustomerId || undefined,
        assigned_to: filterAssignedTo || undefined,
        status: filterStatus || undefined,
      };
      const data = await leadsApi.list(filters);
      setLeads(data);
    } catch (err: any) {
      setError(err.message || "Failed to load leads.");
    } finally {
      setIsLoading(false);
    }
  };

  const fetchMetaData = async () => {
    try {
      const [compList, custList, empList] = await Promise.all([
        companiesApi.list(),
        customersApi.list(),
        employeesApi.list(),
      ]);
      setCompanies(compList);
      setCustomers(custList);
      setEmployees(empList);
    } catch (err: any) {
      console.error("Failed to load metadata", err);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, [filterCompanyId, filterCustomerId, filterAssignedTo, filterStatus]);

  useEffect(() => {
    fetchMetaData();
  }, []);

  const openCreateModal = () => {
    setEditingId(null);
    setName("");
    setEmail("");
    setPhone("");
    setRequirement("");
    setStatus("new");
    setSource("");
    setNotes("");
    setCompanyId(companies[0]?.id || "");
    setCustomerId("");
    setAssignedTo("");
    setFormError(null);
    setIsModalOpen(true);
  };

  const openEditModal = (lead: Lead) => {
    setEditingId(lead.id);
    setName(lead.name);
    setEmail(lead.email || "");
    setPhone(lead.phone || "");
    setRequirement(lead.requirement || "");
    setStatus(lead.status);
    setSource(lead.source || "");
    setNotes(lead.notes || "");
    setCompanyId(lead.company_id);
    setCustomerId(lead.customer_id || "");
    setAssignedTo(lead.assigned_to || "");
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    const payload = {
      company_id: companyId,
      customer_id: customerId || null,
      assigned_to: assignedTo || null,
      name,
      email: email || null,
      phone: phone || null,
      requirement: requirement || null,
      status,
      source: source || null,
      notes: notes || null,
    };

    try {
      if (editingId) {
        await leadsApi.update(editingId, payload);
      } else {
        await leadsApi.create(payload);
      }
      setIsModalOpen(false);
      fetchLeads();
    } catch (err: any) {
      if (err.status === 403) {
        setFormError("You don't have permission to perform this action.");
      } else {
        setFormError(err.message || "Failed to save lead.");
      }
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this lead?")) return;

    try {
      await leadsApi.delete(id);
      fetchLeads();
    } catch (err: any) {
      if (err.status === 403) {
        alert("You don't have permission to perform this action.");
      } else {
        alert(err.message || "Failed to delete lead.");
      }
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "new":
        return "bg-blue-500/10 text-blue-400 border-blue-800";
      case "contacted":
        return "bg-amber-500/10 text-amber-400 border-amber-800";
      case "qualified":
        return "bg-purple-500/10 text-purple-400 border-purple-800";
      case "proposal":
        return "bg-pink-500/10 text-pink-400 border-pink-800";
      case "won":
        return "bg-emerald-500/10 text-emerald-400 border-emerald-800";
      case "lost":
        return "bg-rose-500/10 text-rose-400 border-rose-800";
      default:
        return "bg-zinc-500/10 text-zinc-400 border-zinc-800";
    }
  };

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Leads</h1>
            <p className="text-sm text-zinc-400 mt-1">Track business opportunities, sales funnels, and prospect assignments.</p>
          </div>
          {isAdmin && (
            <button
              onClick={openCreateModal}
              className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 transition-colors shadow-md"
            >
              <Plus className="h-4 w-4" />
              <span>Add Lead</span>
            </button>
          )}
        </div>

        {/* Filters Section */}
        <div className="p-4 rounded-xl border border-zinc-800 bg-zinc-900/30 flex flex-wrap gap-4 items-center">
          <div className="flex items-center gap-2 text-zinc-400 text-xs font-semibold uppercase">
            <Filter className="h-4 w-4" />
            <span>Filters</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 flex-1">
            <select
              value={filterCompanyId}
              onChange={(e) => setFilterCompanyId(e.target.value)}
              className="rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-xs text-white focus:outline-none"
            >
              <option value="">All Companies</option>
              {companies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
            <select
              value={filterCustomerId}
              onChange={(e) => setFilterCustomerId(e.target.value)}
              className="rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-xs text-white focus:outline-none"
            >
              <option value="">All Customers</option>
              {customers.map((c) => (
                <option key={c.id} value={c.id}>
                  {`${c.first_name} ${c.last_name}`}
                </option>
              ))}
            </select>
            <select
              value={filterAssignedTo}
              onChange={(e) => setFilterAssignedTo(e.target.value)}
              className="rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-xs text-white focus:outline-none"
            >
              <option value="">All Assignees</option>
              {employees.map((e) => (
                <option key={e.id} value={e.id}>
                  {e.email}
                </option>
              ))}
            </select>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-xs text-white focus:outline-none capitalize"
            >
              <option value="">All Statuses</option>
              {LEAD_STATUSES.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
        </div>

        {error && (
          <div className="rounded-lg bg-red-950/30 border border-red-800 p-4 flex justify-between items-center text-red-400">
            <span>{error}</span>
            <button onClick={fetchLeads} className="p-1 hover:bg-red-900/20 rounded-md">
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>
        )}

        {isLoading ? (
          <div className="flex h-48 items-center justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
          </div>
        ) : leads.length === 0 ? (
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/20 p-12 text-center text-zinc-400">
            <p className="text-lg font-semibold text-white">No leads found</p>
            <p className="text-sm mt-1">Get started by creating your first sales lead opportunity.</p>
            {isAdmin && (
              <button
                onClick={openCreateModal}
                className="mt-4 inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 px-4 py-2 text-sm font-semibold text-white transition-colors"
              >
                Create Lead
              </button>
            )}
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-900/30">
            <table className="min-w-full divide-y divide-zinc-850">
              <thead>
                <tr className="text-left text-xs font-semibold text-zinc-400 uppercase bg-zinc-900/50">
                  <th className="px-6 py-4">Opportunity</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4">Company</th>
                  <th className="px-6 py-4">Customer Contact</th>
                  <th className="px-6 py-4">Assigned To</th>
                  <th className="px-6 py-4">Source</th>
                  {isAdmin && <th className="px-6 py-4 text-right">Actions</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-850 text-sm text-zinc-300">
                {leads.map((lead) => {
                  const companyName = companies.find((c) => c.id === lead.company_id)?.name || "—";
                  const customer = customers.find((c) => c.id === lead.customer_id);
                  const customerName = customer ? `${customer.first_name} ${customer.last_name}` : "—";
                  const assignee = employees.find((e) => e.id === lead.assigned_to);
                  return (
                    <tr key={lead.id} className="hover:bg-zinc-900/20">
                      <td className="px-6 py-4">
                        <div>
                          <p className="font-medium text-white">{lead.name}</p>
                          <p className="text-xs text-zinc-500 mt-0.5">{lead.requirement || "No requirement notes"}</p>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border capitalize ${getStatusBadge(lead.status)}`}>
                          {lead.status}
                        </span>
                      </td>
                      <td className="px-6 py-4">{companyName}</td>
                      <td className="px-6 py-4">{customerName}</td>
                      <td className="px-6 py-4 text-xs">
                        {assignee ? (
                          <div className="flex items-center gap-1.5">
                            <div className="h-5 w-5 rounded-full bg-indigo-950 flex items-center justify-center text-[8px] text-indigo-300 font-semibold border border-indigo-900">
                              {assignee.email.substring(0, 2).toUpperCase()}
                            </div>
                            <span>{assignee.email}</span>
                          </div>
                        ) : (
                          <span className="text-zinc-500">Unassigned</span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-xs text-zinc-400">{lead.source || "—"}</td>
                      {isAdmin && (
                        <td className="px-6 py-4 text-right space-x-2">
                          <button
                            onClick={() => openEditModal(lead)}
                            className="inline-flex p-1.5 rounded-lg border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-100 transition-colors"
                          >
                            <Edit2 className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(lead.id)}
                            className="inline-flex p-1.5 rounded-lg border border-red-950 bg-zinc-900 hover:bg-red-950/20 text-red-400 hover:text-red-300 transition-colors"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </td>
                      )}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* Modal for Create/Update */}
        {isModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-zinc-950/80 backdrop-blur-sm">
            <div className="relative w-full max-w-lg rounded-2xl border border-zinc-800 bg-zinc-900 p-6 shadow-2xl">
              <button
                onClick={() => setIsModalOpen(false)}
                className="absolute top-4 right-4 text-zinc-400 hover:text-zinc-100"
              >
                <X className="h-5 w-5" />
              </button>
              <h2 className="text-lg font-bold text-white mb-4">
                {editingId ? "Edit Lead" : "Add Lead"}
              </h2>

              {formError && (
                <div className="rounded-md bg-red-950/30 border border-red-800 p-3 text-sm text-red-400 mb-4">
                  {formError}
                </div>
              )}

              <form onSubmit={handleSave} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Lead Name *</label>
                    <input
                      type="text"
                      required
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                      placeholder="Enterprise Integration deal"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Status *</label>
                    <select
                      value={status}
                      onChange={(e) => setStatus(e.target.value)}
                      required
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm capitalize"
                    >
                      {LEAD_STATUSES.map((s) => (
                        <option key={s} value={s}>
                          {s}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Company Association *</label>
                    <select
                      value={companyId}
                      onChange={(e) => setCompanyId(e.target.value)}
                      required
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    >
                      <option value="" disabled>Select Company</option>
                      {companies.map((c) => (
                        <option key={c.id} value={c.id}>
                          {c.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Customer Contact</label>
                    <select
                      value={customerId}
                      onChange={(e) => setCustomerId(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    >
                      <option value="">No Contact</option>
                      {customers.map((c) => (
                        <option key={c.id} value={c.id}>
                          {`${c.first_name} ${c.last_name}`}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Assignee</label>
                    <select
                      value={assignedTo}
                      onChange={(e) => setAssignedTo(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    >
                      <option value="">Unassigned</option>
                      {employees.map((e) => (
                        <option key={e.id} value={e.id}>
                          {e.email}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Lead Source</label>
                    <input
                      type="text"
                      value={source}
                      onChange={(e) => setSource(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                      placeholder="LinkedIn, Conference..."
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Email</label>
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                      placeholder="deal@example.com"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Phone</label>
                    <input
                      type="text"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                      placeholder="123-456-7890"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Requirement Summary</label>
                  <input
                    type="text"
                    value={requirement}
                    onChange={(e) => setRequirement(e.target.value)}
                    className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    placeholder="Custom database setup and migrations"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Notes</label>
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm h-16 resize-none"
                  />
                </div>

                <div className="flex justify-end gap-3 pt-4 border-t border-zinc-800">
                  <button
                    type="button"
                    onClick={() => setIsModalOpen(false)}
                    className="rounded-lg border border-zinc-700 bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-zinc-300 hover:bg-zinc-800 hover:text-white transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-500 transition-colors"
                  >
                    Save
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
