# Cuervo Revision 7: completed editorial and design pass

September 29, 2026. Revision 6 is preserved unchanged.

## Result

The reading proof contains 147 pages, 20,732 main-text words, 169 source notes, 211 note calls, 18 author photographs and 40 visual positions. The main text is 258 words shorter than Revision 6. This is a focused finishing pass; the substantial compression belongs to earlier revisions.

## Editorial changes

- Consolidated repeated explanations of merchant credit, joint shipments, farm counts, visiting care and railway administration.
- Simplified the discussion of staffing and maintenance. Kept the distinction between a proposed replacement and confirmed resumption of instruction.
- Moved narrow limits about newspaper coverage and garage operations into the relevant notes, while retaining qualifications needed to understand the argument.
- Recast Chapter 7's conclusion to state the interpretation first: locally concentrated trade and services contracted within a continuing regional economy. The following paragraph distinguishes documented changes from possible feedback and reopening costs.
- Retained the compact AC and Los Lunas discussions, all source-note identities and all note calls.
- Replaced Figure 5.1's misleading title with “Fewer residents, still young.” The population and age observations remain unchanged.

The paragraph-level record is in `editorial-changes.json`; the reproducible edit script is `manuscript/edit_book_revision07.py`.

## Typography and page design

The proof uses Playfair Display Bold for chapter titles and major headings, and Playfair Display Regular for subheads. Futura was unavailable on this computer. Jost Regular is an explicitly labeled provisional geometric-sans stand-in, set at 11.3 points with 16.2-point line spacing. This does not establish how the exact Futura version will paginate or read.

The two-page typography comparison sets the same passage with Jost and the earlier Garamond face, retaining the same Playfair hierarchy. Playfair provides a clear distinction between major headings and subheads. The geometric body treatment is legible in the inspected screen proof; sustained reading and a physical proof should determine the final body choice.

Notes use a wider measure. Illustration placement and page transitions were adjusted to resolve isolated fragments, a detached caption and an unwanted blank page introduced during reflow. Some chapter endings and note endings intentionally leave generous white space.

All 18 photographs retain their full frames and aspect ratios. Reproduction copies are capped at 300 dpi at placed size; photographs use high-quality JPEG encoding, and documentary plates remain PNG. Originals are unchanged. Photographic color treatment, paper and binding remain publication-design decisions.

Font sources and licenses are retained under `manuscript/fonts/revision07/`: [Playfair Display](https://github.com/google/fonts/tree/main/ofl/playfairdisplay) and [Jost](https://github.com/google/fonts/tree/main/ofl/jost).

## Verification completed

- Revision 6: all 150 pages rendered and inspected in overviews, supplementing the preceding 32-page detail review. Findings are recorded in `output/editorial/cuervo-revision-06-complete-visual-review.md`.
- Revision 7: all 147 final pages rendered and inspected in 13 overviews. Eighteen final pages also inspected at larger scale: 1, 2, 3, 8, 31, 53, 58, 63, 75, 83, 107, 118, 121, 127, 139, 142, 146 and 147.
- No apparent overlapping text, clipped page content, missing images or detached captions in the inspected final proof. Chart and source-plate relationships remain coherent after reflow.
- All main text and all notes transferred from the revised source. All 211 source-note links resolve to 169 distinct destinations; 20 contents links, 16 photograph-concordance links and 10 bookmarks pass checks.
- Page-edge checks pass. Embedded text uses Jost and Playfair; legacy Garamond and Calibri no longer appear in explanatory tables or source-plate text. Typography within original scans and raster chart labels is retained.
- Original Revision 6 chapter and PDF hashes match. Earlier Revision 5 checks also pass.
- Both companion PDFs have two pages and received visual review.

This is screen-layout and document-integrity verification, not an independent scholarly review, an audit of every historical source or a physical press proof. The checked PDF hash and review scope are recorded in `visual-review.json`.

## Outside review and remaining publication work

The outside-reader brief asks readers to test the interpretation, economic mechanisms, historical method, comparisons, visuals and accessibility. It requests specific claims and reasons for any essential new research. The brief is prepared; no outside reader has been contacted in this pass.

The next publication tasks are outside critique, an index, the final cover and print production. Actual Futura can be substituted once the font is available, followed by another pagination and layout check.
