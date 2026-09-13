import { useMemo } from "react";
import { Link } from "react-router-dom";
import {
  BookOpen,
  Link2,
  Sparkles,
  Tags,
} from "lucide-react";

import { getMyProfile, getTracking } from "../services/api";
import { useApiData } from "../services/useApiData";
import { KpiCard } from "../components/KpiCard";
import { StatusBadge } from "../components/StatusBadge";
import { CollaborationAssistant } from "../components/CollaborationAssistant";
import {
  LoadingView,
  ErrorView,
} from "../components/StateViews";

function greeting() {
  const hour = new Date().getHours();

  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";

  return "Good evening";
}

export default function Dashboard() {
  const {
    data: facultyData,
    status: facultyStatus,
    error: facultyError,
  } = useApiData(getMyProfile);

  const {
    data: trackingData,
    status: trackingStatus,
  } = useApiData(getTracking);

  const profile = facultyData || null;

  const myTrackingRecords = useMemo(() => {
    if (!trackingData?.records || !profile?.name) {
      return [];
    }

    const name = profile.name.trim().toLowerCase();

    return trackingData.records.filter(
      (record) =>
        (record.faculty_a || "").trim().toLowerCase() === name ||
        (record.faculty_b || "").trim().toLowerCase() === name
    );
  }, [trackingData, profile]);

  if (facultyStatus === "loading") {
    return <LoadingView label="Loading your dashboard" />;
  }

  if (facultyStatus === "error") {
    return <ErrorView message={facultyError} />;
  }

  return (
    <div>
      {/* Greeting */}
      <div className="mb-6">
        <p className="text-sm text-surface-muted">
          {greeting()}, {profile?.name || "Faculty"}
        </p>

        {profile && (
          <>
            <h1 className="font-display text-2xl font-bold text-navy-800">
              {profile.designation}
            </h1>

            <p className="text-sm text-surface-muted">
              {profile.department}
            </p>
          </>
        )}
      </div>

      <div className="grid grid-cols-1 gap-6">
        {/* Profile + stats + research areas + activity */}
        <div className="space-y-6">
          {/* Profile summary */}
          <div className="rounded-panel border border-surface-line bg-white p-5 shadow-panel">
            <h2 className="font-display text-sm font-semibold text-navy-800">
              Profile Summary
            </h2>

            {!profile ? (
              <p className="mt-3 text-sm text-surface-muted">
                We couldn't load your research profile.
              </p>
            ) : (
              <dl className="mt-3 grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <dt className="text-xs text-surface-muted">
                    Name
                  </dt>
                  <dd className="text-sm font-medium text-navy-800">
                    {profile.name}
                  </dd>
                </div>

                <div>
                  <dt className="text-xs text-surface-muted">
                    Designation
                  </dt>
                  <dd className="text-sm font-medium text-navy-800">
                    {profile.designation}
                  </dd>
                </div>

                <div>
                  <dt className="text-xs text-surface-muted">
                    Department
                  </dt>
                  <dd className="text-sm font-medium text-navy-800">
                    {profile.department}
                  </dd>
                </div>

                <div>
                  <dt className="text-xs text-surface-muted">
                    Faculty ID
                  </dt>
                  <dd className="text-sm font-medium text-navy-800">
                    {profile.faculty_id}
                  </dd>
                </div>
              </dl>
            )}
          </div>

          {/* Research snapshot */}
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <KpiCard
              label="Publications"
              value={profile?.publications_count ?? "-"}
              icon={BookOpen}
            />

            <KpiCard
              label="Total Collaborations"
              value={profile?.collaboration_count ?? "-"}
              icon={Link2}
              accent="active"
            />

            <KpiCard
              label="Research Areas"
              value={profile?.research_interests?.length ?? "-"}
              icon={Tags}
              accent="purple"
            />

            <KpiCard
              label="Tracked Activity"
              value={myTrackingRecords.length}
              icon={Sparkles}
              accent="teal"
            />
          </div>

          {/* Research areas */}
          <div className="rounded-panel border border-surface-line bg-white p-5 shadow-panel">
            <h2 className="font-display text-sm font-semibold text-navy-800">
              Research Areas
            </h2>

            {profile?.research_interests?.length > 0 ? (
              <div className="mt-3 flex flex-wrap gap-2">
                {profile.research_interests.map((area) => (
                  <span
                    key={area}
                    className="rounded-full bg-sky-100 px-3 py-1 text-xs font-medium text-accent-blue"
                  >
                    {area}
                  </span>
                ))}
              </div>
            ) : (
              <p className="mt-3 text-sm text-surface-muted">
                No research areas on file yet.
              </p>
            )}
          </div>

          {/* Projects */}
          <div className="rounded-panel border border-surface-line bg-white p-5 shadow-panel">
            <h2 className="font-display text-sm font-semibold text-navy-800">
              Previous &amp; Current Projects
            </h2>

            {profile?.projects?.length > 0 ? (
              <div className="mt-3 space-y-4">
                {profile.projects.map((project) => (
                  <div
                    key={project.id || project.title}
                    className="border-b border-surface-line pb-3 last:border-0 last:pb-0"
                  >
                    <p className="text-sm font-medium text-navy-800">
                      {project.title}
                    </p>

                    {project.description && (
                      <p className="mt-1 text-xs leading-5 text-surface-muted">
                        {project.description}
                      </p>
                    )}

                    <div className="mt-2 flex flex-wrap gap-2">
                      {project.research_area && (
                        <span className="rounded-full bg-sky-100 px-2.5 py-1 text-[11px] font-medium text-accent-blue">
                          {project.research_area}
                        </span>
                      )}

                      {project.status && (
                        <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-medium text-surface-muted">
                          {project.status}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="mt-3 text-sm text-surface-muted">
                No projects on file yet.
              </p>
            )}
          </div>

          {/* Collaboration activity */}
          <div className="rounded-panel border border-surface-line bg-white p-5 shadow-panel">
            <div className="flex items-center justify-between">
              <h2 className="font-display text-sm font-semibold text-navy-800">
                My Collaboration Activity
              </h2>

              <Link
                to="/requests"
                className="text-xs font-medium text-accent-blue hover:text-navy-700"
              >
                View all
              </Link>
            </div>

            {trackingStatus === "loading" && (
              <p className="mt-3 text-sm text-surface-muted">
                Loading...
              </p>
            )}

            {trackingStatus === "success" &&
              myTrackingRecords.length === 0 && (
                <p className="mt-3 text-sm text-surface-muted">
                  No tracked collaboration activity yet.
                </p>
              )}

            {trackingStatus === "success" &&
              myTrackingRecords.length > 0 && (
                <div className="mt-3 space-y-3">
                  {myTrackingRecords.slice(0, 4).map((record) => {
                    const other =
                      (record.faculty_a || "").trim().toLowerCase() ===
                      (profile?.name || "").trim().toLowerCase()
                        ? record.faculty_b
                        : record.faculty_a;

                    return (
                      <div
                        key={record.id}
                        className="flex items-center justify-between gap-2 border-b border-surface-line pb-3 last:border-0 last:pb-0"
                      >
                        <div className="min-w-0">
                          <p className="truncate text-sm font-medium text-navy-800">
                            {other || record.external_institution}
                          </p>

                          <p className="text-xs text-surface-muted">
                            {record.topic}
                          </p>
                        </div>

                        <StatusBadge status={record.current_stage} />
                      </div>
                    );
                  })}
                </div>
              )}
          </div>
        </div>

        {/* Find Collaborators - search happens directly on the Dashboard;
            reuses the existing CollaborationAssistant / searchCollaborators
            search, OpportunityCard results, and Request Collaboration flow. */}
        <CollaborationAssistant topK={8} />
      </div>
    </div>
  );
}