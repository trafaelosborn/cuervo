# Cuervo — response to the first editor pass

September 29, 2026. Revision 5 preserves Revision 4 as the review baseline. Page numbers in the editor's comments refer to Revision 4; the new proof repaginates automatically.

## Substantive findings

| Editor's point | Resolution in Revision 5 |
|---|---|
| p. 4: “That July” could mean July 2020 | Chapter 1 now says **“In July 2026.”** The ranch purchase remains dated to 2020. |
| p. 20: fall 1899 conflicts with an August account | Chapter 2 uses **1899**, without a season. Note 4 explains that both statements occur in Grubbs. His printed p. 97 / PDF p. 229 was visually checked; the August date is in footnote 3. No exact opening day is inferred. |
| p. 11: ambiguous housing/AC pronoun | Chapter 1 names **Santa Rosa's year-round housing** and then “the town's population.” The county room-unit evidence and Cuervo limitations remain in note 12. |
| p. 132: Golden State end date insufficiently supported | The *Congressional Record*, April 25, 1968, printed p. 10779 / PDF p. 88, left column under “Restatement of Operating Costs,” explicitly reports discontinuance on **March 25, 1968**. The scan was enlarged and read; OCR incorrectly renders the day as 26. Chapter 6 attributes the report and uses **March 1968**. Note 14 supplies the exact passage and public scan. The 1968 timeline marker remains supported. An exact last-run convention is not needed for this book's argument. |
| p. 132: 103-car siding locator | Chapter 6 names the October 1958 and September 1959 timetables and adds a note call immediately after the siding paragraph. Note 13 gives timetable 52, printed p. 9 / PDF p. 11, and timetable 53, printed p. 7 / PDF p. 9, alongside the 1967 92-car listing. The 1958 Cuervo row was visually checked. The different capacity counts still do not establish shortened track. |
| pp. 55–56: unstated 1935 farm denominator | Chapter 3 states **851 farms in 1935**, explains the intervening rise from 596 in 1930, and keeps the later decline distinct. Note 23 identifies the farm-count table; note 25 identifies the off-farm-work table and denominator. This explains the presentation without inventing a cause for the rise. |

## Dates confirmed rather than changed

- **September 14, 1911; February 8, 1912; April 4, 1912:** the original Clipper mastheads all explicitly say **Thursday**. The opening date stands. No particular date for a publication-day change is inferred.
- **Parish bulletin:** its cover is dated **December 21, 2025**; the collection report on PDF p. 2 is headed **12/6 12/7** and includes “Cuervo Function 170.00.” Chapter 8 and note 9 distinguish publication and collection dates. Both original pages were visually checked.
- **Inflation:** the [Minneapolis Fed historical CPI table](https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1800-) was checked on September 29, 2026. Its 2025 value is 967.5; relevant earlier values include 1899/1900 = 25, 1904 = 27, 1910/1911 = 28, 1915 = 30.4 and 1932 = 41.0. The pre-1913 values are reconstructed estimates. The amounts in question remain correctly rounded: school bonds approximately $138,214 → $140,000; loan $2,123,780 → $2.1 million; monthly salary $2,687.50 → $2,700. Notes now identify the convention beside all three conversions.

## Apparatus and prose

- All **174 notes** are rewritten as reader-facing citations and methods. They identify publications, dates, tables, printed/PDF pages, manuscript census districts and sheets, or county survey/card identifiers. Locally supplied county documents are described as copies in the author's collection.
- “Working documentation,” internal source-register codes, dated study references, local file links and research-process narration are removed from the reading apparatus. The old research trails remain intact in Revision 4 and the research archive.
- All **220 existing note calls** remain, with **one additional call** beside the siding-capacity paragraph: **221** in total.
- **32 cadence edits** reduce repeated demonstrations of what a source “establishes” and repeated section-ending qualifications. Main-text occurrences of “establish/establishes/established” fall from 84 to 61. Material limits on geography, causation, accounting, source conflicts and uncertain dates remain.
- Apostrophes and quotation marks are normalized in prose, notes and typeset captions. Four-digit year ranges use en dashes. Source identifiers, URLs, enumeration districts and compound printed page numbers retain their meaningful punctuation. Original source-image typography is preserved.
- All eighteen author photographs, analytical figures and source-image plates are retained. This revision adds no new research chapter or theoretical claim.

## What this pass does not finish

The chapter notes are ready for readers, but a consolidated bibliography and index remain to be compiled. Final print design and a physical production proof remain separate tasks. This pass checks revised layout and source-image placement; it is not an independent second scholarly review of every figure or a new double transcription of the census.

## Reproducibility

- `editorial-changes.json` records every substantive or cadence replacement against Revision 4.
- `revision05_notes.py` contains the replacement notes; `edit_book_revision05.py` checks that all original note definitions remain and generates the eight chapter files.
- `build_book_revision05.py` creates the combined manuscript, linked PDF and build manifest.
- `check_book_revision05.py` checks paragraph preservation, note destinations, contents links, bookmarks and page count, and prepares the visual overview sheets.
- `validation.json` records the final checks; the PDF's hash is recorded in both validation and build manifests.

## Final verification

The released proof has **180 pages and 31,075 main-text words**, with 174 notes, 221 internal note calls, eight chapter bookmarks and 41 visual positions, including eighteen author photographs. All original note calls remain; the siding paragraph adds one. Text preservation and internal destinations pass. The export contains no straight apostrophes, straight double quotation marks, working-note references or local-file links. Year ranges retain en dashes.

All pages were rendered. Every preliminary page was visually reviewed; final changed layouts and representative source-note pages were inspected again. The final render comparison and review record identify the pages checked. Chapter 4's stranded closing paragraph was removed by tightening its repetitive transition. No short orphan pages remain. Public links are syntactically valid HTTPS targets; this pass does not claim a fresh availability test of every remote server.

Revision 4 remains byte-for-byte unchanged. Final PDF SHA-256: `c7f5f7138fab067184872ee50f6891753c6445b964a80e88853a295c783271c1`.

