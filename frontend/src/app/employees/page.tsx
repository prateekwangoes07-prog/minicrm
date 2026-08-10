"use client";

import React, { useEffect, useState } from "react";
import AppLayout from "@/components/layout/AppLayout";
import { useAuth } from "@/hooks/useAuth";
import { employeesApi } from "@/lib/api/employees";
import { companiesApi } from "@/lib/api/companies";
import { User as Employee, Company } from "@/types";
import { Plus, Edit2, Trash2, X, RefreshCw } from "lucide-react";
import { useRouter } from "next/navigation";

export default function EmployeesPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [companyId, setCompanyId] = useState("");
  const [isActive, setIsActive] = useState(true);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    if (user && user.role !== "admin") {
      router.push("/dashboard");
    }
  }, [user, router]);

  const fetchData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [empList, companyList] = await Promise.all([
        employeesApi.list(),
        companiesApi.list(),
      ]);
      setEmployees(empList);
      setCompanies(companyList);
    } catch (err: any) {
      setError(err.message || "Failed to load employees and companies.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const openCreateModal = () => {
    setEditingId(null);
    setEmail("");
    setPassword("");
    setFirstName("");
    setLastName("");
    setCompanyId(companies[0]?.id || "");
    setIsActive(true);
    setFormError(null);
    setIsModalOpen(true);
  };

  const openEditModal = (emp: Employee) => {
    setEditingId(emp.id);
    setEmail(emp.email);
    setPassword("");
    setFirstName(emp.first_name || "");
    setLastName(emp.last_name || "");
    setCompanyId((emp as any).company_id || "");
    setIsActive(emp.is_active);
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    if (!editingId && (!password || password.length < 8)) {
      setFormError("Password is required and must be at least 8 characters long.");
      return;
    }

    const payload: any = {
      email,
      first_name: firstName || null,
      last_name: lastName || null,
      company_id: companyId || null,
      is_active: isActive,
    };

    if (!editingId || password) {
      payload.password = password;
    }

    try {
      if (editingId) {
        const updatePayload: any = {
          first_name: payload.first_name,
          last_name: payload.last_name,
          company_id: payload.company_id,
          is_active: payload.is_active,
        };
        if (password) {
          updatePayload.password = password;
        }
        await employeesApi.update(editingId, updatePayload);
      } else {
        await employeesApi.create(payload);
      }
      setIsModalOpen(false);
      fetchData();
    } catch (err: any) {
      setFormError(err.message || "Failed to save employee.");
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this employee?")) return;

    try {
      await employeesApi.delete(id);
      fetchData();
    } catch (err: any) {
      alert(err.message || "Failed to delete employee.");
    }
  };

  if (!user || user.role !== "admin") {
    return null;
  }

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Employees</h1>
            <p className="text-sm text-zinc-400 mt-1">Manage staff users, roles, permissions, and corporate association.</p>
          </div>
          <button
            onClick={openCreateModal}
            className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 transition-colors shadow-md"
          >
            <Plus className="h-4 w-4" />
            <span>Add Employee</span>
          </button>
        </div>

        {error && (
          <div className="rounded-lg bg-red-950/30 border border-red-800 p-4 flex justify-between items-center text-red-400">
            <span>{error}</span>
            <button onClick={fetchData} className="p-1 hover:bg-red-900/20 rounded-md">
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>
        )}

        {isLoading ? (
          <div className="flex h-48 items-center justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
          </div>
        ) : employees.length === 0 ? (
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/20 p-12 text-center text-zinc-400">
            <p className="text-lg font-semibold text-white">No employees found</p>
            <p className="text-sm mt-1">Get started by creating your first employee user profile.</p>
            <button
              onClick={openCreateModal}
              className="mt-4 inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 px-4 py-2 text-sm font-semibold text-white transition-colors"
            >
              Create Employee
            </button>
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-900/30">
            <table className="min-w-full divide-y divide-zinc-850">
              <thead>
                <tr className="text-left text-xs font-semibold text-zinc-400 uppercase bg-zinc-900/50">
                  <th className="px-6 py-4">Name</th>
                  <th className="px-6 py-4">Email</th>
                  <th className="px-6 py-4">Company</th>
                  <th className="px-6 py-4">Role</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-850 text-sm text-zinc-300">
                {employees.map((emp) => {
                  const companyName = companies.find((c) => c.id === (emp as any).company_id)?.name || "—";
                  return (
                    <tr key={emp.id} className="hover:bg-zinc-900/20">
                      <td className="px-6 py-4 font-medium text-white">
                        {emp.first_name || emp.last_name ? `${emp.first_name || ""} ${emp.last_name || ""}`.trim() : "—"}
                      </td>
                      <td className="px-6 py-4">{emp.email}</td>
                      <td className="px-6 py-4">{companyName}</td>
                      <td className="px-6 py-4">
                        <span className="px-2 py-0.5 rounded text-xs font-medium bg-zinc-800 text-zinc-300 border border-zinc-700 capitalize">
                          {emp.role}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold border ${
                            emp.is_active
                              ? "bg-emerald-500/10 text-emerald-400 border-emerald-800"
                              : "bg-zinc-500/10 text-zinc-400 border-zinc-800"
                          }`}
                        >
                          {emp.is_active ? "Active" : "Inactive"}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right space-x-2">
                        <button
                          onClick={() => openEditModal(emp)}
                          className="inline-flex p-1.5 rounded-lg border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-100 transition-colors"
                        >
                          <Edit2 className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(emp.id)}
                          className="inline-flex p-1.5 rounded-lg border border-red-950 bg-zinc-900 hover:bg-red-950/20 text-red-400 hover:text-red-300 transition-colors"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </td>
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
                {editingId ? "Edit Employee" : "Add Employee"}
              </h2>

              {formError && (
                <div className="rounded-md bg-red-950/30 border border-red-800 p-3 text-sm text-red-400 mb-4">
                  {formError}
                </div>
              )}

              <form onSubmit={handleSave} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">First Name</label>
                    <input
                      type="text"
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Last Name</label>
                    <input
                      type="text"
                      value={lastName}
                      onChange={(e) => setLastName(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Email *</label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">
                    Password {editingId && "(leave blank to keep current)"}
                  </label>
                  <input
                    type="password"
                    required={!editingId}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    placeholder="Min. 8 characters"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Company Association</label>
                  <select
                    value={companyId}
                    onChange={(e) => setCompanyId(e.target.value)}
                    className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                  >
                    <option value="">No Company</option>
                    {companies.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="flex items-center gap-2 pt-2">
                  <input
                    type="checkbox"
                    id="is-active"
                    checked={isActive}
                    onChange={(e) => setIsActive(e.target.checked)}
                    className="h-4 w-4 rounded border-zinc-700 bg-zinc-800 text-indigo-600 focus:ring-indigo-500"
                  />
                  <label htmlFor="is-active" className="text-sm font-medium text-zinc-300">
                    Mark as Active
                  </label>
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
