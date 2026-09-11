import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

export function Layout() {
  return (
    <div className="min-h-screen bg-sky-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="px-6 py-6 lg:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
