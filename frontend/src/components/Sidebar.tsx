"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/dashboard/", label: "Dashboard" },
  { href: "/tenders/", label: "Tenders" },
  { href: "/suppliers/", label: "Suppliers" },
  { href: "/settings/", label: "Settings" },
];

export function Sidebar() {
  const path = usePathname();
  return (
    <nav className="flex w-56 shrink-0 flex-col gap-1 border-r border-slate-200 bg-white p-4">
      <div className="mb-6 px-2 text-lg font-semibold text-slate-900">CoTender</div>
      {NAV.map((item) => {
        const active = path.startsWith(item.href);
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`rounded-md px-2 py-1.5 text-sm ${
              active ? "bg-slate-900 text-white" : "text-slate-700 hover:bg-slate-100"
            }`}
          >
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
