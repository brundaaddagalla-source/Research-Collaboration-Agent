/**
 * Agent 24 API service
 * ---------------------
 * This is the ONLY file that knows the backend's base URL and endpoint paths.
 * Pages/components should always go through the functions exported here
 * instead of calling fetch() directly - this keeps the "React page -> API
 * service -> FastAPI -> mock data -> JSON -> React UI" flow clean and makes
 * it easy to point at a different backend later without touching any page.
 */

const BASE_URL = "http://localhost:8000";

async function request(path) {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request to ${path} failed with status ${response.status}`);
  }
  return response.json();
}

export const getDashboard = () => request("/api/dashboard");
export const getFaculty = () => request("/api/faculty");
export const getExpertise = () => request("/api/expertise");
export const getCollaborations = () => request("/api/collaborations");
export const getOpportunities = () => request("/api/opportunities");
export const getExternalResearchers = () => request("/api/external-researchers");
export const getFunding = () => request("/api/funding");
export const getMous = () => request("/api/mous");
export const getTracking = () => request("/api/tracking");
