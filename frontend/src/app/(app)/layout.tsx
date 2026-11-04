import { Sidebar } from "@/components/Sidebar";
import { TopBar } from "@/components/TopBar";

// TODO(FE-02): auth guard - call GET /me on load and redirect to /login on 401.
export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar />
        <main className="page-in flex-1 p-5 md:p-10">{children}</main>
      </div>
    </div>
  );
}
