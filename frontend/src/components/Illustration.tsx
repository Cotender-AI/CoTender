/** Brand illustration: a tender sheet with source-page ferrules and an approval tick. Palette tokens only. */
export function TenderSheetIllustration({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 320 260" className={className} role="img" aria-label="A tender document with approved lines">
      <rect x="70" y="24" width="180" height="224" rx="18" fill="var(--card)" stroke="var(--border)" strokeWidth="2" />
      <rect x="94" y="52" width="84" height="10" rx="5" fill="var(--foreground)" />
      <rect x="94" y="72" width="120" height="7" rx="3.5" fill="var(--border)" />
      {[104, 140, 176].map((y, i) => (
        <g key={y}>
          <rect x="94" y={y} width="132" height="26" rx="8" fill={i === 1 ? "#FBEFE7" : "var(--muted)"} stroke={i === 1 ? "var(--copper)" : "none"} />
          <rect x="102" y={y + 9} width={i === 1 ? 70 : 54} height="8" rx="4" fill="var(--border)" />
          <rect x="190" y={y + 6} width="28" height="14" rx="4" fill="var(--foreground)" />
        </g>
      ))}
      <circle cx="244" cy="196" r="30" fill="var(--earth-green)" />
      <path d="M230 196l10 10 20-22" fill="none" stroke="#fff" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
      <rect x="94" y="222" width="60" height="6" rx="3" fill="url(#earth)" />
      <defs>
        <linearGradient id="earth" x1="0" x2="1">
          <stop offset="0.5" stopColor="var(--earth-green)" />
          <stop offset="0.5" stopColor="var(--earth-yellow)" />
        </linearGradient>
      </defs>
    </svg>
  );
}
