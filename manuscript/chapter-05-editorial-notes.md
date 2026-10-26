# Chapter 5: editorial and evidence record

**September 28, 2026. Draft 1 complete; illustrated reading proof checked.**

## Delivered

- [Editable chapter](chapter-05-people-across-places.md): **5,555 main-text words**, excluding headings, figure directives and notes.
- [Reading proof](../output/pdf/cuervo-chapter-05-people-across-places.pdf): **27 pages**, three statistical figures, one census plate, 24 source notes and 32 resolving internal note links.
- Chapters 1-5 now total **26,221 main-text words, 113 notes, 16 visual positions and 119 separately paginated reading-proof pages**. The chapter notes contain 152 resolving internal references across the five proofs. This is not yet a combined or print-ready book.

## Argument and scope

Chapter 4 examined the work involved in maintaining services. Chapter 5 separates changes in those services from changes in the population and its residential arrangements. It opens with John Higgins Jr.'s reported 1969 graduation and 2006 move, explicitly distinguishing the two dates from a claim of continuous residence.

The chapter develops:

1. The population inside the Cuervo precinct label, including rural territory and early redistricting.
2. Contraction without steady prewar aging, using all five census age inventories and corrected 1950 readings.
3. The 1940-1950 increase through more, smaller household groups, cohort accounting, selected family changes and recent arrivals.
4. Occupations at the level of people and households, including women's proprietorship, paid employment and unpaid family work.
5. School, work and home as distinct histories in the Higgins, Bailey and Vigil accounts.
6. Santa Rosa's household persistence and institutional population alongside Los Lunas's much larger household-population expansion.
7. Why later block counts cannot be appended to the old precinct series as if the geography had stayed fixed.

The handoff to Chapter 6 concerns the journeys and transport arrangements that made residence, work and service use across places practical. No complete family migration reconstruction, causal allocation of wartime changes or universal population threshold is required or claimed.

## Evidence work

This chapter uses held sources and prior checked readings. No new historical acquisition was made. The [source-review record](../research_evidence/chapter05_2026-09-28/source-review.md) distinguishes targeted rereading from reused transcriptions.

The figure builder recomputes population, unread-age bounds and medians from the person records. It substitutes the corrected September 19 data for 1940/1950, retaining the earlier files unchanged. Named-row counts reproduce 545, 438, 287, 188 and 210; total appearances 1,668; unresolved ages seven; corrected 1950 median 25.5. Household group counts and size distributions are recomputed from member groups. Regional household-plus-group-quarters totals are checked at all five plotted dates for both municipalities. [Calculation record](../research_evidence/chapter05_2026-09-28/calculations.json).

The descriptive calculations do not resolve geographic changes, all handwriting uncertainty, enumeration error or disclosure protection. Counts of occupation appearances are not employment rates or workplace job totals. Selected family accounts are illustrative evidence, not a representative migration sample.

## Visual sequence

| Figure | Proof page | Evidence | Treatment |
|---|---:|---|---|
| 5.1 A smaller, still young population | 5 | Cuervo precinct counts and manually read ages, 1910-1950 | Discrete populations and age points/ranges in separate panels; unread-age bounds are not confidence intervals |
| 5.2 More people, smaller groups | 8 | 1940/1950 people and head-listed household groups | Separate population bars and stacked group counts; no inference of new houses |
| 5.3 Several livelihoods, one household | 15 | Higgins and Santa Rosa railway/cafe household rows, 1950 | Names/relationships and work columns in paired excerpts; omitted columns explicitly identified |
| 5.4 Growth has different components | 21 | Santa Rosa and Los Lunas, 1980-2020 | Santa Rosa household/group-quarters composition above; household-population comparison below |

Generated charts are retained as PNG and editable SVG. The [asset manifest](figures/chapter05/sources.json) records input hashes, source files and crop coordinates. Historical source excerpts were cropped without retouching; their original writing and marks remain visible.

## Verification

- All 27 final rendered pages reviewed in contact sheets. Figures on pages 5, 8, 15 and 21 inspected at full rendered-page size; census details also reviewed at larger source size.
- Two figure placements revised to improve the prose flow and remove a short spill page. Final headings, labels, captions, notes and folios are unclipped, with no accidental blank pages.
- All 32 internal note references resolve to 24 distinct destinations; notes follow first-appearance order. Every local source link exists.
- PDF metadata names Meridian. No replacement characters, black-square glyphs or leftover placeholders found in extracted text.
- Sentence diagnostic: mean 12.8 words, longest 28 under the simple punctuation split. This is an editing aid, not a formal readability score.
- Builders: `build_chapter05_assets.py` and `build_chapter05_pdf.py`; mechanical and rendered-page checks: `check_chapter05.py`.
- Final PDF SHA-256: `61bf79b3cb32440da56eb67e700f44033cfd971aa61f3c5b81d7eb774fe9ed05`.

The chapter remains a documented first draft. Independent demographic transcription review, cross-chapter editing, scholarly critique and final book production are later stages. The next writing task is Chapter 6, *Changing the connections*.
