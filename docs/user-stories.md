# IntelTPS user stories: RFQ to compliance checklist

Visual version: `visuals/rfq-workflow.html`.

**Epic:** As an estimator at an electrical subcontractor, I want to upload a municipal RFQ and get every requirement and compliance condition in one register with page references, so that I don't miss anything that would disqualify our bid.

## US-01 · Create tender

As an estimator, I want to open a tender workspace for an RFQ I've received, so that every document, requirement and task for it sits in one place.

**Acceptance criteria**
- [ ] Title, reference, client and closing date are required
- [ ] The tender is visible only to my organisation
- [ ] The closing date shows on the dashboard countdown

**FRs:** FR-06, FR-08, FR-44

**System steps**
1. Form posts to `POST /tenders` with the session cookie
2. API checks the user's role and takes the organisation from the token
3. Service validates the closing date and sets status `draft`
4. Repository inserts the tender, scoped to the organisation

Writes: `tenders`, `audit_events`

## US-02 · Upload RFQ

As an estimator, I want to upload the RFQ PDF and see that it was received, so that I am not left guessing whether processing started.

**Acceptance criteria**
- [ ] PDF, DOCX, XLSX and CSV accepted; anything else rejected with a clear message
- [ ] Confirmation within 5 seconds with a visible status
- [ ] Re-uploading creates version 2 and keeps version 1

**FRs:** FR-07, FR-09, FR-11, FR-12

**System steps**
1. Browser streams the file to `POST /tenders/{id}/documents`
2. API reads the first bytes: a real PDF, under 20 MB, within the plan's page limit
3. File stored privately in Blob under the organisation's folder; SHA-256 computed
4. Document and job rows saved in one transaction; job id put on the queue
5. API answers 202 in under 5 seconds; the screen starts polling the job

Writes: `documents`, `extraction_jobs`, `usage_counters`

## US-03 · Read pages

As an estimator, I want to see processing progress page by page, so that I know when the RFQ is ready and which pages were scanned.

**Acceptance criteria**
- [ ] Progress and status update without refreshing
- [ ] Scanned pages are marked as OCR
- [ ] A failure shows a reason and a retry button

**FRs:** FR-13, FR-14, FR-15, FR-16

**System steps**
1. Queue wakes the worker; it claims the job and marks it running
2. Worker downloads the file from Blob
3. PyMuPDF reads the 22 pages that have embedded text
4. Pages 20 and 21 are scans, so Document Intelligence OCRs them
5. Each page's text is saved with its page number; progress updates as it goes

Writes: `document_pages`, `extraction_jobs.progress`

## US-04 · Find requirements

As an estimator, I want the system to find every requirement, date and compliance condition in the RFQ, so that I don't have to read 24 pages line by line to build a checklist.

**Acceptance criteria**
- [ ] Every item has a source page
- [ ] Items are classed mandatory, conditional or information
- [ ] Disqualifying conditions and deadlines are flagged
- [ ] Nothing is marked verified until a person approves it

**FRs:** FR-17, FR-18, FR-19, FR-21

**System steps**
1. Worker sends page-sized chunks to Azure OpenAI, marked as document data, not instructions
2. The model must answer in the requirement JSON schema; anything else is rejected
3. Pydantic validates each item and checks its page exists
4. Rules add flags: dates, disqualifiers, grading thresholds, low OCR confidence
5. 22 items saved as *extracted*, each with its source page; job succeeded

Writes: `tender_requirements`, `audit_events`

## US-05 · Compliance register

As an estimator, I want one consolidated register of all requirements grouped by category, so that I can see at a glance what we must submit, prove and comply with.

**Acceptance criteria**
- [ ] Grouped into dates, returnables, eligibility, technical, commercial
- [ ] Filter by type and review status
- [ ] Each item shows its page and flags
- [ ] The register says it is extracted information, not a compliance ruling

**FRs:** FR-21, FR-22, FR-23

**System steps**
1. Screen calls `GET /tenders/{id}/requirements`
2. Repository returns only this organisation's items, grouped by category
3. Counts by type and review status are computed on the server
4. Flags are listed first so the riskiest items get reviewed first

Writes: `(read only)`

## US-06 · Review at source

As an estimator, I want to check each item against the page it came from and approve or correct it, so that the checklist is something I can trust and defend.

**Acceptance criteria**
- [ ] Source page opens beside the item with the wording highlighted
- [ ] Original wording is kept after a correction
- [ ] Approved items show who approved them and when

**FRs:** FR-19, FR-20, FR-26

