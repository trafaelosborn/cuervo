# Cuervo Clipper: indexing status and next work

*Updated September 21, 2026. Supersedes the earlier unexecuted OCR plan.*

## Completed

- **Scans covering all 270 catalog dates are held.** The original 267 combined issue PDFs contain 1,148 newspaper pages. Nineteen supplemental source-page PDFs fill three missing four-page issues and seven further pages of November 4, 1921. The resulting collection has 1,167 newspaper pages, excluding repository covers.
- **Existing UNM CONTENTdm OCR is acquired and locally searchable.** This was retrieval of the repository's text, not a fresh Tesseract run or exhaustive correction. Both page metadata and the supplied OCR are preserved.
- **Repository duplication and empty records are reconciled.** The API supplied 272 issue records and 1,189 child-page objects. Two duplicate issue records account for eight pages; fourteen other child transcripts are empty. The canonical index retains 1,167 nonempty page transcripts across 270 dates.
- **A first search pass generated 9,288 unverified leads** across transport/freight, medical/church/post, land/agriculture, school, newspaper, business change and trade geography. Repeated advertisements, syndicated stories and other places are among the matches. This is not an event count.
- **Selected source images have been closely read.** Fourteen additional Clipper front pages join the previously checked December 1, 1922 editorial. The [full-life study](full_life_chronology_2026-09-21.md) combines these with directories, a 1947 regional newspaper observation and prior studies into 57 dated observations and 14 business/institution entries.

## Files to use

- [School and merchant follow-up](school_and_merchant_2026-09-21.md): eight additional front pages visually inspected after the full-life study; 730 overlapping unverified targeted OCR hits, 12 curated observations including prior baselines, and a [correction log](school_and_merchant_2026-09-21/review_corrections.json). Enrollment figures from Newkirk were excluded; Cuervo's 1910 and 1912 numerals were checked against the scans. The July 1922 gasoline item reads fifteen barrels with no time interval.

- [Curated chronology](full_life_chronology_2026-09-21/chronology.json), [register](full_life_chronology_2026-09-21/business_register.json) and [source key](full_life_chronology_2026-09-21/sources.json).
- [Canonical page mapping](full_life_chronology_2026-09-21/canonical_ocr_pages.json), [issue coverage](full_life_chronology_2026-09-21/issue_coverage.json) and [coverage audit](full_life_chronology_2026-09-21/ocr_coverage_audit.json).
- [Unverified search leads](full_life_chronology_2026-09-21/ocr_search_leads.jsonl).
- Per-issue searchable text: `../sources/02_newspapers/cuervo_clipper/repository_ocr_2026-09-21/issues/YYYY-MM-DD.txt`.
- Source metadata, per-page text and retrieval manifest: `../sources/02_newspapers/cuervo_clipper/repository_ocr_2026-09-21/`.
- [Supplemental scans and download manifest](../sources/02_newspapers/cuervo_clipper/supplemental_scans_2026-09-21/download_manifest.json).

## Remaining work

1. Visually verify additional leads for named businesses and institutions, retaining the exact issue, source page and column where practical.
2. Distinguish openings, sales, plans, temporary closures, permanent closures and changes of location. Absence from a later advertisement or directory is not a closing date.
3. Resolve the doctor-recruitment proposal, Sanford's practice move and the Clipper's actual final publication date.
4. Extend named business observations into later regional papers and administrative records, with the 1947 Bond & Wiest listing as one midpoint.
5. Connect the 1910-1912 school sequence to enrollment, residence, transport and the later closure/consolidation decision.

## Coverage limits

The held dates span 1910-1922 but are not an unbroken weekly run. There are no issue dates for 1914-1916, and only four for 1920. All cataloged dates now have scans; this does not establish that every issue or every original page survives. OCR remains noisy and the human reading is selective. The digitized endpoint in December 1922 is not a verified cessation date: the LOC catalog tentatively gives 1923.
