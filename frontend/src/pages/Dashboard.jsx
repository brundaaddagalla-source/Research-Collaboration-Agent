// import {
//   Users,
//   BookOpen,
//   Link2,
//   Sparkles,
//   Globe2,
//   Landmark,
//   FileWarning,
// } from "lucide-react";
// import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
// import { getDashboard } from "../services/api";
// import { useApiData } from "../services/useApiData";
// import { PageHeader } from "../components/PageHeader";
// import { KpiCard } from "../components/KpiCard";
// import { ScoreBar } from "../components/ScoreBar";
// import { StatusBadge } from "../components/StatusBadge";
// import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

// export default function Dashboard() {
//   const { data, status, error } = useApiData(getDashboard);

//   if (status === "loading") return <LoadingView label="Loading dashboard" />;
//   if (status === "error") return <ErrorView message={error} />;
//   if (!data) return <EmptyView />;

//   const { summary, collaboration_activity, top_opportunities, funding_highlights, mou_highlights } = data;

//   const kpis = [
//     { label: "Faculty", value: summary.faculty_count, icon: Users },
//     { label: "Research Areas", value: summary.research_areas, icon: BookOpen },
//     { label: "Existing Collaborations", value: summary.existing_collaborations, icon: Link2 },
//     { label: "Potential Collaborations", value: summary.potential_collaborations, icon: Sparkles, accent: "active" },
//     { label: "External Candidates", value: summary.external_candidates, icon: Globe2 },
//     { label: "Funding Matches", value: summary.funding_matches, icon: Landmark },
//     { label: "Dormant MoUs", value: summary.dormant_mous, icon: FileWarning, accent: "dormant" },
//   ];

//   return (
//     <div>
//       <PageHeader
//         title="Research Intelligence Overview"
//         description="A snapshot of faculty expertise, collaboration health, and open opportunities across the institution."
//       />

//       {/* KPI cards */}
//       <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 xl:grid-cols-7">
//         {kpis.map((kpi) => (
//           <KpiCard key={kpi.label} {...kpi} />
//         ))}
//       </div>

//       <div className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-3">
//         {/* Potential collaborations */}
//         <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel xl:col-span-2">
//           <h2 className="font-display text-sm font-semibold text-navy-950">Potential Collaborations</h2>
//           <p className="mb-4 text-xs text-navy-900/50">Suggested pairings mock data, for Phase 1 review only.</p>
//           <div className="space-y-4">
//             {top_opportunities.map((op) => (
//               <div key={op.id} className="rounded-lg border border-navy-900/5 bg-sky-50/60 p-4">
//                 <div className="flex flex-wrap items-center justify-between gap-2">
//                   <p className="font-display text-sm font-semibold text-navy-950">
//                     {op.faculty_a} <span className="text-navy-900/30">&harr;</span> {op.faculty_b}
//                   </p>
//                   <StatusBadge status={op.status} />
//                 </div>
//                 <p className="mt-1 text-xs text-navy-900/55">{op.research_areas.join(" + ")}</p>
//                 <p className="mt-2 text-sm text-navy-900/75">{op.reason}</p>
//                 <div className="mt-3 max-w-xs">
//                   <ScoreBar score={op.compatibility_score} />
//                 </div>
//               </div>
//             ))}
//           </div>
//         </div>

//         {/* MoU snapshot */}
//         <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel">
//           <h2 className="font-display text-sm font-semibold text-navy-950">MoU Snapshot</h2>
//           <p className="mb-4 text-xs text-navy-900/50">Active, underutilized, and dormant partnerships.</p>
//           <div className="space-y-3">
//             {mou_highlights.map((mou) => (
//               <div key={mou.id} className="flex items-center justify-between gap-2 border-b border-navy-900/5 pb-3 last:border-0 last:pb-0">
//                 <div className="min-w-0">
//                   <p className="truncate text-sm font-medium text-navy-950">{mou.institution}</p>
//                   <p className="text-xs text-navy-900/50">{mou.research_area}</p>
//                 </div>
//                 <StatusBadge status={mou.status} />
//               </div>
//             ))}
//           </div>
//         </div>
//       </div>

//       <div className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-3">
//         {/* Funding */}
//         <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel">
//           <h2 className="font-display text-sm font-semibold text-navy-950">Funding Opportunities</h2>
//           <p className="mb-4 text-xs text-navy-900/50">Calls matched to current faculty research areas.</p>
//           <div className="space-y-3">
//             {funding_highlights.map((fund) => (
//               <div key={fund.id} className="border-b border-navy-900/5 pb-3 last:border-0 last:pb-0">
//                 <p className="text-sm font-medium text-navy-950">{fund.title}</p>
//                 <p className="mt-0.5 text-xs text-navy-900/50">{fund.organization} &middot; Deadline {fund.deadline}</p>
//                 <p className="mt-1 text-xs text-navy-700">{fund.research_areas.join(", ")}</p>
//               </div>
//             ))}
//           </div>
//         </div>

