// MOCK DATA for the checklist scaffold, shaped like docs/user-stories.md "Example compliance register".
// Replaced by GET /api/v1/tenders/{id}/checklist (FE-06 / C3).

export type ChecklistStatus = "open" | "in_progress" | "done" | "not_applicable";
export type Mandatory = "mandatory" | "conditional" | "optional";

export type ChecklistItem = {
  id: string;
  category: string;
  text: string;
  mandatory: Mandatory;
  page: number;
  flag?: string;
  /** The contractor must attach their own file (certificate, report, signed form). */
  needsFile: boolean;
  /** Plain-language hint on how to get it. */
  hint?: string;
  status: ChecklistStatus;
  file?: string;
  assignee: string;
  due: string;
};

export const CATEGORIES = [
  "Key dates",
  "Returnable documents",
  "Eligibility and compliance",
  "Technical",
  "Commercial",
] as const;

const item = (
  id: string, category: string, text: string, mandatory: Mandatory, page: number,
  o: Partial<ChecklistItem> = {},
): ChecklistItem => ({
  id, category, text, mandatory, page, needsFile: false, status: "open", assignee: "You", due: "10 Nov", ...o,
});

export const CHECKLIST: ChecklistItem[] = [
  item("R01", "Key dates", "Bids close 14 November 2026 at 11:00. Late bids are not accepted.", "mandatory", 1, { flag: "Deadline", status: "done" }),
  item("R02", "Key dates", "Attend the compulsory site briefing on 28 October 2026 at 10:00, Ward 7 hall. Bidders who miss it are disqualified.", "mandatory", 2, { flag: "Disqualifying if missed", status: "done" }),
  item("R03", "Key dates", "Keep your bid valid for 90 days after the closing date.", "mandatory", 3),
  item("R04", "Key dates", "Send technical questions in writing by 4 November 2026.", "optional", 2),

  item("R05", "Returnable documents", "SBD 1 Invitation to Bid, completed and signed", "mandatory", 5, { needsFile: true, hint: "Sign every page where it says 'signature'.", file: "SBD1_signed.pdf", status: "done" }),
  item("R06", "Returnable documents", "SBD 4 Bidder's Disclosure, completed and signed", "mandatory", 7, { needsFile: true, hint: "List any family or business links to the municipality.", status: "in_progress", assignee: "Thandi (PM)", due: "6 Nov" }),
  item("R07", "Returnable documents", "SBD 6.1 preference points claim form", "conditional", 9, { needsFile: true, hint: "Only if you are claiming preference points." }),
  item("R08", "Returnable documents", "Valid B-BBEE certificate or sworn affidavit", "conditional", 9, { needsFile: true, hint: "Needed to claim preference points. Check the expiry date.", flag: "Check expiry" }),
  item("R09", "Returnable documents", "Pricing schedule completed in black ink, no correction fluid", "mandatory", 20, { needsFile: true, flag: "Check wording: scan was low quality" }),

  item("R10", "Eligibility and compliance", "Registered on the Central Supplier Database. Attach the CSD summary report.", "mandatory", 4, { needsFile: true, hint: "Download it from the CSD website. It must be dated this month." }),
  item("R11", "Eligibility and compliance", "Tax compliance status confirmed through a valid SARS PIN", "mandatory", 4, { needsFile: true, hint: "Request the PIN on SARS eFiling." }),
  item("R12", "Eligibility and compliance", "CIDB grading of 3EP or higher", "mandatory", 4, { flag: "Check your grading" }),
  item("R13", "Eligibility and compliance", "Registered electrical contractor with the Department of Employment and Labour. Attach the certificate.", "mandatory", 11, { needsFile: true }),
  item("R14", "Eligibility and compliance", "Municipal rates and services accounts not more than 90 days in arrears", "mandatory", 6, { needsFile: true, hint: "Attach a recent statement or clearance letter." }),
  item("R15", "Eligibility and compliance", "Letter of good standing in terms of COIDA", "mandatory", 11, { needsFile: true, hint: "Request it from the Compensation Fund. It expires each year." }),

  item("R16", "Technical", "Install to SANS 10142-1 and issue a Certificate of Compliance on completion", "mandatory", 13),
  item("R17", "Technical", "All cable must comply with SANS 1507", "mandatory", 14),
  item("R18", "Technical", "At least three similar projects in the last five years, with contactable references", "mandatory", 12, { needsFile: true, flag: "Scored in functionality", hint: "List client, value, year and a phone number for each." }),

  item("R19", "Commercial", "Prices must be firm and include VAT at 15%", "mandatory", 20),
  item("R20", "Commercial", "10% retention is held until practical completion", "optional", 17),
  item("R21", "Commercial", "Penalty of R2,500 per calendar day of late completion", "optional", 17),
  item("R22", "Commercial", "Evaluated on the 80/20 preference point system", "optional", 8),
];
