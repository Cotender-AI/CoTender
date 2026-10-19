import { Placeholder } from "@/components/Placeholder";

export default function RegisterPage() {
  return (
    <Placeholder title="Create your company workspace" issue="FE-02">
      Company name, your name, email, password → <code>POST /api/v1/auth/register</code>.
    </Placeholder>
  );
}
