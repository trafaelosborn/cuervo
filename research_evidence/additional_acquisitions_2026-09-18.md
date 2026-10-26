# Additional records acquired, September 18, 2026

**158 files acquired and format-validated:** 155 distinct source files, two repository OCR companions, and one duplicate census-map copy. Catalog metadata and our reading/rendering files are excluded from this count. Total source/access-file size is approximately 1.09 GB (decimal).

The most substantial addition is **the original 1940 household census for Cuervo and comparison communities**. Two business-directory volumes also provide dated lists of Cuervo's enterprises before Route 66.

- [Every file, with local and repository links](additional_acquisitions_file_index_2026-09-18.md)
- [Download manifest: URLs, sizes, SHA-256 checksums, validation](../sources/_logs/round3_2026-09-18/download_manifest.json)
- [Acquisition script](../sources/pull_public_sources_2026_09_18.py)

## 1. The 1940 household census: 120 schedule images

Downloaded every schedule image listed in NARA's state metadata for these nine enumeration districts (EDs). Image counts include blank sheet reverses and other retained images; they are not population or household counts.

| ED | Coverage in the official descriptions | Images | Local folder |
|---|---|---:|---|
| 10-6 | Cuervo election precinct 6, including Cuervo | 6 | [Cuervo](../sources/03_census/1940_manuscripts/ed_10-6/) |
| 10-7 | Newkirk election precinct 7, including Newkirk | 8 | [Newkirk](../sources/03_census/1940_manuscripts/ed_10-7/) |
| 10-8 | Santa Rosa village, including Guadalupe County Jail | 62 | [Santa Rosa](../sources/03_census/1940_manuscripts/ed_10-8/) |
| 10-9 | Santa Rosa precinct outside the village | 8 | [Santa Rosa surroundings](../sources/03_census/1940_manuscripts/ed_10-9/) |
| 19-18 | Montoya election precinct 13, Quay County | 4 | [Montoya](../sources/03_census/1940_manuscripts/ed_19-18/) |
| 31-1 | Los Lunas village, including Valencia County Jail | 16 | [Los Lunas village](../sources/03_census/1940_manuscripts/ed_31-1/) |
| 31-2 | State residential institution in Los Lunas precinct | 4 | [Institution, separate ED](../sources/03_census/1940_manuscripts/ed_31-2/) |
| 31-3 | Los Lunas precinct outside the village, excluding Isleta Purchase | 10 | [Los Lunas surroundings](../sources/03_census/1940_manuscripts/ed_31-3/) |
| 31-4 | Los Lunas precinct within Isleta Purchase | 2 | [Separate precinct portion](../sources/03_census/1940_manuscripts/ed_31-4/) |
| **Total** | | **120** | |

The schedules contain age, sex, household relationships, employment, occupation/industry, and residence on April 1, 1935. They create a way to test the proposed prewar age difference and examine migration before 1940. They do not themselves identify later wartime enlistments or military absences. Reading the 1935 residence fields requires the enumerator instructions, including treatment of young children and entries such as "same house," "same place," and rural residence.

**Inspection so far:** all six Cuervo images viewed at overview scale, with the first sheet's header checked more closely; selected Santa Rosa, Montoya, and Los Lunas headers checked against the metadata. Cuervo's first sheet contains WPA and CCC work entries. This is a useful lead about Depression-era employment, not an occupation total. A systematic person-level transcription and age comparison has not been performed. No population series has been revised on the basis of this intake.

Cuervo ED 10-6 is a precinct. Los Lunas's village, surrounding territory, and institutional ED remain separate. Do not combine them into a town total or assume each ED has comparable territory across years.

