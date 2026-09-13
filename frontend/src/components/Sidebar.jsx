import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Inbox,
  Users,
  UserCircle,
  Radar,
  LogOut,
} from "lucide-react";

import { getStoredFaculty, clearStoredFaculty } from "../services/auth";

// Faculty-facing navigation only. The previous admin-style sections
// (Expertise Map, External Researchers, Funding, MoUs, Collaboration
// Network) are hidden from this interface for now, per the new
// faculty-facing scope - their pages and backend routes are untouched.
// Faculty search now happens directly on the Dashboard, so there is no
// separate "Faculty Search" nav item.
const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/requests", label: "My Requests", icon: Inbox },
  { to: "/collaborations", label: "My Collaborations", icon: Users },
  { to: "/profile", label: "My Profile", icon: UserCircle },
];

export function Sidebar() {
  const navigate = useNavigate();
  const faculty = getStoredFaculty();

  function handleLogout() {
    clearStoredFaculty();
    navigate("/login", { replace: true });
  }

  return (
    <aside className="fixed left-0 top-0 hidden h-screen w-64 flex-col border-r border-surface-line bg-white lg:flex">
      {/* Brand */}
      <div className="flex items-center gap-3 border-b border-surface-line px-6 py-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-soft-blue ring-1 ring-blue/10">
          <Radar className="h-5 w-5 text-blue" />
        </div>

        <div>
          <p className="font-display text-sm font-bold leading-tight text-navy-800">
            Agent 24
          </p>
          <p className="mt-0.5 text-[11px] leading-tight text-surface-muted">
            Research Collaboration
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="mt-4 flex-1 space-y-1 overflow-y-auto px-3">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-all ${
                isActive
                  ? "bg-soft-blue font-semibold text-blue shadow-sm"
                  : "text-surface-muted hover:bg-sky-50 hover:text-navy-800"
              }`
            }
          >
            <Icon className="h-4 w-4 shrink-0" />
            <span className="truncate">{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Logged-in faculty + logout */}
      <div className="border-t border-surface-line p-4">
        <div className="rounded-xl border border-surface-line bg-sky-50 p-3">
          <p className="text-[11px] font-medium text-surface-muted">
            Logged in as
          </p>
          <p className="truncate text-sm font-semibold text-navy-800">
            {faculty?.name || "Faculty"}
          </p>

          <button
            onClick={handleLogout}
            className="mt-3 flex w-full items-center justify-center gap-2 rounded-lg border border-surface-line bg-white px-3 py-2 text-xs font-medium text-surface-muted transition hover:border-signal-dormant/30 hover:text-signal-dormant"
          >
            <LogOut className="h-3.5 w-3.5" />
            Logout
          </button>
        </div>
      </div>
    </aside>
  );
}