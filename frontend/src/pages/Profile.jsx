import { useCallback, useState } from "react";
import { UserCircle, Upload, FileText, Trash2, Loader2 } from "lucide-react";
import {
  getMyProfile,
  listMyResearchDocuments,
  uploadResearchDocument,
  deleteResearchDocument,
} from "../services/api";
import { useApiData } from "../services/useApiData";
import { PageHeader } from "../components/PageHeader";
import { LoadingView, ErrorView, EmptyView } from "../components/StateViews";

function Field({ label, value }) {
  return (
    <div>
      <dt className="text-xs text-surface-muted">{label}</dt>
      <dd className="mt-0.5 text-sm font-medium text-navy-800">{value ?? "Not available"}</dd>
    </div>
  );
}

function UploadForm({ onUploaded }) {
  const [title, setTitle] = useState("");
  const [keywords, setKeywords] = useState("");
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | uploading | error
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    if (!title.trim() || !file) {
      setError("Please provide a title and choose a file.");
      setStatus("error");
      return;
    }
    setStatus("uploading");
    setError("");
    try {
      await uploadResearchDocument({ title, keywords, file });
      setTitle("");
      setKeywords("");
      setFile(null);
      setStatus("idle");
      onUploaded();
    } catch (err) {
      setError(err.message || "Upload failed.");
      setStatus("error");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3 rounded-xl border border-dashed border-surface-line bg-sky-50/50 p-4">
      <div>
        <label className="mb-1 block text-xs font-medium text-navy-800">Title</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="e.g. AI-Based Flood Detection Using Satellite Images"
          className="w-full rounded-lg border border-surface-line bg-white px-3 py-2 text-sm text-navy-800 outline-none focus:border-blue focus:ring-2 focus:ring-blue/15"
        />
      </div>
      <div>
        <label className="mb-1 block text-xs font-medium text-navy-800">Keywords (comma-separated)</label>
        <input
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          placeholder="Computer Vision, Remote Sensing, Flood Detection"
          className="w-full rounded-lg border border-surface-line bg-white px-3 py-2 text-sm text-navy-800 outline-none focus:border-blue focus:ring-2 focus:ring-blue/15"
        />
      </div>
      <div>
        <label className="mb-1 block text-xs font-medium text-navy-800">File (.pdf, .doc, .docx)</label>
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="w-full text-sm text-navy-800"
        />
      </div>

      {status === "error" && (
        <p className="rounded-lg bg-signal-dormant/5 px-3 py-2 text-xs text-signal-dormant">{error}</p>
      )}

      <button
        type="submit"
        disabled={status === "uploading"}
        className="flex items-center justify-center gap-2 rounded-lg bg-accent-blue px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-2 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {status === "uploading" ? <Loader2 className="h-4 w-4 animate-spin" /> : <Upload className="h-4 w-4" />}
        Upload Research Work
      </button>
    </form>
  );
}

function DocumentRow({ doc, onDeleted }) {
  const [deleting, setDeleting] = useState(false);

  async function handleDelete() {
    setDeleting(true);
    try {
      await deleteResearchDocument(doc.id);
      onDeleted();
    } finally {
      setDeleting(false);
    }
  }

  return (
    <div className="flex items-center justify-between gap-3 border-b border-surface-line py-3 last:border-0">
      <div className="flex min-w-0 items-start gap-3">
        <FileText className="mt-0.5 h-4 w-4 shrink-0 text-blue" />
        <div className="min-w-0">
          <p className="truncate text-sm font-medium text-navy-800">{doc.title}</p>
          <p className="text-xs text-surface-muted">
            {doc.file_name} ┬╖ {doc.file_type.toUpperCase()}
            {doc.uploaded_at ? ` ┬╖ ${new Date(doc.uploaded_at).toLocaleDateString()}` : ""}
          </p>
          {doc.keywords?.length > 0 && (
            <p className="mt-1 text-xs text-blue">{doc.keywords.join(", ")}</p>
          )}
          {doc.extraction_status === "unavailable" && (
            <p className="mt-1 text-[11px] text-surface-muted">Text extraction unavailable for this file.</p>
          )}
        </div>
      </div>
      <button
        onClick={handleDelete}
        disabled={deleting}
        className="shrink-0 rounded-lg p-2 text-surface-muted transition hover:bg-signal-dormant/10 hover:text-signal-dormant disabled:opacity-50"
        title="Delete document"
      >
        <Trash2 className="h-4 w-4" />
      </button>
    </div>
  );
}

