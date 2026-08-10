"use client";

import React, { useEffect, useState } from "react";
import AppLayout from "@/components/layout/AppLayout";
import { useAuth } from "@/hooks/useAuth";
import { companiesApi } from "@/lib/api/companies";
import { Company } from "@/types";
import { Plus, Edit2, Trash2, X, RefreshCw } from "lucide-react";

export default function CompaniesPage() {
  const { user } = useAuth();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [industry, setIndustry] = useState("");
  const [website, setWebsite] = useState("");
  const [isActive, setIsActive] = useState(true);
  const [formError, setFormError] = useState<string | null>(null);

  const isAdmin = user?.role === "admin";

  const fetchCompanies = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await companiesApi.list();
      setCompanies(data);
    } catch (err: any) {
      setError(err.message || "Failed to load companies.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCompanies();
  }, []);

  const openCreateModal = () => {
    setEditingId(null);
    setName("");
    setEmail("");
    setPhone("");
    setIndustry("");
    setWebsite("");
    setIsActive(true);
    setFormError(null);
    setIsModalOpen(true);
  };

  const openEditModal = (company: Company) => {
    setEditingId(company.id);
    setName(company.name);
    setEmail(company.email);
    setPhone(company.phone || "");
    setIndustry(company.industry || "");
    setWebsite(company.website || "");
    setIsActive(company.is_active);
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    const payload = {
      name,
      email,
      phone: phone || null,
      industry: industry || null,
      website: website || null,
      is_active: isActive,
    };

    try {
      if (editingId) {
        await companiesApi.update(editingId, payload);
      } else {
        await companiesApi.create(payload);
      }
      setIsModalOpen(false);
      fetchCompanies();
    } catch (err: any) {
      setFormError(err.message || "Failed to save company details.");
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this company?")) return;

    try {
      await companiesApi.delete(id);
      fetchCompanies();
    } catch (err: any) {
      alert(err.message || "Failed to delete company.");
    }
  };

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Companies</h1>
            <p className="text-sm text-zinc-400 mt-1">Manage partner organizations, clients, and corporate profiles.</p>
          </div>
          {isAdmin && (
            <button
              onClick={openCreateModal}
              className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 transition-colors shadow-md"
            >
              <Plus className="h-4 w-4" />
              <span>Add Company</span>
            </button>
          )}
        </div>

        {error && (
          <div className="rounded-lg bg-red-950/30 border border-red-800 p-4 flex justify-between items-center text-red-400">
            <span>{error}</span>
            <button onClick={fetchCompanies} className="p-1 hover:bg-red-900/20 rounded-md">
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>
        )}

        {isLoading ? (
          <div className="flex h-48 items-center justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
          </div>
        ) : companies.length === 0 ? (
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/20 p-12 text-center text-zinc-400">
            <p className="text-lg font-semibold text-white">No companies found</p>
            <p className="text-sm mt-1">Get started by creating your first client company record.</p>
            {isAdmin && (
              <button
                onClick={openCreateModal}
                className="mt-4 inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 px-4 py-2 text-sm font-semibold text-white transition-colors"
              >
                Create Company
              </button>
            )}
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-900/30">
            <table className="min-w-full divide-y divide-zinc-850">
              <thead>
                <tr className="text-left text-xs font-semibold text-zinc-400 uppercase bg-zinc-900/50">
                  <th className="px-6 py-4">Company Name</th>
                  <th className="px-6 py-4">Email</th>
                  <th className="px-6 py-4">Phone</th>
                  <th className="px-6 py-4">Industry</th>
                  <th className="px-6 py-4">Website</th>
                  <th className="px-6 py-4">Status</th>
                  {isAdmin && <th className="px-6 py-4 text-right">Actions</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-850 text-sm text-zinc-300">
                {companies.map((company) => (
                  <tr key={company.id} className="hover:bg-zinc-900/20">
                    <td className="px-6 py-4 font-medium text-white">{company.name}</td>
                    <td className="px-6 py-4">{company.email}</td>
                    <td className="px-6 py-4">{company.phone || "—"}</td>
                    <td className="px-6 py-4">
                      {company.industry ? (
                        <span className="px-2 py-1 rounded bg-zinc-800 text-zinc-300 text-xs font-medium border border-zinc-700">
                          {company.industry}
                        </span>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td className="px-6 py-4">
                      {company.website ? (
                        <a
                          href={company.website.startsWith("http") ? company.website : `https://${company.website}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-indigo-400 hover:underline text-xs"
                        >
                          {company.website}
                        </a>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold border ${
                          company.is_active
                            ? "bg-emerald-500/10 text-emerald-400 border-emerald-800"
                            : "bg-zinc-500/10 text-zinc-400 border-zinc-800"
                        }`}
                      >
                        {company.is_active ? "Active" : "Inactive"}
                      </span>
                    </td>
                    {isAdmin && (
                      <td className="px-6 py-4 text-right space-x-2">
                        <button
                          onClick={() => openEditModal(company)}
                          className="inline-flex p-1.5 rounded-lg border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-100 transition-colors"
                        >
                          <Edit2 className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(company.id)}
                          className="inline-flex p-1.5 rounded-lg border border-red-950 bg-zinc-900 hover:bg-red-950/20 text-red-400 hover:text-red-300 transition-colors"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
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
                {editingId ? "Edit Company" : "Add Company"}
              </h2>

              {formError && (
                <div className="rounded-md bg-red-950/30 border border-red-800 p-3 text-sm text-red-400 mb-4">
                  {formError}
                </div>
              )}

              <form onSubmit={handleSave} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Company Name *</label>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                  />
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
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Phone</label>
                    <input
                      type="text"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Industry</label>
                    <input
                      type="text"
                      value={industry}
                      onChange={(e) => setIndustry(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Website</label>
                  <input
                    type="text"
                    value={website}
                    onChange={(e) => setWebsite(e.target.value)}
                    className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                  />
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
