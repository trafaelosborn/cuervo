# Cuervo Clipper scan intake — September 17, 2026

> **September 21 update superseding the status below:** all 270 catalog dates now have held scans. Nineteen additional source-page PDFs fill the three missing four-page issues and seven further pages of November 4, 1921, bringing the total to 1,167 newspaper pages. UNM's repository OCR has been acquired and indexed; selected findings are visually verified in the [full-life study](full_life_chronology_2026-09-21.md). Historical gaps remain; this is not every issue ever published.
>
> **Correction to the preliminary editorial reading below:** the Santa Rosa paper is the **Public Voice**, not the Democratic Voice; the teaching contract concerns **Charles Gerhardt**, not Hicks. The claimed reference to her husband's health was an erroneous first reading and is withdrawn. Use the [September 17 deep dive](deep_dive_2026-09-17.md) and September 21 study for the corrected interpretation. The older intake text is retained as a dated audit record.

## Verified holdings

Taylor supplied **267 issue PDFs**, totaling **1,415 PDF pages** and **4.35 GB** (decimal). Each contains a UNM repository cover, leaving **1,148 scanned newspaper pages**. All 267 files passed PDF parsing and page-structure checks. There are no duplicate issue dates or identical-file hashes. All 267 filename dates agree with the date printed on the repository cover and match entries in the existing 270-issue catalog index.

This checks file integrity and catalog coverage; it does not certify that every issue contains every original printed page. Newspaper mastheads were visually checked for January 7, 1910; August 1, 1919; November 4, 1921; and December 1, 1922. All four agree with their catalog dates. Source damage is visible on some pages.

## Three catalog issues not found in the local folder

- [1910-02-11](https://digitalrepository.unm.edu/cuervo_clipper_news/5)
- [1912-02-22](https://digitalrepository.unm.edu/cuervo_clipper_news/76)
- [1917-09-28](https://digitalrepository.unm.edu/cuervo_clipper_news/150)

No matching Clipper PDFs were found in the standard Downloads folder during this check. These may still be elsewhere or need another download. The earlier single-page February 4, 1910 file is retained separately and is excluded from the 267-issue count.

## Page counts and OCR readiness

| PDF pages, including cover | Number of issue files |
|---:|---:|
| 2 | 1 |
| 5 | 243 |
| 6 | 1 |
| 7 | 3 |
| 9 | 19 |

[November 4, 1921](../sources/02_newspapers/cuervo_clipper/full_scans/The%20Cuervo%20Clipper,%2011-04-1921%20-%20The%20Cuervo%20Clipper%2011-04-1921.pdf) contains only the repository cover and one scanned front page. It is a valid PDF, but whether this represents the entire surviving repository issue remains unverified. Do not assume the download is corrupt or the original issue was only one page.

The first newspaper scan in **every one of the 267 PDFs** has no extractable text layer; the covers do have text. A text search returning only cover metadata would therefore miss the newspaper contents. Full-corpus OCR has not been run. OCR should skip the repository covers, retain original PDFs, preserve the PDF-page-to-scan-page mapping, and treat extracted hits as leads requiring visual verification.

## A promising first observation

The [December 1, 1922 front page](../sources/02_newspapers/cuervo_clipper/full_scans/The%20Cuervo%20Clipper,%2012-01-1922%20-%20The%20Cuervo%20Clipper%2012-01-1922.pdf) (PDF page 2), in **“To My Clipper Readers,”** contains Katharine A. Hick's announcement that she is withdrawing financial involvement in the Clipper. She argues that current economic conditions favor supporting one strong county weekly at the county seat and encourages support for Mr. Gerhardt's Santa Rosa paper, the Democratic Voice. She also refers to her county teaching contract and her husband's health.

This is a contemporary statement about newspaper economics and county-seat concentration decades before I-40. It is an editor's argument and explanation, not independent proof of a town-wide economic mechanism. The announcement does not itself establish the exact date on which the Clipper stopped publishing. Full transcription and comparison with surrounding issues remain to be done.

## Audit trail

The [machine-readable audit](../sources/02_newspapers/cuervo_clipper/full_scan_audit_2026-09-17.json) records every file's path, date, catalog URL, size, SHA-256, page count, cover-date check, and first-scan text-layer check. Original files were not renamed or modified.
