"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Bell, Menu, Search, User } from "lucide-react";
import { toast } from "sonner";
import { api, errorMessage } from "@/api/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { NavLinks } from "./Sidebar";

export function TopBar() {
  const router = useRouter();
  const [navOpen, setNavOpen] = useState(false);
  const [query, setQuery] = useState("");

  function onSearch(e: React.FormEvent) {
    e.preventDefault();
    const q = query.trim();
    router.push(q ? `/tenders/?q=${encodeURIComponent(q)}` : "/tenders/");
  }

  async function onLogout() {
    const { error } = await api.POST("/api/v1/auth/logout");
    if (error) {
      toast.error(errorMessage(error));
      return;
    }
    router.push("/login/");
  }

  return (
    <header className="flex h-16 items-center gap-3 sticky top-0 z-20 border-b border-border/60 bg-card/80 px-4 backdrop-blur-xl">
      <Sheet open={navOpen} onOpenChange={setNavOpen}>
        <SheetTrigger
          render={<Button variant="ghost" size="icon" className="md:hidden" aria-label="Open menu" />}
        >
          <Menu />
        </SheetTrigger>
        <SheetContent side="left" className="w-60 border-sidebar-border bg-sidebar p-4 text-sidebar-foreground">
          <SheetHeader className="p-0">
            <SheetTitle className="font-heading">CoTender</SheetTitle>
          </SheetHeader>
          <nav className="mt-4 flex flex-col gap-1">
            <NavLinks onNavigate={() => setNavOpen(false)} />
          </nav>
        </SheetContent>
      </Sheet>

      <form onSubmit={onSearch} className="relative max-w-sm flex-1" role="search">
        <Search className="absolute left-2.5 top-2.5 size-4 text-slate-400" />
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search tenders"
          aria-label="Search tenders"
          className="pl-8"
        />
      </form>

      <div className="ml-auto flex items-center gap-1">
        {/* Placeholder until A5-NOTIFY / FE-07 wire up GET /notifications. */}
        <Button variant="ghost" size="icon" aria-label="Notifications">
          <Bell />
        </Button>
        <DropdownMenu>
          <DropdownMenuTrigger render={<Button variant="ghost" size="icon" aria-label="User menu" />}>
            <User />
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuGroup>
              <DropdownMenuLabel>Account</DropdownMenuLabel>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={onLogout}>Log out</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
