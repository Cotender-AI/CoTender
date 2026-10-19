import { Placeholder } from "@/components/Placeholder";

export default function Page() {
  return (
    <Placeholder title="New tender" issue="FE-03">
      Title, reference, client, location, closing date. <code>POST /api/v1/tenders</code>.
    </Placeholder>
  );
}