**System steps**
1. Screen shows the RFQ page beside the extracted item, wording highlighted
2. Approve calls `PATCH /requirements/{id}` with the reviewer stamped
3. A correction keeps the original wording and logs a field revision
4. Every change writes an audit event

Writes: `tender_requirements`, `field_revisions`, `audit_events`

## US-07 · Assign and track

As a project manager, I want to assign each requirement to a person with a due date, so that nothing falls through before the briefing and closing dates.

**Acceptance criteria**
- [ ] Only organisation members can be assigned
- [ ] Overdue and due-soon items are highlighted
- [ ] Status changes are recorded

**FRs:** FR-43, FR-44, FR-45, FR-46

**System steps**
1. Assigning calls `PATCH /requirements/{id}` with an owner and due date
2. Owner must be a member of the same organisation
3. A daily job creates reminders for items due within 3 days
4. The dashboard shows the site briefing as the next hard deadline

Writes: `tasks`, `notifications`, `audit_events`

## US-08 · Export checklist

As an estimator, I want to export the compliance checklist as a PDF, so that the team can work through it while compiling the bid pack.

**Acceptance criteria**
- [ ] Shows source page for each item
- [ ] Draft if any mandatory item is unapproved
- [ ] Includes version, generation date and disclaimer
- [ ] Export is recorded in the audit trail

**FRs:** FR-23, FR-39, FR-40, FR-41, FR-42

**System steps**
1. `POST /tenders/{id}/exports` builds the checklist PDF
2. Only approved items are listed as verified; the rest are marked draft
3. Header carries version, date and source document; footer carries the disclaimer
4. File saved to Blob; download via a 5-minute link; export audited

Writes: `exports`, `audit_events`

## Example compliance register (fictional RFQ ELEC-2026-114)

Use as a test fixture shape for the requirement extractor.

| ID | Category | Requirement | Type | Page | Flag |
| --- | --- | --- | --- | --- | --- |
| R01 | Key dates | Bids close 14 November 2026 at 11:00; late bids will not be accepted | Mandatory | 1 | Deadline |
| R02 | Key dates | Compulsory site briefing on 28 October 2026 at 10:00 at the Ward 7 hall; bidders who do not attend will be disqualified | Mandatory | 2 | Disqualifying if missed |
| R03 | Key dates | Bids must remain valid for 90 days after the closing date | Mandatory | 3 |  |
| R04 | Key dates | Technical questions in writing by 4 November 2026 | Information | 2 |  |
| R05 | Returnable documents | SBD 1 Invitation to Bid, completed and signed | Mandatory | 5 |  |
| R06 | Returnable documents | SBD 4 Bidder's Disclosure, completed and signed | Mandatory | 7 |  |
| R07 | Returnable documents | SBD 6.1 preference points claim form, only if claiming preference points | Conditional | 9 |  |
| R08 | Returnable documents | Valid B-BBEE certificate or sworn affidavit, required to claim preference points | Conditional | 9 |  |
| R09 | Returnable documents | Pricing schedule completed in black ink; no correction fluid | Mandatory | 20 | Low OCR confidence, check wording |
| R10 | Eligibility and compliance | Bidder registered on the Central Supplier Database; attach CSD summary report | Mandatory | 4 |  |
| R11 | Eligibility and compliance | Tax compliance status confirmed through a valid SARS PIN | Mandatory | 4 |  |
| R12 | Eligibility and compliance | CIDB grading of 3EP or higher | Mandatory | 4 | Check your grading |
| R13 | Eligibility and compliance | Registered electrical contractor with the Department of Employment and Labour; attach certificate | Mandatory | 11 |  |
| R14 | Eligibility and compliance | Municipal rates and services accounts not in arrears for more than 90 days | Mandatory | 6 |  |
| R15 | Eligibility and compliance | Letter of good standing in terms of COIDA | Mandatory | 11 |  |
| R16 | Technical | Installation to SANS 10142-1; Certificate of Compliance issued on completion | Mandatory | 13 |  |
| R17 | Technical | All cable to comply with SANS 1507 | Mandatory | 14 |  |
| R18 | Technical | At least three similar projects in the last five years, with contactable references | Mandatory | 12 | Scored in functionality |
| R19 | Commercial | Prices firm and inclusive of VAT at 15% | Mandatory | 20 |  |
| R20 | Commercial | 10% retention held until practical completion | Information | 17 |  |
| R21 | Commercial | Penalty of R2,500 per calendar day of late completion | Information | 17 |  |
| R22 | Commercial | Evaluated on the 80/20 preference point system | Information | 8 |  |
