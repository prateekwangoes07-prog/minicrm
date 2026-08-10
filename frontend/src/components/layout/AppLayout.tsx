"use client";

import React, { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Building2,
  Users2,
  UserSquare2,
  LineChart,
  LogOut,
  Menu,
  X,
  User as UserIcon,
} from "lucide-react";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { user, isLoading, logout } = useAuth();
  const pathname = usePathname();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  if (isLoading) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-zinc-950 text-zinc-100">
        <div className="flex flex-col items-center gap-4">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
          <p className="text-sm text-zinc-400">Loading MiniCRM...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const isAdmin = user.role === "admin";

  const navigation = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard, show: true },
    { name: "Companies", href: "/companies", icon: Building2, show: isAdmin },
    { name: "Employees", href: "/employees", icon: Users2, show: isAdmin },
    { name: "Customers", href: "/customers", icon: UserSquare2, show: true },
    { name: "Leads", href: "/leads", icon: LineChart, show: true },
  ];

  return (
    <div className="flex h-screen bg-zinc-950 text-zinc-100 overflow-hidden">
      {/* Sidebar for desktop */}
      <aside className="hidden md:flex md:w-64 md:flex-col bg-zinc-900 border-r border-zinc-800">
        <div className="flex items-center h-16 px-6 border-b border-zinc-800">
          <Link href="/dashboard" className="flex items-center gap-2 font-bold text-lg text-indigo-400">
            <Building2 className="h-6 w-6" />
            <span>MiniCRM</span>
          </Link>
        </div>
        <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
          {navigation.map((item) => {
            if (!item.show) return null;
            const isActive = pathname.startsWith(item.href);
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-indigo-600 text-white"
                    : "text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100"
                }`}
              >
                <item.icon className="h-5 w-5" />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
        <div className="p-4 border-t border-zinc-800">
          <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-zinc-950/50 mb-3">
            <div className="flex items-center justify-center h-9 w-9 rounded-full bg-indigo-900 text-indigo-200">
              <UserIcon className="h-5 w-5" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-semibold truncate text-zinc-200">{user.email}</p>
              <p className="text-[10px] text-zinc-500 capitalize">{user.role}</p>
            </div>
          </div>
          <button
            onClick={() => logout()}
            className="flex w-full items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-red-400 hover:bg-red-950/20 transition-colors"
          >
            <LogOut className="h-5 w-5" />
            <span>Log out</span>
          </button>
        </div>
      </aside>

      {/* Mobile Sidebar overlay */}
      {isSidebarOpen && (
        <div className="fixed inset-0 z-40 flex md:hidden bg-zinc-950/80 backdrop-blur-sm">
          <div className="relative flex w-64 max-w-xs flex-col bg-zinc-900 border-r border-zinc-800">
            <div className="absolute top-0 right-0 -mr-12 pt-4">
              <button
                onClick={() => setIsSidebarOpen(false)}
                className="flex h-10 w-10 items-center justify-center rounded-full text-zinc-400 hover:text-zinc-100 focus:outline-none"
              >
                <X className="h-6 w-6" />
              </button>
            </div>
            <div className="flex items-center h-16 px-6 border-b border-zinc-800">
              <Link href="/dashboard" className="flex items-center gap-2 font-bold text-lg text-indigo-400">
                <Building2 className="h-6 w-6" />
                <span>MiniCRM</span>
              </Link>
            </div>
            <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
              {navigation.map((item) => {
                if (!item.show) return null;
                const isActive = pathname.startsWith(item.href);
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setIsSidebarOpen(false)}
                    className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                      isActive
                        ? "bg-indigo-600 text-white"
                        : "text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100"
                    }`}
                  >
                    <item.icon className="h-5 w-5" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </nav>
            <div className="p-4 border-t border-zinc-800">
              <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-zinc-950/50 mb-3">
                <div className="flex items-center justify-center h-9 w-9 rounded-full bg-indigo-900 text-indigo-200">
                  <UserIcon className="h-5 w-5" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-xs font-semibold truncate text-zinc-200">{user.email}</p>
                  <p className="text-[10px] text-zinc-500 capitalize">{user.role}</p>
                </div>
              </div>
              <button
                onClick={() => logout()}
                className="flex w-full items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-red-400 hover:bg-red-950/20 transition-colors"
              >
                <LogOut className="h-5 w-5" />
                <span>Log out</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main content wrapper */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        <header className="flex h-16 items-center justify-between px-6 bg-zinc-900/50 border-b border-zinc-800 md:justify-end">
          <button
            onClick={() => setIsSidebarOpen(true)}
            className="md:hidden text-zinc-400 hover:text-zinc-100"
          >
            <Menu className="h-6 w-6" />
          </button>
          <div className="flex items-center gap-4">
            <span className="text-xs text-zinc-400 hidden sm:inline">Signed in as <strong className="text-zinc-200">{user.email}</strong> ({user.role})</span>
          </div>
        </header>

        {/* Page children */}
        <main className="flex-1 overflow-y-auto bg-zinc-950 p-6 md:p-8">
          <div className="mx-auto max-w-7xl">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
