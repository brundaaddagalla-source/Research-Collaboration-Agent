import { getCollaborations } from "../services/api";
import { useApiData } from "../services/useApiData";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

// Fixed layout positions for the mock nodes (percentages of the canvas).
// This is a static placeholder layout only - Phase 2+ will replace this
// with an algorithmically generated graph.
const LAYOUT = {
  ananya_rao: { x: 18, y: 20 },
  arjun_desai: { x: 18, y: 65 },
  rahul_sharma: { x: 50, y: 15 },
  meera_krishnan: { x: 50, y: 60 },
  vikram_nair: { x: 82, y: 22 },
  priya_menon: { x: 82, y: 68 },
  kavitha_reddy: { x: 34, y: 88 },
  suresh_iyer: { x: 66, y: 88 },
};

const STRENGTH_COLOR = {
  Strong: "#0f9d6d",
  Moderate: "#c98a1c",
  Weak: "#c23b3b",
};

export default function CollaborationNetwork() {
  const { data, status, error } = useApiData(getCollaborations);

  if (status === "loading") return <LoadingView label="Loading collaboration network" />;
  if (status === "error") return <ErrorView message={error} />;

  const collaborations = data?.collaborations || [];
  const network = data?.network || { nodes: [], edges: [] };

  if (network.nodes.length === 0) return <EmptyView message="No collaboration network data yet." />;

  return (
    <div>
      <PageHeader
        title="Collaboration Network"
        description="A visual placeholder of existing faculty collaborations. Real network analysis (co-authorship graphs, centrality, gap detection) will be added in a later phase."
      />

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        {/* Graph */}
        <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel xl:col-span-2">
          <h2 className="mb-4 font-display text-sm font-semibold text-navy-950">Network Snapshot</h2>
          <div className="relative h-[420px] w-full rounded-lg bg-sky-50">
            <svg className="absolute inset-0 h-full w-full">
              {network.edges.map((edge, i) => {
                const from = LAYOUT[edge.source];
                const to = LAYOUT[edge.target];
                if (!from || !to) return null;
                return (
                  <line
                    key={i}
                    x1={`${from.x}%`}
                    y1={`${from.y}%`}
                    x2={`${to.x}%`}
                    y2={`${to.y}%`}
                    stroke={STRENGTH_COLOR[edge.strength] || "#94a3b8"}
                    strokeWidth={2}
                    strokeDasharray={edge.strength === "Weak" ? "5,4" : "0"}
                  />
                );
              })}
            </svg>

            {network.nodes.map((node) => {
              const pos = LAYOUT[node.id];
              if (!pos) return null;
              return (
                <div
                  key={node.id}
                  className="absolute flex -translate-x-1/2 -translate-y-1/2 flex-col items-center gap-1"
                  style={{ left: `${pos.x}%`, top: `${pos.y}%` }}
                >
                  <div className="flex h-11 w-11 items-center justify-center rounded-full border-2 border-navy-700 bg-white text-[11px] font-display font-bold text-navy-700 shadow-panel">
                    {node.label
                      .replace("Dr. ", "")
                      .split(" ")
                      .map((w) => w[0])
                      .join("")}
                  </div>
                  <span className="whitespace-nowrap rounded bg-white/90 px-1.5 py-0.5 text-[11px] font-medium text-navy-950 shadow-sm">
                    {node.label}
                  </span>
                  <span className="text-[10px] text-navy-900/45">{node.department}</span>
                </div>
              );
            })}
          </div>

          <div className="mt-4 flex flex-wrap gap-4 text-xs text-navy-900/55">
            <LegendDot color={STRENGTH_COLOR.Strong} label="Strong collaboration" />
            <LegendDot color={STRENGTH_COLOR.Moderate} label="Moderate collaboration" />
            <LegendDot color={STRENGTH_COLOR.Weak} label="Weak collaboration" dashed />
          </div>
        </div>

        {/* List */}
        <div className="rounded-xl border border-navy-900/5 bg-white p-5 shadow-panel">
          <h2 className="mb-4 font-display text-sm font-semibold text-navy-950">Existing Collaborations</h2>
          <div className="space-y-3">
            {collaborations.map((c) => (
              <div key={c.id} className="border-b border-navy-900/5 pb-3 last:border-0 last:pb-0">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-sm font-medium text-navy-950">
                    {c.faculty_a} &harr; {c.faculty_b}
                  </p>
                  <StatusBadge status={c.collaboration_strength} />
                </div>
                <p className="mt-1 text-xs text-navy-900/50">{c.department}</p>
                <p className="mt-1 text-xs text-navy-700">{c.research_areas.join(", ")} &middot; {c.collaboration_type}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function LegendDot({ color, label, dashed }) {
  return (
    <span className="flex items-center gap-1.5">
      <span
        className="inline-block h-0.5 w-4"
        style={{ backgroundColor: dashed ? "transparent" : color, borderTop: dashed ? `2px dashed ${color}` : "none" }}
      />
      {label}
    </span>
  );
}
