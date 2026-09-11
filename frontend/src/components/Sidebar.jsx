import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Network,
  GitBranch,
  Lightbulb,
  Globe2,
  Landmark,
  FileSignature,
  Activity,
  Radar,
} from "lucide-react";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/expertise", label: "Expertise Map", icon: Network },
  { to: "/collaboration-network", label: "Collaboration Network", icon: GitBranch },
  { to: "/opportunities", label: "Internal Opportunities", icon: Lightbulb },
  { to: "/external-researchers", label: "External Researchers", icon: Globe2 },
  { to: "/funding", label: "Funding & Consortiums", icon: Landmark },
  { to: "/mous", label: "MoU Intelligence", icon: FileSignature },
  { to: "/tracking", label: "Collaboration Tracking", icon: Activity },
];

export function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 hidden h-screen w-64 flex-col bg-navy-950 text-white lg:flex">
      <div className="flex items-center gap-2.5 px-6 py-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-navy-700">
          <Radar className="h-5 w-5 text-sky-100" />
        </div>
        <div>
          <p className="font-display text-sm font-bold leading-tight">Agent 24</p>
          <p className="text-[11px] leading-tight text-white/45">Research Collaboration</p>
        </div>
      </div>

      <nav className="mt-2 flex-1 space-y-1 overflow-y-auto px-3">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors ${
                isActive
                  ? "bg-navy-700 text-white font-medium"
                  : "text-white/60 hover:bg-white/5 hover:text-white"
              }`
            }
          >
            <Icon className="h-4 w-4 shrink-0" />
            <span className="truncate">{label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-white/10 px-6 py-4">
        <p className="text-[11px] leading-relaxed text-white/35">
          Phase 1 · Foundation build
          <br />
          Mock data only, no AI logic active
        </p>
      </div>
    </aside>
  );
}
