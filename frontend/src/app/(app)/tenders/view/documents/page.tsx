import { Placeholder } from "@/components/Placeholder";

export default function Page() {
  return (
    <Placeholder title="Documents" issue="FE-04">
      Upload (PDF, DOCX, XLSX, CSV, max 20 MB), then poll <code>GET /api/v1/jobs/:id</code> every 3 s.
    </Placeholder>
  );
}