//         {/* Collaboration activity chart */}
//         <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel xl:col-span-2">
//           <h2 className="font-display text-sm font-semibold text-navy-950">Collaboration Activity</h2>
//           <p className="mb-2 text-xs text-navy-900/50">New collaborations and introductions per month (mock).</p>
//           <div className="h-56 w-full">
//             <ResponsiveContainer width="100%" height="100%">
//               <LineChart data={collaboration_activity} margin={{ top: 10, right: 12, left: -12, bottom: 0 }}>
//                 <CartesianGrid strokeDasharray="3 3" stroke="#e6f0fb" />
//                 <XAxis dataKey="month" tick={{ fontSize: 12, fill: "#15316b99" }} axisLine={false} tickLine={false} />
//                 <YAxis tick={{ fontSize: 12, fill: "#15316b99" }} axisLine={false} tickLine={false} />
//                 <Tooltip
//                   contentStyle={{ borderRadius: 8, borderColor: "#cfe3f7", fontSize: 12 }}
//                 />
//                 <Line type="monotone" dataKey="new_collaborations" name="New collaborations" stroke="#1e3a8a" strokeWidth={2.5} dot={false} />
//                 <Line type="monotone" dataKey="introductions" name="Introductions" stroke="#0f9d6d" strokeWidth={2.5} dot={false} />
//               </LineChart>
//             </ResponsiveContainer>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }


import {
  Users,
  BookOpen,
  Link2,
  Sparkles,
  Globe2,
  Landmark,
  FileWarning,
  LayoutDashboard,
} from "lucide-react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

import { useEffect, useState } from "react";

import {
  getDashboard,
  getFaculty,
  getOpportunities,
} from "../services/api";

import { useApiData } from "../services/useApiData";

import { PageHeader } from "../components/PageHeader";
import { KpiCard } from "../components/KpiCard";
import { ScoreBar } from "../components/ScoreBar";
import { StatusBadge } from "../components/StatusBadge";
import {
  LoadingView,
  ErrorView,
  EmptyView,
} from "../components/StateViews";

