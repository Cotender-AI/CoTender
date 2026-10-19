// The only way screens talk to the backend. Types come from docs/openapi.json:
// after the API contract changes, run `npm run gen:api`.
import createClient from "openapi-fetch";
import type { paths } from "./schema";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const api = createClient<paths>({
  baseUrl: API_URL,
  credentials: "include", // auth lives in httpOnly cookies (block A1)
});

export type ApiError = { error: { code: string; message: string; details?: unknown } };

/** Turn the standard error body into a message people can read. */
export function errorMessage(err: unknown): string {
  const e = err as Partial<ApiError> | undefined;
  return e?.error?.message ?? "Something went wrong. Please try again.";
}
