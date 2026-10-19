import { Placeholder } from "@/components/Placeholder";

export default function LoginPage() {
  return (
    <Placeholder title="Log in" issue="FE-02">
      Email + password form → <code>POST /api/v1/auth/login</code>, then go to /dashboard.
      Demo users: admin@demo.co.za / estimator@ / pm@ / reviewer@ (password DemoPass123!).
    </Placeholder>
  );
}
