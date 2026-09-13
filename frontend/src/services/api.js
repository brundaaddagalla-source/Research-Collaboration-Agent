/**
 * Agent 24 API service
 * ---------------------
 * This is the ONLY file that knows the backend's base URL and endpoint paths.
 * Pages/components should always go through the functions exported here
 * instead of calling fetch() directly - this keeps the "React page -> API
 * service -> FastAPI -> mock data -> JSON -> React UI" flow clean and makes
 * it easy to point at a different backend later without touching any page.
 */

import { getToken, clearStoredFaculty } from "./auth";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path) {
  const token = getToken();
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
  });
  if (response.status === 401) {
    // Session expired/invalid - drop it so the next visit to a
    // protected page prompts a fresh login instead of looping on 401s.
    clearStoredFaculty();
  }
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(data?.detail || `Request to ${path} failed with status ${response.status}`);
  }
  return data;
}

async function authedRequest(path, method, body) {
  const token = getToken();
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (response.status === 401) {
    clearStoredFaculty();
  }
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(data?.detail || `Request to ${path} failed with status ${response.status}`);
  }
  return data;
}

async function postRequest(path, body) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(data?.detail || `Request to ${path} failed with status ${response.status}`);
  }
  return data;
}

export const getDashboard = () => request("/api/dashboard");
export const getFaculty = () => request("/api/faculty");
export const getExpertise = () => request("/api/expertise");
export const getCollaborations = () => request("/api/collaborations");
export const getOpportunities = (facultyName, topK = 5) =>
  request(
    `/api/opportunities?faculty_name=${encodeURIComponent(facultyName)}&top_k=${topK}`
  );
export const getExternalResearchers = () => request("/api/external-researchers");
export const getFunding = () => request("/api/funding");
export const getMous = () => request("/api/mous");
export const getTracking = () => request("/api/tracking");

/**
 * ---------------------------------------------------------------------
 * Faculty auth (Faculty ID + password + grid authentication)
 * ---------------------------------------------------------------------
 */

export const requestFacultyGrid = (facultyId) =>
  postRequest("/api/auth/faculty/grid", { faculty_id: facultyId }).then((data) => ({
    gridPositions: data.grid_positions,
  }));

export const facultyLogin = ({ facultyId, password, gridValues }) =>
  postRequest("/api/auth/faculty/login", {
    faculty_id: facultyId,
    password,
    grid_values: gridValues,
  }).then((data) => ({
    faculty: {
      facultyId: data.faculty.faculty_id,
      name: data.faculty.name,
      token: data.access_token,
    },
  }));

/**
 * ---------------------------------------------------------------------
 * Current faculty profile (JWT-derived identity only)
 * ---------------------------------------------------------------------
 */
export const getMyProfile = () => request("/api/faculty/me");

/**
 * ---------------------------------------------------------------------
 * Faculty research documents (upload/list/delete own uploads)
 * ---------------------------------------------------------------------
 */
export const listMyResearchDocuments = () => request("/api/faculty/research-documents");

export async function uploadResearchDocument({ title, keywords, file }) {
  const token = getToken();
  const formData = new FormData();
  formData.append("title", title);
  formData.append("keywords", keywords);
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/api/faculty/research-documents`, {
    method: "POST",
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    body: formData,
  });
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(data?.detail || "Upload failed.");
  }
  return data;
}

export const deleteResearchDocument = (documentId) =>
  authedRequest(`/api/faculty/research-documents/${documentId}`, "DELETE");

/**
 * ---------------------------------------------------------------------
 * Collaboration search (evidence-based, ranked collaborators)
 * ---------------------------------------------------------------------
 */
export const searchCollaborators = (query, topK = 10) =>
  authedRequest("/api/collaborations/search", "POST", { query, top_k: topK });

/**
 * ---------------------------------------------------------------------
 * Collaboration requests
 * ---------------------------------------------------------------------
 * The requester's identity always comes from the JWT on the backend -
 * never sent from here as a body field.
 */
export const createCollaborationRequest = ({
  targetFacultyId,
  targetExternalResearcherId,
  topic,
  proposal,
  reason,
  fundingId,
  mouId,
  universityBenefit,
}) =>
  authedRequest("/api/collaboration-requests", "POST", {
    ...(targetFacultyId
      ? { target_faculty_id: targetFacultyId }
      : {}),
    ...(targetExternalResearcherId
      ? {
          target_external_researcher_id:
            targetExternalResearcherId,
        }
      : {}),
    topic,
    proposal,
    reason,
    funding_id: fundingId ?? null,
    mou_id: mouId ?? null,
    university_benefit: universityBenefit ?? null,
  });

export const getSentRequests = () => request("/api/collaboration-requests/sent");
export const getReceivedRequests = () => request("/api/collaboration-requests/received");
export const getRequestDetail = (id) => request(`/api/collaboration-requests/${id}`);

export const respondToRequestAsFaculty = (id, status, comments) =>
  authedRequest(`/api/collaboration-requests/${id}/faculty-response`, "PATCH", {
    status,
    comments,
  });

// Public - clicked from an emailed one-time link, no login required.
export const respondViaEmailToken = (token) =>
  fetch(`${BASE_URL}/api/collaboration-requests/respond/${encodeURIComponent(token)}`).then(
    async (response) => {
      const data = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(data?.detail || "Could not process this response link.");
      }
      return data;
    }
  );