export default function Profile() {
  const { data: profile, status, error } = useApiData(getMyProfile);
  const [refreshKey, setRefreshKey] = useState(0);
  const { data: docsData, status: docsStatus } = useApiData(
    listMyResearchDocuments,
    [refreshKey]
  );

  const reload = useCallback(() => setRefreshKey((k) => k + 1), []);

  if (status === "loading") return <LoadingView label="Loading your profile" />;
  if (status === "error") return <ErrorView message={error} />;

  const documents = docsData?.documents || [];

  return (
    <div>
      <PageHeader
        icon={UserCircle}
        title="My Profile"
        description="Your faculty profile, research work, and collaboration history."
      />

      <div className="rounded-panel border border-surface-line bg-white p-6 shadow-panel">
        <h2 className="font-display text-sm font-semibold text-navy-800">Personal Information</h2>
        <dl className="mt-4 grid grid-cols-1 gap-5 sm:grid-cols-2">
          <Field label="Faculty ID" value={profile?.faculty_id} />
          <Field label="Name" value={profile?.name} />
          <Field label="Email" value={profile?.email} />
          <Field label="Department" value={profile?.department} />
          <Field label="Designation" value={profile?.designation} />
        </dl>

        <div className="mt-6">
          <p className="text-xs text-surface-muted">Research Interests</p>
          {profile?.research_interests?.length > 0 ? (
            <div className="mt-2 flex flex-wrap gap-2">
              {profile.research_interests.map((area) => (
                <span key={area} className="rounded-full bg-soft-blue px-3 py-1 text-xs font-medium text-blue">
                  {area}
                </span>
              ))}
            </div>
          ) : (
            <p className="mt-2 text-sm text-surface-muted">No research areas on file.</p>
          )}
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-panel border border-surface-line bg-white p-6 shadow-panel">
          <h2 className="font-display text-sm font-semibold text-navy-800">Publications</h2>
          {profile?.publications?.length > 0 ? (
            <ul className="mt-3 space-y-2">
              {profile.publications.map((p) => (
                <li key={p.id} className="text-sm text-navy-800">
                  {p.title} <span className="text-xs text-surface-muted">({p.year})</span>
                </li>
              ))}
            </ul>
          ) : (
            <EmptyView message="No publications on file." />
          )}
        </div>

        <div className="rounded-panel border border-surface-line bg-white p-6 shadow-panel">
          <h2 className="font-display text-sm font-semibold text-navy-800">Projects</h2>
          {profile?.projects?.length > 0 ? (
            <ul className="mt-3 space-y-2">
              {profile.projects.map((p) => (
                <li key={p.id} className="text-sm text-navy-800">
                  {p.title} <span className="text-xs text-surface-muted">({p.status})</span>
                </li>
              ))}
            </ul>
          ) : (
            <EmptyView message="No projects on file." />
          )}
        </div>
      </div>

      <div className="mt-6 rounded-panel border border-surface-line bg-white p-6 shadow-panel">
        <h2 className="font-display text-sm font-semibold text-navy-800">Existing Research Work</h2>
        <p className="mt-1 text-xs text-surface-muted">
          Upload PDFs/DOC/DOCX of your existing research - this becomes extra evidence when other
          faculty search for collaborators.
        </p>

        <div className="mt-4">
          <UploadForm onUploaded={reload} />
        </div>

        <div className="mt-5">
          {docsStatus === "loading" ? (
            <LoadingView label="Loading your documents" />
          ) : documents.length === 0 ? (
            <EmptyView message="No research documents uploaded yet." />
          ) : (
            <div>
              {documents.map((doc) => (
                <DocumentRow key={doc.id} doc={doc} onDeleted={reload} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}