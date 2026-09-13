import { Search } from "lucide-react";
import { PageHeader } from "../components/PageHeader";
import { CollaborationAssistant } from "../components/CollaborationAssistant";

export default function Collaborate() {
  return (
    <div>
      <PageHeader
        icon={Search}
        title="Find Collaborators"
        description="Discover researchers whose expertise complements yours."
      />

      <CollaborationAssistant topK={8} />
    </div>
  );
}
