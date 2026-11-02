import { cn } from "@/lib/utils";

/** Source-page tag, styled like a cable ferrule. No page = cannot be approved (rule 9: no_source). */
export function Ferrule({ page, className }: { page?: number | null; className?: string }) {
  if (page == null) {
    return (
      <span className={cn("num inline-flex items-center rounded-sm border border-copper px-1.5 text-[11px] leading-5 text-copper", className)}>
        no source
      </span>
    );
  }
  return (
    <span
      title={`Source: page ${page}`}
      className={cn("num inline-flex items-center rounded-sm bg-foreground px-1.5 text-[11px] leading-5 text-background", className)}
    >
      p.{page}
    </span>
  );
}