Source: [NARA's 1940 census public dataset](https://registry.opendata.aws/nara-1940-census/), managed by NARA, with anonymous public downloads. [Official New Mexico metadata](https://nara-1940-census.s3.us-east-2.amazonaws.com/metadata/json/nm.json) and [selected district metadata](../sources/_logs/round3_2026-09-18/nara1940_selected_districts.json) are preserved locally.

## 2. Census geography: 23 map images and three description images

Downloaded the map images listed for Guadalupe County (6), Quay County (6), and Valencia County (11), plus the three distinct description images associated with the selected districts. These are scans, not necessarily 23 distinct map sheets. [Geography folder](../sources/03_census/1940_manuscripts/geography/).

The Guadalupe [description image](../sources/03_census/1940_manuscripts/geography/m-t1224-00105-01710.jpg) explicitly identifies precinct 6 and instructs the enumerator to show unincorporated Cuervo separately. Its handwritten 1940 total beside the precinct is **188**; Santa Rosa village is **2,310**, with **217** outside the village. These annotations support the geography of our published-table readings. They do not resolve the separate 128 figure attributed to Cuervo in later accounts.

A Wikimedia copy of NARA map 5835368 was acquired first. Its SHA-256 matches the subsequent official NARA download `m-a3378-00039-00911.jpg` exactly. It is retained for provenance and counted as a duplicate, not additional historical evidence. Map boundaries and base-map dates still need systematic comparison with the 1950 geography.

## 3. Business directories for 1920 and 1921

Both **Part 1 volumes** are downloaded in full, together with the Internet Archive's OCR XML. Part 2 volumes are not included in this acquisition.

| Volume | Local original PDF | Cuervo entry |
|---|---|---|
| 1920, 814 PDF pages | [1920 directory](../sources/11_business_directories/newmexicostatebu01unse_0.pdf) | Printed **190**, PDF **305** |
| 1921, 780 PDF pages | [1921 directory](../sources/11_business_directories/newmexicostatebu01unse.pdf) | Printed **186-187**, PDF **289 and 291**; PDF 290 is a blank reverse |

Repository records: [1920](https://archive.org/details/newmexicostatebu01unse_0), [1921](https://archive.org/details/newmexicostatebu01unse). The printed state-directory headings also identify the years (PDF 47 in the 1920 volume; PDF 45 in 1921). The publisher is Gazetteer Publishing Co., Denver.

### Visually checked Cuervo entries

- **1920:** Armijo Mercantile; Bond & Wiest; Golden Rule Garage; Oklahoma Hotel; Rock Island Hotel; Landers & Sanford; S. J. T. Pepper & Co.; other merchants, livestock operators and service providers. It lists Anna Faircloth as school principal, W. E. Bennett as postmaster, W. A. Craig as railroad/express/telegraph agent, and J. H. Easley with a stage and mail line to Lucille.
- **1921:** the entry still lists both hotels and Bond & Wiest, among other enterprises. It also lists Romero Dome Oil Co.; a directory listing does not establish oil production. Lillian Verell is listed as the Clipper's editor/manager, compared with W. J. Ferguson in 1920. The Rock Island Hotel proprietor is J. L. Foster, compared with Mrs. L. C. Bailey in 1920.

These supply dated business observations to match against Clipper advertisements and the merchant archives. They are not exact opening/closure dates. Do not count a proprietor's entry and a separately listed business as two establishments. An omitted business is not automatically closed.

Both entries give a **"population of neighborhood" of 350**. That is a directory figure with different provenance and geography, not a replacement for the census precinct totals. The whole volumes have not been read; the above statements concern the complete Cuervo entries.

## 4. Church documents and a restoration lead

- [2018 Archdiocese parish directory](../sources/10_church_history/archdiocese_santa_fe_parishes_2018.pdf): printed **99**, PDF **85**, lists Santo Niño, Cuervo, among St. Rose of Lima's Santa Rosa missions. Attendance totals on that page are parish-level figures, not Cuervo-specific attendance.
- [December 21, 2025 parish bulletin](../sources/10_church_history/st_rose_bulletin_2025-12-21.pdf): PDF **2**, in the collection report labeled **12/6-12/7**, records **"Cuervo Function 170.00"**. PDF **3** lists Santo Niño/Cuervo among the parish missions. This is a dated parish financial entry; it does not identify the event's location, attendance, or service frequency.
- [Dorothy Chavez's 2017 funeral-home notice](https://www.chavezfuneralhome.com/obituaries/4151483), [local HTML](../sources/10_church_history/dorothy_chavez_obituary_2017.html): names her involvement in Santo Nino Church Restoration and announces a March 9, 2017 funeral Mass at the church, officiated by Father Sotero Sena. This gives a named restoration participant and another dated service announcement. It is a family memorial, not a parish administrative record.

**Additional lead, book not acquired:** Daniel B. Flores, *Cuentos del Cuervo: Tales of a Guadalupe County Village*, ISBN 9781503069275, 144 pages, cataloged as November 2014. A [retail catalog description](https://business.walmart.com/ip/Cuentos-Del-Cuervo-Tales-of-a-Guadalupe-County-Village-9781503069275/685707541) describes monthly Sunday services and church restoration. A present-day catalog blurb does not establish when that description was written or the dates of the practice. The actual book and its sources need checking.

The date and reason for a reduction or end of regular priest visits remain unresolved. None of these records independently verifies the explanation Taylor heard. See the [field-account note](cuervo_church_field_lead_2026-09-18.md).

## 5. Los Lunas: municipal transportation history

[2035 Master Transportation Plan, adopted October 10, 2013](../sources/08_context/los_lunas_master_transportation_plan_2035_adopted_2013.pdf), 71 PDF pages. **Printed 12, PDF 18** explicitly relates the village's development as a bedroom community to Albuquerque employment growth, relatively affordable housing, rural character, and the commute enabled by I-25.

This is a municipal retrospective that identifies the mechanism we want to compare with Santa Rosa/Cuervo. It does not estimate a universal city-size threshold or establish why Cuervo failed to develop the same residential role. [Municipal source](https://www.loslunasnm.gov/DocumentCenter/View/14449/Los-Lunas-Master-Transportation-Plan-2035---Adopted-10102013-PDF?bidId=).

## 6. Wartime livestock context

- [USDA, *The Livestock and Wool Situation*, June 1945, LWS-38](../sources/08_context/usda_livestock_wool_1945-06.pdf), 26 PDF pages. **Printed/PDF 16-17** discuss government purchases, military demand, and exports; Table 4 distinguishes beef/veal, sheep meat, pork, and all meat. The 6.8-billion-pound wartime export figure is **all meat**, not beef. The page 16 footnote excludes shipments to U.S. armed forces abroad from the export measure. **Locator correction:** the relevant discussion is page 16, not page 26.
- [USDA, *Livestock Slaughter - Meat and Lard Production, 1940-1946*, May 1947](../sources/08_context/usda_livestock_slaughter_1940-1946_1947-05.pdf), two pages. Gives national slaughter and production estimates across the war and early postwar period.

These are national context. Neither records Cuervo's shipments, destinations, railroad tonnage, or local employment effects. The newly acquired 1940 household schedules are the stronger immediate source for testing the age-composition part of the wartime hypothesis.

## 7. An earlier postal connection

[Senate Document 460, *Discontinuance of Star Routes*, 1914](../sources/05_postal/us_post_office_star_routes_curtailed_1914.pdf), 70 pages. Printed/PDF **33**, New Mexico table, records route **67404, Hanson-Cuervo**, 7.5 miles, three round trips weekly, annual cost $160. The recorded discontinuance took effect **July 15, 1913**, because Hanson had no suitable postmaster candidate.

This documents a feeder mail connection and a stated reason for its loss. It is not the closure of Cuervo's post office and does not establish Cuervo's 1902 opening date. [Official government scan](https://www.govinfo.gov/content/pkg/SERIALSET-06597_00_00-152-0460-0000/pdf/SERIALSET-06597_00_00-152-0460-0000.pdf).

## Validation and remaining gaps

All 155 distinct source files, both OCR companions, and the duplicate map passed file-format checks. All acquired PDFs parse; image files pass Pillow verification. Checksums are recorded for every file. Relevant directory, parish, postal, Los Lunas, and USDA pages were rendered and inspected. This is a validation of acquisition and selected readings, not an exhaustive transcription or a guarantee that repository scans contain every original page.

The 1912-1913 Polk directory catalog was located but its direct request returned HTTP 403; no scan was acquired from it. Two other discovery-page requests failed, without preventing the acquisitions above. The metadata log retains those outcomes.

Still missing: 1910-1930 household schedules, historical aerials, the town-company and merchant books, local school records, actual highway project/land files, and the administrative history of regular Mass. Existing request statuses have not been rechecked against the inbox. No emails or new archive requests were sent during this acquisition.
