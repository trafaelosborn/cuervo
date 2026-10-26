# Chapters 2 and 3: editorial record

**September 26, 2026 - First complete drafts - Meridian**

## Deliverables

- [Chapter 2: Why a town here?](B:/Meridian/Cuervo/manuscript/chapter-02-why-a-town-here.md)
- [Chapter 3: The business of ranch country](B:/Meridian/Cuervo/manuscript/chapter-03-the-business-of-ranch-country.md)
- [Chapter 2 reading proof](B:/Meridian/Cuervo/output/pdf/cuervo-chapter-02-why-a-town-here.pdf)
- [Chapter 3 reading proof](B:/Meridian/Cuervo/output/pdf/cuervo-chapter-03-the-business-of-ranch-country.pdf)
- [Reproducible proof and figure builder](B:/Meridian/Cuervo/manuscript/build_chapters02_03_pdf.py)

The drafts apply the [Meridian house style](B:/Meridian/Cuervo/manuscript/meridian-house-style.md): institutional voice, accessible sentences, connected argument, economic mechanisms explained before their names, and qualifications proportionate to the claim. They develop the agreed 40,000-60,000-word book architecture. Chapter 1 remains draft 6.

## Division of work

Chapter 2 explains formation. It begins with the Cabra predecessor, follows the relocation and commitments at Cuervo, establishes Santa Rosa's different early functions, and shows how trade and schooling gave people reasons to gather. Its conclusion connects the railway opportunity with the organization that made the location useful. It does not assert an exact town or station founding day.

Chapter 3 explains the merchant economy and subsequent regional change. It distinguishes inventory, sales, credit, cash and profits; develops sheep/wool relationships and freight aggregation; examines financing, management and comparisons within the Bond network; and carries the county agriculture and statewide cattle-price context into the postwar period. North's regional-growth argument supplies the final synthesis. Company, precinct, county and state observations retain their distinct geographic scope.

School staffing, physician support and newspaper finance remain the principal work of Chapter 4. Chapter 2 uses early provision to explain formation, rather than retelling those later cases. Chapter 3 supplies the economic basis for distinguishing a durable merchant from differently supported local services.

## Evidence and interpretation

| Passage or finding | Principal support | Treatment |
|---|---|---|
| Cabra opening, finance, relocation and Cuervo premises | Grubbs, printed pp. 96-102 | Attributed reconstruction; several formation events kept distinct |
| Santa Rosa's early functions | 1902 railway report; 1908 Sanborn sheets | Specific connection, public and commercial functions; no matched-town experiment |
| Actual shipments, supplies, schooling and practitioner entry | Selected checked Clipper pages, 1910-1912 | Dated observations; separate notices not fused into single transactions |
| December 1910 permanent passenger-loss claim | Grubbs compared with December 9, 1910 and January 20, 1911 Clipper reports | Contradiction retained; no invented replacement explanation |
| Early profit recovery and changed investment mix | Grubbs Tables 32-35, manually transcribed | Nominal amounts and accounting categories preserved; his merchandise-dominance generalization qualified |
| Linked credit, livestock and trade | Cuervo account; Rosa exchange; Burguete opinion | Related-firm comparisons and selected litigation identified explicitly |
| Shareholder financing and salary | Grubbs pp. 101-102 | Visually checked; shares, cash contributions and earnings distribution distinguished |
| County livestock and operating scale | Seven agricultural-census observations, 1930-1959 | Separate commodities; changing dates, coverage and farm definitions retained |
| Labor and trucks | 1959 agriculture Table 6, including retrospective 1954 | Different seasonal labor weeks; no annual job-loss calculation or claimed rise in mechanization |
| Cattle-price cycle and population rebound | Held USDA series, prior BLS reading and precinct counts | Economic context; no correlation promoted to a causal result |
| Export activity and local diversification | North (1959); Smith; selected Braverman-Stiglitz reading | Mechanisms applied to the historical case; no estimated multiplier or universal threshold |

No new historical sources were acquired. The drafting pass revisited prior checked readings and structured transcriptions, the selected Grubbs chapter OCR, held North and Smith texts, and relevant passages of the preserved court opinion. Grubbs printed pp. 101, 102 and 107 were visually rechecked for newly developed construction, shareholder-finance and pricing passages. The first Sanborn sheet was revisited visually. This is not a new full reading of every held volume or of the original merchant manuscripts.

## Design and figures

The proofs continue Chapter 1's page size, generous margins, readable Garamond body, navy italic headings and restrained running furniture. Chapter openings use typographic title pages and dated source-based observations. These are reading proofs, not a finalized image sequence for the whole book.

Chapter 2 includes the full first sheet of the December 1908 Santa Rosa Sanborn map, with provenance and a warning about displaced insets. Chapter 3 includes two new figures generated from the checked JSON transcriptions: separate panels for merchant balances and annual net profit, and discrete markers for the seven county livestock observations. The latter has no interpolated annual line. The chart PNGs and editable SVGs are retained in [the figure folder](B:/Meridian/Cuervo/manuscript/figures/chapters02-03), with a source manifest.

The builder uses the bundled Python and ReportLab. Matplotlib was installed into the project's temporary dependency folder because it was absent from the bundled runtime; the script uses that folder explicitly. No global Python installation was changed.

## Review

Structural, reference and visual checks are recorded in `tmp/pdfs/chapters02-03-draft01/`.

| Draft | Main-text words | PDF pages | Notes | Note references |
|---|---:|---:|---:|---:|
| Chapter 2 | 5,010 | 20 | 23 | 33 |
| Chapter 3 | 6,502 | 27 | 28 | 42 |
| Combined | 11,512 | 47 | 51 | 75 |

All 75 note references resolve to valid destinations in the PDFs. Note definitions follow first appearance, and the manuscript source links point to existing local files. Mechanical checks found no replacement glyphs or unfinished placeholders; PDF metadata, running headings and rendered page counts passed.

All 47 pages were reviewed in overview sheets. The final covers, opening prose, manager passage, map, both charts and a representative notes page were also inspected at full size. Review corrected title-page letter spacing, the finance chart's axis limits and a short page preceding the map. The final proofs have no observed clipping, overlapping text or stranded section headings. They remain reading proofs for editorial review, rather than publication-final layouts.

## Remaining editorial work

The requested chapters are complete drafts. The next useful review concerns pacing, the balance between concrete business history and explanation, and continuity across Chapters 1-3. No additional archive acquisition is a prerequisite for that review. A final book-wide source and image review remains part of publication preparation, rather than a reason to delay these drafts.
