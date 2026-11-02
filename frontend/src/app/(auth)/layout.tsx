import { TenderSheetIllustration } from "@/components/Illustration";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="grid min-h-screen lg:grid-cols-[1fr_30rem]">
      <section className="hidden flex-col justify-between bg-muted/60 p-12 lg:flex">
        <div className="flex items-center gap-2">
          <span className="grid size-8 place-items-center rounded-lg bg-copper font-heading font-bold text-white">C</span>
          <span className="font-heading text-xl font-semibold">CoTender</span>
        </div>
        <div>
          <TenderSheetIllustration className="mb-10 w-72" />
          <h2 className="max-w-lg font-heading text-5xl font-semibold leading-[1.08] tracking-tight">
            Every line traced to its page.
          </h2>
          <p className="mt-4 max-w-md text-lg text-muted-foreground">
            Upload the tender pack. CoTender reads the BoQ and requirements. You approve what&apos;s right.
          </p>
        </div>
        <div className="earth-stripe h-1.5 w-32 rounded-full" />
      </section>
      <section className="page-in flex items-center justify-center p-8">
        <div className="w-full max-w-sm">{children}</div>
      </section>
    </main>
  );
}
