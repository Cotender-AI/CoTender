import { Suspense } from "react";
import { TenderTabs } from "@/components/TenderTabs";

export default function TenderWorkspaceLayout({ children }: { children: React.ReactNode }) {
  return (
    <Suspense>
      <TenderTabs />
      {children}
    </Suspense>
  );
}
