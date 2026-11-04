"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

// MOCK: skips auth. Real version (FE-02) posts to /api/v1/auth/login; the server sets the httpOnly cookie.
export default function LoginPage() {
  const router = useRouter();
  return (
    <form
      className="space-y-4"
      onSubmit={(e) => {
        e.preventDefault();
        router.push("/dashboard/");
      }}
    >
      <h1 className="text-2xl font-semibold">Log in</h1>
      <label className="block text-sm font-medium">
        Email
        <Input type="email" name="email" autoComplete="email" defaultValue="estimator@demo.co.za" className="mt-1" required />
      </label>
      <label className="block text-sm font-medium">
        Password
        <Input type="password" name="password" autoComplete="current-password" className="mt-1" required />
      </label>
      <Button type="submit" className="w-full">Log in</Button>
      <p className="text-sm text-muted-foreground">
        New to CoTender? <Link href="/register/" className="font-medium text-copper hover:underline">Create a workspace</Link>
      </p>
    </form>
  );
}
