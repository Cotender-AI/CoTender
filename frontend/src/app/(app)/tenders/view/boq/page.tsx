import { Placeholder } from "@/components/Placeholder";

export default function Page() {
  return (
    <Placeholder title="Bill of quantities" issue="D3">
      Editable table; totals always come from <code>GET /api/v1/tenders/:id/boq</code>.
    </Placeholder>
  );
}
