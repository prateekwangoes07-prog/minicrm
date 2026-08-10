"use client";

import React, { useEffect, useState } from "react";
import AppLayout from "@/components/layout/AppLayout";
import { useAuth } from "@/hooks/useAuth";
import { customersApi } from "@/lib/api/customers";
import { companiesApi } from "@/lib/api/companies";
import { Customer, Company } from "@/types";
import { Plus, Edit2, Trash2, X, RefreshCw } from "lucide-react";

export default function CustomersPage() {
  const { user } = useAuth();
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [notes, setNotes] = useState("");
  const [companyId, setCompanyId] = useState("");
  const [isActive, setIsActive] = useState(true);
  const [formError, setFormError] = useState<string | null>(null);

  const isAdmin = user?.role === "admin";

  const fetchData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [custList, compList] = await Promise.all([
        customersApi.list(),
        companiesApi.list(),
      ]);
      setCustomers(custList);
      setCompanies(compList);
    } catch (err: any) {
      setError(err.message || "Failed to load customers.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const openCreateModal = () => {
    setEditingId(null);
    setFirstName("");
    setLastName("");
    setEmail("");
    setPhone("");
    setAddress("");
    setNotes("");
    setCompanyId(companies[0]?.id || "");
    setIsActive(true);
    setFormError(null);
    setIsModalOpen(true);
  };

  const openEditModal = (customer: Customer) => {
    setEditingId(customer.id);
    setFirstName(customer.first_name);
    setLastName(customer.last_name);
    setEmail(customer.email);
    setPhone(customer.phone || "");
    setAddress(customer.address || "");
    setNotes(customer.notes || "");
    setCompanyId(customer.company_id);
    setIsActive(customer.is_active);
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    const payload = {
      first_name: firstName,
      last_name: lastName,
      email,
      phone: phone || null,
      address: address || null,
      notes: notes || null,
      company_id: companyId,
      is_active: isActive,
    };

    try {
      if (editingId) {
        await customersApi.update(editingId, payload);
      } else {
        await customersApi.create(payload);
      }
      setIsModalOpen(false);
      fetchData();
    } catch (err: any) {
      if (err.status === 403) {
        setFormError("You don't have permission to perform this action.");
      } else {
        setFormError(err.message || "Failed to save customer.");
      }
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this customer?")) return;

    try {
      await customersApi.delete(id);
      fetchData();
    } catch (err: any) {
      if (err.status === 403) {
        alert("You don't have permission to perform this action.");
      } else {
        alert(err.message || "Failed to delete customer.");
      }
    }
  };

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Customers</h1>
            <p className="text-sm text-zinc-400 mt-1">Manage corporate client contacts, profiles, and communications.</p>
          </div>
          {isAdmin && (
            <button
              onClick={openCreateModal}
              className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 transition-colors shadow-md"
            >
              <Plus className="h-4 w-4" />
              <span>Add Customer</span>
            </button>
          )}
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
        ) : customers.length === 0 ? (
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/20 p-12 text-center text-zinc-400">
            <p className="text-lg font-semibold text-white">No customers found</p>
            <p className="text-sm mt-1">Get started by creating your first customer contact.</p>
            {isAdmin && (
              <button
                onClick={openCreateModal}
                className="mt-4 inline-flex items-center gap-2 rounded-lg border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 px-4 py-2 text-sm font-semibold text-white transition-colors"
              >
                Create Customer
              </button>
            )}
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-900/30">
            <table className="min-w-full divide-y divide-zinc-850">
              <thead>
                <tr className="text-left text-xs font-semibold text-zinc-400 uppercase bg-zinc-900/50">
                  <th className="px-6 py-4">Customer Name</th>
                  <th className="px-6 py-4">Email</th>
                  <th className="px-6 py-4">Phone</th>
                  <th className="px-6 py-4">Company</th>
                  <th className="px-6 py-4">Status</th>
                  {isAdmin && <th className="px-6 py-4 text-right">Actions</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-850 text-sm text-zinc-300">
                {customers.map((cust) => {
                  const companyName = companies.find((c) => c.id === cust.company_id)?.name || "—";
                  return (
                    <tr key={cust.id} className="hover:bg-zinc-900/20">
                      <td className="px-6 py-4 font-medium text-white">{`${cust.first_name} ${cust.last_name}`}</td>
                      <td className="px-6 py-4">{cust.email}</td>
                      <td className="px-6 py-4">{cust.phone || "—"}</td>
                      <td className="px-6 py-4">{companyName}</td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold border ${
                            cust.is_active
                              ? "bg-emerald-500/10 text-emerald-400 border-emerald-800"
                              : "bg-zinc-500/10 text-zinc-400 border-zinc-800"
                          }`}
                        >
                          {cust.is_active ? "Active" : "Inactive"}
                        </span>
                      </td>
                      {isAdmin && (
                        <td className="px-6 py-4 text-right space-x-2">
                          <button
                            onClick={() => openEditModal(cust)}
                            className="inline-flex p-1.5 rounded-lg border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-100 transition-colors"
                          >
                            <Edit2 className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(cust.id)}
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
                {editingId ? "Edit Customer" : "Add Customer"}
              </h2>

              {formError && (
                <div className="rounded-md bg-red-950/30 border border-red-800 p-3 text-sm text-red-400 mb-4">
                  {formError}
                </div>
              )}

              <form onSubmit={handleSave} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">First Name *</label>
                    <input
                      type="text"
                      required
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)}
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Last Name *</label>
                    <input
                      type="text"
                      required
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
                    <label className="block text-sm font-medium text-zinc-300 mb-2">Company Association *</label>
                    <select
                      value={companyId}
                      onChange={(e) => setCompanyId(e.target.value)}
                      required
                      className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                    >
                      {companies.map((c) => (
                        <option key={c.id} value={c.id}>
                          {c.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Address</label>
                  <input
                    type="text"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-2">Notes</label>
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    className="block w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2.5 text-white focus:border-indigo-500 focus:outline-none sm:text-sm h-20 resize-none"
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
