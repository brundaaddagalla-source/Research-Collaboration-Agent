import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "./components/Layout";
import { RequireAuth } from "./components/RequireAuth";
import FacultyLogin from "./pages/FacultyLogin";
import Dashboard from "./pages/Dashboard";
import MyRequests from "./pages/MyRequests";
import MyCollaborations from "./pages/MyCollaborations";
import Profile from "./pages/Profile";
import CollaborationResponse from "./pages/CollaborationResponse";

// The previous admin-style pages (ExpertiseMap, CollaborationNetwork,
// InternalOpportunities, ExternalResearchers, Funding, MouIntelligence,
// CollaborationTracking) are intentionally no longer routed here - this
// is now a faculty-facing app. Their files and the backend routes/agents
// behind them are untouched, so they can be reintroduced (e.g. behind an
// admin view) later without any rework.
//
// Collaborate.jsx (the standalone "Faculty Search" page) is likewise no
// longer routed: search now happens directly on the Dashboard via the
// same CollaborationAssistant component, so a separate page would be a
// duplicate of the same search. The file itself is left untouched.

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<FacultyLogin />} />

        {/* Public - reached by clicking Accept/Reject/Approve/Reject in an
            email. No login required: the one-time token itself is the
            authorization (see backend routes/collaboration_requests.py). */}
        <Route path="/login/collaboration-response/:token" element={<CollaborationResponse />} />

        <Route
          element={
            <RequireAuth>
              <Layout />
            </RequireAuth>
          }
        >
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          {/* Old bookmarks/links to the removed standalone search page
              land back on the Dashboard, where the same search now lives. */}
          <Route path="/collaborate" element={<Navigate to="/dashboard" replace />} />
          <Route path="/requests" element={<MyRequests />} />
          <Route path="/collaborations" element={<MyCollaborations />} />
          <Route path="/profile" element={<Profile />} />
        </Route>

        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;