export default function Dashboard() {
  const {
    data,
    status,
    error,
  } = useApiData(getDashboard);

  const {
    data: facultyData,
    status: facultyStatus,
    error: facultyError,
  } = useApiData(getFaculty);

  const [selectedFaculty, setSelectedFaculty] = useState("");

  const faculty = facultyData?.faculty || [];

  useEffect(() => {
    if (!selectedFaculty && faculty.length > 0) {
      setSelectedFaculty(faculty[0].name);
    }
  }, [faculty, selectedFaculty]);

  const {
    data: opportunityData,
    status: opportunityStatus,
    error: opportunityError,
  } = useApiData(
    () =>
      selectedFaculty
        ? getOpportunities(selectedFaculty, 3)
        : Promise.resolve({ opportunities: [] }),
    [selectedFaculty]
  );

  if (status === "loading" || facultyStatus === "loading") {
    return <LoadingView label="Loading dashboard" />;
  }

  if (status === "error") {
    return <ErrorView message={error} />;
  }

  if (facultyStatus === "error") {
    return <ErrorView message={facultyError} />;
  }

  if (opportunityStatus === "loading") {
    return <LoadingView label="Finding collaboration opportunities" />;
  }

  if (opportunityStatus === "error") {
    return <ErrorView message={opportunityError} />;
  }

  if (!data) {
    return <EmptyView />;
  }

  const {
    summary,
    collaboration_activity,
    funding_highlights,
    mou_highlights,
  } = data;

  const top_opportunities =
    opportunityData?.opportunities || [];

  const kpis = [
    {
      label: "Faculty",
      value: summary.faculty_count,
      icon: Users,
      accent: "blue",
    },
    {
      label: "Research Areas",
      value: summary.research_areas,
      icon: BookOpen,
      accent: "teal",
    },
    {
      label: "Existing Collaborations",
      value: summary.existing_collaborations,
      icon: Link2,
      accent: "navy",
    },
    {
      label: "Potential Collaborations",
      value: top_opportunities.length,
      icon: Sparkles,
      accent: "active",
    },
    {
      label: "External Candidates",
      value: summary.external_candidates,
      icon: Globe2,
      accent: "purple",
    },
    {
      label: "Funding Matches",
      value: summary.funding_matches,
      icon: Landmark,
      accent: "orange",
    },
    {
      label: "Dormant MoUs",
      value: summary.dormant_mous,
      icon: FileWarning,
      accent: "dormant",
    },
  ];

  return (
    <div>
      <PageHeader
        icon={LayoutDashboard}
        title="Research Intelligence Overview"
        description="A snapshot of faculty expertise, collaboration health, and open opportunities across the institution."
      />

      {/* KPI cards */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 xl:grid-cols-7">
        {kpis.map((kpi) => (
          <KpiCard key={kpi.label} {...kpi} />
        ))}
      </div>

      {/* Potential collaborations + MoU */}
      <div className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-3">

        {/* Potential collaborations */}
        <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel xl:col-span-2">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="font-display text-sm font-semibold text-navy-950">
                Potential Collaborations
              </h2>

              <p className="mb-4 text-xs text-navy-900/50">
                Live collaboration opportunities generated by Agent 24.
              </p>
            </div>

            {faculty.length > 0 && (
              <select
                value={selectedFaculty}
                onChange={(event) =>
                  setSelectedFaculty(event.target.value)
                }
                className="rounded-lg border border-navy-900/10 bg-white px-3 py-2 text-xs text-navy-900 outline-none"
              >
                {faculty.map((member) => (
                  <option
                    key={member.id}
                    value={member.name}
                  >
                    {member.name}
                  </option>
                ))}
              </select>
            )}
          </div>

          {top_opportunities.length === 0 ? (
            <EmptyView message="No collaboration opportunities found for this faculty member." />
          ) : (
            <div className="space-y-4">
              {top_opportunities.map((op, index) => (
                <div
                  key={`${op.faculty_a}-${op.faculty_b}-${index}`}
                  className="rounded-lg border border-navy-900/5 bg-sky-50/60 p-4"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <p className="font-display text-sm font-semibold text-navy-950">
                      {op.faculty_a}
                      <span className="text-navy-900/30">
                        {" "}
                        &harr;{" "}
                      </span>
                      {op.faculty_b}
                    </p>

                    <StatusBadge
                      status={op.opportunity_level}
                    />
                  </div>

                  <p className="mt-2 text-sm font-medium text-navy-700">
                    {op.potential_topic}
                  </p>

                  <p className="mt-2 text-sm text-navy-900/75">
                    {op.reasons?.[0] ||
                      "Potential collaboration identified from research evidence."}
                  </p>

                  <div className="mt-3 grid grid-cols-2 gap-4">
                    <ScoreBar
                      score={op.collaboration_score}
                      label="Collaboration"
                    />

                    <ScoreBar
                      score={op.complementarity_score}
                      label="Complementarity"
                    />
                  </div>

                  <div className="mt-3 flex flex-wrap gap-2">
                    <span className="rounded-full bg-navy-900/5 px-3 py-1 text-xs text-navy-900/70">
                      Research relevance:{" "}
                      {op.semantic_similarity?.toFixed(2)}
                    </span>

                    <span className="rounded-full bg-navy-900/5 px-3 py-1 text-xs text-navy-900/70">
                      Network: {op.network_reachability}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* MoU snapshot */}
        <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel">
          <h2 className="font-display text-sm font-semibold text-navy-950">
            MoU Snapshot
          </h2>

          <p className="mb-4 text-xs text-navy-900/50">
            Active, underutilized, and dormant partnerships.
          </p>

          <div className="space-y-3">
            {mou_highlights.map((mou) => (
              <div
                key={mou.id}
                className="flex items-center justify-between gap-2 border-b border-navy-900/5 pb-3 last:border-0 last:pb-0"
              >
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium text-navy-950">
                    {mou.institution}
                  </p>

                  <p className="text-xs text-navy-900/50">
                    {mou.research_area}
                  </p>
                </div>

                <StatusBadge status={mou.status} />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Funding + collaboration activity */}
      <div className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-3">

        {/* Funding */}
        <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel">
          <h2 className="font-display text-sm font-semibold text-navy-950">
            Funding Opportunities
          </h2>

          <p className="mb-4 text-xs text-navy-900/50">
            Open funding calls from the research database.
          </p>

          <div className="space-y-3">
            {funding_highlights.map((fund) => (
              <div
                key={fund.id}
                className="border-b border-navy-900/5 pb-3 last:border-0 last:pb-0"
              >
                <p className="text-sm font-medium text-navy-950">
                  {fund.title}
                </p>

                <p className="mt-0.5 text-xs text-navy-900/50">
                  {fund.organization} &middot; Deadline{" "}
                  {fund.deadline}
                </p>

                <p className="mt-1 text-xs text-navy-700">
                  {fund.research_areas.join(", ")}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Collaboration activity */}
        <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel xl:col-span-2">
          <h2 className="font-display text-sm font-semibold text-navy-950">
            Collaboration Activity
          </h2>

          <p className="mb-2 text-xs text-navy-900/50">
            Collaboration activity recorded in the research system.
          </p>

          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={collaboration_activity}
                margin={{
                  top: 10,
                  right: 12,
                  left: -12,
                  bottom: 0,
                }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#e6f0fb"
                />

                <XAxis
                  dataKey="month"
                  tick={{
                    fontSize: 12,
                    fill: "#15316b99",
                  }}
                  axisLine={false}
                  tickLine={false}
                />

                <YAxis
                  tick={{
                    fontSize: 12,
                    fill: "#15316b99",
                  }}
                  axisLine={false}
                  tickLine={false}
                />

                <Tooltip
                  contentStyle={{
                    borderRadius: 8,
                    borderColor: "#cfe3f7",
                    fontSize: 12,
                  }}
                />

                <Line
                  type="monotone"
                  dataKey="new_collaborations"
                  name="New collaborations"
                  stroke="#1e3a8a"
                  strokeWidth={2.5}
                  dot={false}
                />

                <Line
                  type="monotone"
                  dataKey="introductions"
                  name="Introductions"
                  stroke="#0f9d6d"
                  strokeWidth={2.5}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}