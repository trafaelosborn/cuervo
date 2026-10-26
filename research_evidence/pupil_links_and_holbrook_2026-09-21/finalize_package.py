"""Build the source register and audit records without changing earlier readings."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def held(path):
    return {"local_file": path, "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}

sources = []
crops = read("research_evidence/pupil_links_and_holbrook_2026-09-21/crop_manifest.json")
for year, sid, url in [
    (1940, "C40", "https://nara-1940-census.s3.us-east-2.amazonaws.com/population-schedules/nm/guadalupe-county/ed/10-6/m-t0627-02445-00652.jpg"),
    (1950, "C50", "https://1950census.archives.gov/search/?county=Guadalupe&ed=10-6&page=1&state=NM"),
]:
    paths = sorted({c["source"] for c in crops if c["id"].startswith(str(year))})
    sources.append({"id": sid, "title": f"{year} U.S. Census, Cuervo precinct/ED 10-6, Guadalupe County, New Mexico", "url": url,
        "evidence_level": "Contemporary manuscript schedule; full sheets and saved detail crops visually inspected",
        "files": [held(p) for p in paths], "locators": "Exact sheet/line references in pupil_linkage_cases.json and the report",
        "limits": "District includes surrounding ranch country; no proof of identical boundaries between censuses, workplace location or continuous residence."})

prior = read("research_evidence/school_and_merchant_2026-09-21/source_index.json")
for i, old_id in enumerate(["S10", "S11", "S12", "S13", "S14"], 1):
    item = next(s for s in prior if s["id"] == old_id)
    sources.append({"id": f"F{i}", "title": item["title"], "url": item["url"], **held(item["local_file"]),
        "evidence_level": "Retrospective public family obituary; original HTML already held", "prior_source_id": old_id,
        "limits": "Family statements are not administrative school or residence records; selected cases cannot establish a migration rate."})

downloads = read("sources/pupil_links_and_holbrook_2026-09-21/download_manifest.json")
for sid, filename, title in [
    ("F6", "john_higgins_sr_2015.html", "John Robert Higgins Sr., obituary, 2015"),
    ("F7", "willa_higgins_2005.html", "Willa D. Higgins, obituary, 2005"),
    ("F8", "john_higgins_jr_2024.html", "John R. Higgins Jr., obituary, 2024"),
]:
    d = next(x for x in downloads if x["local"].endswith(filename))
    sources.append({"id": sid, "title": title, "url": d["url"], **held(d["local"]), "retrieved_utc": d["retrieved_utc"],
        "evidence_level": "Retrospective public family obituary; newly preserved HTML", "limits": "Residence intervals are reported retrospectively; gaps and undated employment must remain explicit."})

sources.extend([
    {"id": "H1", "title": "J. Stuart Holbrook notices on an apparent Albuquerque Tribune A-2 page",
     "url": "https://www.familysearch.org/patron/v2/TH-300-44997-73-40/dist.pdf?ctx=ArtCtxPublic",
     "evidence_level": "Web-extracted PDF text only; newspaper image and printed issue date not verified", "local_file": None,
     "locators": "Two Holbrook items; tool extraction lines 569–584 and 985–1001 (tool-dependent, not printed locators)",
     "working_date": "1965-06-05", "date_status": "inferred", "limits": "No held PDF. Association with a company need not be current employment; spouse conflicts with 1950 wife."},
    {"id": "H2", "title": "NASA, Gemini IV", "url": "https://www.nasa.gov/mission/gemini-iv/", "local_file": None,
     "evidence_level": "Official mission history read online", "use": "June 3, 1965 launch and June 7 landing constrain the newspaper date inference only."},
    {"id": "H3", "title": "PeopleLegacy J. Holbrook burial list", "url": "https://peoplelegacy.com/burial-records/j/holbrook/", "local_file": None,
     "evidence_level": "Secondary search-result pointer; no gravestone image checked", "use": "J. Stuart Holbrook, 1916–1965, Tucumcari Memorial Park; not decisive identity evidence."},
    {"id": "H4", "title": "Tucumcari Memorial Cemetery transcription, part 1", "url": "https://ahgp.org/nm/quay/tucumcarimemorial1.htm", "local_file": None,
     "evidence_level": "Secondary cemetery transcription; rejected identity match", "use": "J. Holbrook Jr. with a March 2, 1949 death is not the 1965 obituary subject."},
    {"id": "A1", "title": "September 16 catalog pull list", **held("research_evidence/archives_catalog_pull_list_2026-09-16.md"),
     "evidence_level": "Project index of previously verified repository catalog references", "limits": "Underlying merchant, school and other archive volumes not held. September 21 bot-check HTML is not fresh catalog evidence."},
    {"id": "A2", "title": "UNM CSWR contact and collections-use guidance", "evidence_level": "Official repository webpages",
     "files": [{"url": d["url"], **held(d["local"]), "retrieved_utc": d["retrieved_utc"]} for d in downloads if "cswr_" in d["local"]],
     "limits": "No visit booked, order placed or fees authorized."},
    {"id": "M1", "title": "NMDOT acknowledgment, IPRA 26-1867-02, September 21, 2026", **held("research_evidence/pupil_links_and_holbrook_2026-09-21/nmdot_receipt_2026-09-21.json"),
     "evidence_level": "Connected Gmail message read; parsed content and metadata preserved, not raw RFC email", "limits": "Status promised by October 1; no historical records supplied."},
])
save("source_index.json", sources)

save("holbrook_audit.json", {
    "date": "2026-09-21", "status": "partly unresolved",
    "primary_1950": {"source": "C50", "sheet": "5", "lines": [9, 10], "household": "1950-5-9", "people": [
        {"id": "1950-5-9", "name_read": "Stuart Holbrook", "age": 33, "occupation_expanded": "general merchandise manager", "class_of_worker": "P"},
        {"id": "1950-5-10", "name_read": "Blanche", "age": 31, "relationship": "wife", "occupation": "store clerk", "class_of_worker": "P"}],
        "sample_answer": "Stuart: same house one year earlier", "employer_named": False, "workplace_located": False},
    "later_notice": {"source": "H1", "name": "J. Stuart Holbrook", "age": 49, "community": "Cuervo", "wife_read": "Selma", "company_association": "Bond-Wiest", "other_activity": "heavy-equipment contracting", "identity": "plausible, not conclusively linked to 1950", "printed_date_verified": False},
    "date_inference": {"working_date": "1965-06-05", "basis": ["Saturday-morning death notice", "Adjacent White/McDivitt flight report approximately 48 hours after launch", "NASA confirms Gemini IV launched June 3, 1965"], "sources": ["H1", "H2"], "limits": "A contextual inference does not substitute for the printed date."},
    "access_log": ["Earlier direct PDF download returned HTTP 403", "Earlier web screenshot could not render the PDF", "September 21 in-app browser showed a blank viewer; no source PDF/image acquired", "Web tool still exposed extracted text; visual issue-date check remains open"],
    "unresolved": ["Printed newspaper date, title and page", "Blanche versus Selma spouse identification", "Dates and nature of Bond-Wiest association", "Whether or where the company operated in 1965"],
    "next_concrete_step": "UNM draft requests the complete apparent Albuquerque Tribune A-2 page around June 5, 1965, plus the listed business volumes and relevant later records.",
    "not_established": ["Bond-Wiest closure date", "Operating Cuervo store in 1965", "Uninterrupted 1950–1965 retail employment"]
})

save("higgins_family_residence_events.json", [
    {"person": "Willa D. Higgins", "date": "1941", "place": "ranch west of Santa Rosa", "kind": "family move", "source": "F7"},
    {"person": "John R. and Willa D. Higgins", "date_start": "1949", "date_end": "1979", "place": "Cuervo", "kind": "reported home interval", "source": "F7", "census_anchor": "1950-8-21 / 1950-8-22"},
    {"person": "John R. and Willa D. Higgins", "date": "1983", "place": "Fort Sumner", "kind": "family home established", "source": "F6", "limit": "F7 says 1980s; residence between 1979 and 1983 not specified"},
    {"person": "Willa D. Higgins", "date": None, "place": "Santa Rosa", "kind": "beauty-shop ownership", "source": "F7", "limit": "Operating years and overlap with Cuervo residence unknown; not itself a home address"},
    {"person": "John R. Higgins Jr.", "date": "1969", "place": "Santa Rosa High School", "kind": "graduation", "source": "F8", "limit": "School location, not a dated residential move"},
    {"person": "John R. Higgins Jr. and family", "date": "2006", "from": "Cuervo", "to": "Santa Rosa", "kind": "reported residential move", "source": "F8", "years_after_graduation": 37, "limit": "Other ranch work mentioned; no proof of uninterrupted Cuervo residence from 1969"}
])

status_path = OUT / "mail_and_draft_status.json"
status = json.loads(status_path.read_text(encoding="utf-8"))
draft_ids = {"state_archives": "r-6046265307816688449", "unm_bond_wiest": "r-5643398373875063561"}
for draft in status["drafts"]:
    draft["draft_id"] = draft_ids[draft["kind"]]
save("mail_and_draft_status.json", status)

canonical = ROOT / "research_evidence/records_requests/06_state_archives_catalog_followup_DRAFT.md"
backup = OUT / "state_archives_local_draft_before_update.md"
if not backup.exists():
    shutil.copyfile(canonical, backup)
shutil.copyfile(OUT / "state_archives_followup_DRAFT.md", canonical)
print(json.dumps({"sources": len(sources), "census_originals": sum(len(s.get("files", [])) for s in sources if s["id"] in ("C40", "C50")), "drafts": "local Archives copy synchronized; no mail tool invoked"}))
