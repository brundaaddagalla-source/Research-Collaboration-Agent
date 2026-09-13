/**
 * Agent 24 - current faculty helper
 * ----------------------------------
 * The Faculty Login flow (services/auth.js) only knows the faculty's
 * login identity: { facultyId, name, token }. The research profile
 * (department, designation, research areas, publication counts, ...)
 * lives in the separate `/api/faculty` list (see backend/models/models.py
 * - Faculty vs FacultyCredential are intentionally different tables).
 *
 * This helper joins the two by name so pages can show a real,
 * personalized profile without hardcoding or inventing any data. If no
 * match is found (e.g. a login account without a matching research
 * profile yet), callers get `null` back and should degrade gracefully
 * rather than fabricate details.
 */

function normalize(name) {
  return (name || "").trim().toLowerCase();
}

// faculty: the array returned by getFaculty() -> { faculty: [...] }
// stored: the object returned by getStoredFaculty() -> { facultyId, name, token }
export function matchCurrentFaculty(facultyList, stored) {
  if (!stored || !Array.isArray(facultyList)) return null;
  const target = normalize(stored.name);
  if (!target) return null;
  return facultyList.find((item) => normalize(item.name) === target) || null;
}