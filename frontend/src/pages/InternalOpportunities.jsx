// import { getOpportunities } from "../services/api";
// import { useApiData } from "../services/useApiData";
// import { PageHeader } from "../components/PageHeader";
// import { StatusBadge } from "../components/StatusBadge";
// import { ScoreBar } from "../components/ScoreBar";
// import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

// export default function InternalOpportunities() {
//   const { data, status, error } = useApiData(getOpportunities);

//   if (status === "loading") return <LoadingView label="Loading opportunities" />;
//   if (status === "error") return <ErrorView message={error} />;

//   const opportunities = data?.opportunities || [];
//   if (opportunities.length === 0) return <EmptyView message="No collaboration opportunities suggested yet." />;

//   return (
//     <div>
//       <PageHeader
//         title="Internal Opportunities"
//         description="Suggested faculty pairings based on complementary, non-overlapping expertise. Mock data - scoring logic is not implemented in Phase 1."
//       />

//       <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
//         {opportunities.map((op) => (
//           <div key={op.id} className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel">
//             <div className="flex items-start justify-between gap-2">
//               <div>
//                 <p className="font-display text-sm font-semibold text-navy-950">{op.faculty_a}</p>
//                 <p className="text-xs text-navy-900/50">{op.department_a}</p>
//               </div>
//               <StatusBadge status={op.status} />
//             </div>

//             <div className="my-2 flex items-center gap-2 text-navy-900/30">
//               <span className="h-px flex-1 bg-navy-900/10" />
//               <span className="text-xs">&harr;</span>
//               <span className="h-px flex-1 bg-navy-900/10" />
//             </div>

//             <div>
//               <p className="font-display text-sm font-semibold text-navy-950">{op.faculty_b}</p>
//               <p className="text-xs text-navy-900/50">{op.department_b}</p>
//             </div>

//             <p className="mt-3 text-xs font-medium text-navy-700">{op.research_areas.join(" + ")}</p>
//             <p className="mt-2 text-sm text-navy-900/75">{op.reason}</p>

//             <div className="mt-4 grid grid-cols-2 gap-4">
//               <ScoreBar score={op.compatibility_score} label="Compatibility" />
//               <ScoreBar score={op.complementarity_score} label="Complementarity" />
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

import { useEffect, useState } from "react";
import { Lightbulb } from "lucide-react";

import { getFaculty, getOpportunities } from "../services/api";
import { useApiData } from "../services/useApiData";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { ScoreBar } from "../components/ScoreBar";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

export default function InternalOpportunities() {
  const [selectedFaculty, setSelectedFaculty] = useState("");

  const {
    data: facultyData,
    status: facultyStatus,
    error: facultyError,
  } = useApiData(getFaculty);

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
        ? getOpportunities(selectedFaculty, 5)
        : Promise.resolve({ opportunities: [] }),
    [selectedFaculty]
  );

  if (facultyStatus === "loading") {
    return <LoadingView label="Loading faculty" />;
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

  const opportunities = opportunityData?.opportunities || [];

  if (faculty.length === 0) {
    return <EmptyView message="No faculty members found." />;
  }

  if (opportunities.length === 0) {
    return (
      <div>
        <PageHeader
          icon={Lightbulb}
          title="Internal Opportunities"
          description="Suggested faculty pairings based on complementary expertise, research evidence, funding opportunities, and collaboration potential."
        />

        <div className="mb-6">
          <label className="mb-2 block text-sm font-medium text-navy-900">
            Select Faculty
          </label>

          <select
            value={selectedFaculty}
            onChange={(event) => setSelectedFaculty(event.target.value)}
            className="w-full max-w-md rounded-lg border border-navy-900/10 bg-white px-4 py-2 text-sm outline-none"
          >
            {faculty.map((member) => (
              <option key={member.id} value={member.name}>
                {member.name}
              </option>
            ))}
          </select>
        </div>

        <EmptyView message="No collaboration opportunities found for this faculty member." />
      </div>
    );
  }

  return (
    <div>
      <PageHeader
        icon={Lightbulb}
        title="Internal Opportunities"
        description="Suggested faculty pairings based on complementary expertise, research evidence, funding opportunities, and collaboration potential."
      />

      <div className="mb-6">
        <label className="mb-2 block text-sm font-medium text-navy-900">
          Select Faculty
        </label>

        <select
          value={selectedFaculty}
          onChange={(event) => setSelectedFaculty(event.target.value)}
          className="w-full max-w-md rounded-lg border border-navy-900/10 bg-white px-4 py-2 text-sm outline-none"
        >
          {faculty.map((member) => (
            <option key={member.id} value={member.name}>
              {member.name}
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {opportunities.map((op, index) => (
          <div
            key={`${op.faculty_a}-${op.faculty_b}-${index}`}
            className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel"
          >
            <div className="flex items-start justify-between gap-2">
              <div>
                <p className="font-display text-sm font-semibold text-navy-950">
                  {op.faculty_a}
                </p>

                <p className="text-xs text-navy-900/50">
                  {op.department_a}
                </p>
              </div>

              <StatusBadge status={op.opportunity_level} />
            </div>

            <div className="my-2 flex items-center gap-2 text-navy-900/30">
              <span className="h-px flex-1 bg-navy-900/10" />
              <span className="text-xs">&harr;</span>
              <span className="h-px flex-1 bg-navy-900/10" />
            </div>

            <div>
              <p className="font-display text-sm font-semibold text-navy-950">
                {op.faculty_b}
              </p>

              <p className="text-xs text-navy-900/50">
                {op.department_b}
              </p>
            </div>

            <p className="mt-3 text-sm font-medium text-navy-700">
              {op.potential_topic}
            </p>

            <p className="mt-2 text-sm text-navy-900/75">
              {op.reasons?.[0] || "Potential collaboration identified from research evidence."}
            </p>

            <div className="mt-4 grid grid-cols-2 gap-4">
              <ScoreBar
                score={op.collaboration_score}
                label="Collaboration"
              />

              <ScoreBar
                score={op.complementarity_score}
                label="Complementarity"
              />
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              <span className="rounded-full bg-navy-900/5 px-3 py-1 text-xs text-navy-900/70">
                Research relevance: {op.semantic_similarity.toFixed(2)}
              </span>

              <span className="rounded-full bg-navy-900/5 px-3 py-1 text-xs text-navy-900/70">
                Network: {op.network_reachability}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}