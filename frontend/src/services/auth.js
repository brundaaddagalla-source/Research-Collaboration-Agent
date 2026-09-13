/**
 * Agent 24 auth state (frontend-only)
 * ------------------------------------
 * Minimal helper around localStorage so the Faculty Login page and the
 * router can agree on whether someone is logged in, without pulling in
 * a routing/auth library. This does NOT verify anything itself - the
 * real JWT is issued and checked by the backend (see routes/auth.py);
 * this module just stores/reads what the backend returned. See
 * `services/api.js` for the login API calls.
 *
 * Stored value shape:
 *   { facultyId: string, name?: string, token: string, loginAt: string }
 */

const STORAGE_KEY = "agent24_faculty";

export function getStoredFaculty() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function setStoredFaculty(faculty) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(faculty));
  } catch {
    // localStorage unavailable (private mode, etc.) - fail silently,
    // the app will just prompt for login again next time.
  }
}

export function clearStoredFaculty() {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // no-op
  }
}

export function isAuthenticated() {
  return getStoredFaculty() !== null;
}

// The JWT to send as `Authorization: Bearer <token>` on API calls.
// Returns null if no one is logged in (or the stored record predates
// JWT auth and has no token).
export function getToken() {
  return getStoredFaculty()?.token ?? null;
}