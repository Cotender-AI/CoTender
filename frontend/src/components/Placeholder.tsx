// Marks a screen that is still to be built. Remove it when the issue is done.
export function Placeholder({ title, issue, children }: {
  title: string;
  issue: string;
  children?: React.ReactNode;
}) {
  return (
    <section>
      <h1 className="text-2xl font-semibold text-slate-900">{title}</h1>
      <p className="mt-2 inline-block rounded bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-900">
        To build in issue {issue}
      </p>
      {children && <div className="mt-6 text-sm text-slate-700">{children}</div>}
    </section>
  );
}
