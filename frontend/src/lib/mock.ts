// MOCK DATA for the UI scaffold. Replaced by the generated API client once endpoints are plugged in.
import type { ReviewStatus } from "@/components/StatusBadge";

export type MockTender = {
  id: string;
  reference: string;
  title: string;
  client: string;
  closes: string;
  daysLeft: number;
  counts: Record<ReviewStatus, number>;
};

export const TENDERS: MockTender[] = [
  { id: "t1", reference: "ESKOM/DX/2026/114", title: "Substation LV upgrade, Boksburg", client: "Eskom Distribution", closes: "9 Nov 2026", daysLeft: 7,
    counts: { extracted: 38, corrected: 6, approved: 41, rejected: 2, stale: 0 } },
  { id: "t2", reference: "CJC/EL/0457", title: "Mall retrofit: lighting and DB boards", client: "Cresta Junction Centre", closes: "13 Nov 2026", daysLeft: 11,
    counts: { extracted: 112, corrected: 0, approved: 9, rejected: 0, stale: 0 } },
  { id: "t3", reference: "GDE-HOS-26-031", title: "Clinic generator and changeover", client: "Gauteng Dept. of Health", closes: "20 Nov 2026", daysLeft: 18,
    counts: { extracted: 0, corrected: 0, approved: 0, rejected: 0, stale: 0 } },
  { id: "t4", reference: "MTN/SITE/882", title: "Rooftop site power, 14 sites", client: "MTN SA", closes: "30 Oct 2026", daysLeft: -3,
    counts: { extracted: 0, corrected: 2, approved: 77, rejected: 1, stale: 4 } },
];

export type MockLine = {
  id: string;
  item: string;
  description: string;
  unit: string;
  qty: string | null;
  rate: string | null;
  status: ReviewStatus;
  page: number | null;
};

export const LINES: MockLine[] = [
  { id: "l1", item: "3.1.1", description: "4 core 16mm² PVC/SWA/PVC cable, supply and install", unit: "m", qty: "240.000", rate: "148.50", status: "approved", page: 14 },
  { id: "l2", item: "3.1.2", description: "4 core 35mm² PVC/SWA/PVC cable, supply and install", unit: "m", qty: "85.000", rate: "262.00", status: "extracted", page: 14 },
  { id: "l3", item: "3.2.1", description: "Cable tray 300mm perforated, galvanised, with bends", unit: "m", qty: "120.000", rate: null, status: "corrected", page: 15 },
  { id: "l4", item: "3.2.2", description: "Cable ladder 600mm heavy duty", unit: "m", qty: null, rate: null, status: "extracted", page: 15 },
  { id: "l5", item: "4.1", description: "630A Form 4 main distribution board, complete", unit: "no", qty: "1.000", rate: "184500.00", status: "extracted", page: 17 },
  { id: "l6", item: "4.2", description: "Earth bar and bonding as specified", unit: "sum", qty: "0.000", rate: null, status: "extracted", page: null },
  { id: "l7", item: "5.1", description: "Testing, commissioning and CoC", unit: "sum", qty: "1.000", rate: "22000.00", status: "rejected", page: 21 },
];

export const zar = (v: string | null) =>
  v == null ? "—" : new Intl.NumberFormat("en-ZA", { style: "currency", currency: "ZAR" }).format(Number(v));

/** Display only. Real totals come from the backend (Decimal, ROUND_HALF_UP). */
export const lineTotal = (l: MockLine) =>
  l.qty == null || l.rate == null ? null : (Math.round(Number(l.qty) * Number(l.rate) * 100) / 100).toFixed(2);
