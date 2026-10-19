import type { NextConfig } from "next";

// Static export: the built site is plain files served by Azure Static Web Apps.
// Dynamic routes are avoided; pages read ids from the query string (?id=...).
const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
};

export default nextConfig;
