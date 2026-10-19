import { Sidebar } from "@/components/Sidebar";

// TODO(FE-02): auth guard - call GET /me on load and redirect to /login on 401.
export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
}
