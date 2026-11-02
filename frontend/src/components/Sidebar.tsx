"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ApiHealth } from "./ApiHealth";
import { NAV } from "./nav";

// Desktop sidebar; hidden below md, where the top bar opens the same links in a sheet.
export function NavLinks({ onNavigate }: { onNavigate?: () => void }) {
  const path = usePathname();
  return (
    <>
      {NAV.map((item) => {
        const active = path.startsWith(item.href);
        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={onNavigate}
            aria-current={active ? "page" : undefined}
            className={`flex items-center gap-2 rounded-md px-2.5 py-2 text-sm transition-colors ${
              active
                ? "bg-sidebar-accent font-medium text-foreground"
                : "text-sidebar-foreground/80 hover:bg-sidebar-accent/60 hover:text-foreground"
            }`}
          >
            <span className={`h-4 w-0.5 rounded-full ${active ? "bg-copper" : "bg-transparent"}`} />
            {item.label}
          </Link>
        );
      })}
    </>
  );
}

export function Brand() {
  return (
    <div className="flex items-center gap-2 px-2.5">
      <span className="grid size-7 place-items-center rounded-md bg-copper font-heading text-sm font-bold text-white">C</span>
      <span className="font-heading text-lg font-semibold tracking-tight text-foreground">CoTender</span>
    </div>
  );
}

export function Sidebar() {
  return (
    <nav className="sticky top-0 hidden h-screen w-60 shrink-0 flex-col gap-1 border-r border-sidebar-border bg-sidebar p-4 md:flex">
      <div className="mb-6 mt-1"><Brand /></div>
      <NavLinks />
      <ApiHealth />
    </nav>
  );
}
