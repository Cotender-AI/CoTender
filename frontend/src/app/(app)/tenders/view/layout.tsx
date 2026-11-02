import { Suspense } from "react";
import { TenderJourney } from "@/components/TenderJourney";
import { TenderTabs } from "@/components/TenderTabs";

export default function TenderWorkspaceLayout({ children }: { children: React.ReactNode }) {
  return (
    <Suspense>
      <TenderJourney />
      <TenderTabs />
      {children}
    </Suspense>
  );
}
