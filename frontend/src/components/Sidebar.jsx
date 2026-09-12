// import { NavLink } from "react-router-dom";
// import {
//   LayoutDashboard,
//   Network,
//   GitBranch,
//   Lightbulb,
//   Globe2,
//   Landmark,
//   FileSignature,
//   Activity,
//   Radar,
// } from "lucide-react";

// const NAV_ITEMS = [
//   { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
//   { to: "/expertise", label: "Expertise Map", icon: Network },
//   { to: "/collaboration-network", label: "Collaboration Network", icon: GitBranch },
//   { to: "/opportunities", label: "Internal Opportunities", icon: Lightbulb },
//   { to: "/external-researchers", label: "External Researchers", icon: Globe2 },
//   { to: "/funding", label: "Funding & Consortiums", icon: Landmark },
//   { to: "/mous", label: "MoU Intelligence", icon: FileSignature },
//   { to: "/tracking", label: "Collaboration Tracking", icon: Activity },
// ];

// export function Sidebar() {
//   return (
//     <aside className="fixed left-0 top-0 hidden h-screen w-64 flex-col bg-navy-950 text-white lg:flex">
//       <div className="flex items-center gap-2.5 px-6 py-6">
//         <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-accent-blue to-navy-700">
//           <Radar className="h-5 w-5 text-sky-100" />
//         </div>
//         <div>
//           <p className="font-display text-sm font-bold leading-tight">Agent 24</p>
//           <p className="text-[11px] leading-tight text-white/45">Research Collaboration</p>
//         </div>
//       </div>

//       <nav className="mt-2 flex-1 space-y-1 overflow-y-auto px-3">
//         {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
//           <NavLink
//             key={to}
//             to={to}
//             end={end}
//             className={({ isActive }) =>
//               `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors ${
//                 isActive
//                   ? "bg-navy-700 text-white font-medium"
//                   : "text-white/60 hover:bg-white/5 hover:text-white"
//               }`
//             }
//           >
//             <Icon className="h-4 w-4 shrink-0" />
//             <span className="truncate">{label}</span>
//           </NavLink>
//         ))}
//       </nav>

      
//     </aside>
//   );
// }

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

      {/* Bottom status */}
      <div className="border-t border-surface-line p-4">
        <div className="rounded-xl border border-surface-line bg-sky-50 p-3">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-signal-active" />
            <span className="text-xs font-medium text-navy-800">
              Agent Online
            </span>
          </div>

          <p className="mt-1 text-[11px] text-surface-muted">
            Research collaboration system
          </p>
        </div>
      </div>
    </aside>
  );
}
