# Cuervo's 1940-1950 rebound: research package

Prepared September 19, 2026. The parent-directory Markdown brief and the eight-page PDF in `output/pdf/` are the narrative deliverables.

## Scope

Complete first-pass names and head-listed household grouping for 188 appearances in 1940 and 210 in 1950; selected identity candidates, seven supplementary prior-residence place readings, and five affirmative WWII-service readings. This is not exhaustive person linkage or a complete migration/service census. Preserve the uncertainties in the narrative and JSON when using the data.

## Reproduction

Run with the bundled Python runtime, in this order:

1. `build_households.py`: joins the manual `household_readings.txt` to the September 18 source-row age inventory and applies the two explicit corrections in `age_reading_corrections.json`. Produces `people_name_age_readings.json` and `households.json`.
2. `curate_evidence.py`: writes manually inspected source observations, locators, and linkage cases. It does not automatically read the handwriting or PDF tables.
3. `analyze.py`: validates row coverage and computes `analysis_summary.json` and `households_and_cattle.png`. Uses the local Matplotlib installation under `tmp/deep_dive/python_deps`.
4. `build_pdf.py`: typesets the parent-directory Markdown brief. Uses ReportLab and the existing DejaVu fonts. Follow the PDF skill's artifact marker requirement for a new authoring operation.

## Provenance

- `source_index.json` supplies public URLs and local originals. Exact person source image, sheet, and line are carried in the person file.
- `agriculture_observations.json` has printed page, PDF page, row, period, geography, and unit. The 1940 cattle inventory is **19,227**; a preliminary unpublished reading of 15,227 was rejected after magnification.
- `prior_residence_readings.json` preserves overwritten checkbox problems and leaves the Texas county/place unresolved. The earlier working guess Houston was not accepted.
- `wwii_service_readings.json` reports five observed Yes answers and marks three candidate 1940 identities. These are not five proven Cuervo draftees.
- `household_linkage_examples.json` distinguishes strong candidates, a probable family link, and an unaccepted ambiguous match.
- The USDA download manifest is in `sources/03_census/agriculture_rebound_2026-09-19/`. The downloaded PDFs are 119, 19, and 48 pages.
- Source reading crops are in `tmp/rebound_1940_1950/`. The PDF page renders are in `tmp/pdfs/cuervo_rebound_qa/`.

## Corrections and comparability

1950 Ruth Parker is 38 rather than 58; Henry Yates is 34 rather than 24. The corrected median is 25.5. September 18 data and PDFs are preserved as audit copies, with correction notices in their Markdown reports. Household grouping follows head entries, not building counts. Precinct legal boundary continuity and household-definition comparability are not yet demonstrated. County agricultural statistics do not identify Cuervo's contribution.

The scripts check coverage and arithmetic. They do not independently verify the manual readings; those remain provisional historical transcriptions.
