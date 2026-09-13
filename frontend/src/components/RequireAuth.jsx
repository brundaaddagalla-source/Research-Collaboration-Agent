import { Navigate } from "react-router-dom";
import { isAuthenticated } from "../services/auth";

/**
 * Wraps the existing authenticated routes (Layout + pages). Sends
 * unauthenticated visitors to /login without touching anything else
 * about how those routes render.
 */
export function RequireAuth({ children }) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
}