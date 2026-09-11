import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import ExpertiseMap from "./pages/ExpertiseMap";
import CollaborationNetwork from "./pages/CollaborationNetwork";
import InternalOpportunities from "./pages/InternalOpportunities";
import ExternalResearchers from "./pages/ExternalResearchers";
import Funding from "./pages/Funding";
import MouIntelligence from "./pages/MouIntelligence";
import CollaborationTracking from "./pages/CollaborationTracking";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/expertise" element={<ExpertiseMap />} />
          <Route path="/collaboration-network" element={<CollaborationNetwork />} />
          <Route path="/opportunities" element={<InternalOpportunities />} />
          <Route path="/external-researchers" element={<ExternalResearchers />} />
          <Route path="/funding" element={<Funding />} />
          <Route path="/mous" element={<MouIntelligence />} />
          <Route path="/tracking" element={<CollaborationTracking />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
