"""Retrieve public railway reference material and retain provenance."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sources/01_railroad/local_functions_2026-09-20"
OUT.mkdir(parents=True, exist_ok=True)
TARGETS = [
    ("utep_division_engineer_1.pdf", "https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=1000&context=finding_aid&filename=1&type=additional"),
    ("utep_division_engineer_2.pdf", "https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=1000&context=finding_aid&filename=2&type=additional"),
    ("utep_freight_agent.pdf", "https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=1000&context=finding_aid&filename=4&type=additional"),
    ("utep_common_contract_carrier_nmcc.pdf", "https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=1000&context=finding_aid&filename=10&type=additional"),
    ("utep_misc_correspondence.pdf", "https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=1000&context=finding_aid&filename=12&type=additional"),
    ("utep_land_tax.pdf", "https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=1000&context=finding_aid&filename=15&type=additional"),
    ("utep_files_of_importance.pdf", "https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=1000&context=finding_aid&filename=21&type=additional"),
    ("nmarchives_corporation_search.html", "https://nmarchives.unm.edu/search?q%5B%5D=Corporation%20Commission&op%5B%5D=&field%5B%5D=keyword"),
    ("nmarchives_cuervo_search.html", "https://nmarchives.unm.edu/search?q%5B%5D=Cuervo&op%5B%5D=&field%5B%5D=keyword"),
]

def fetch(target):
    name, url = target
    path = OUT / name
    item = {"file": str(path.relative_to(ROOT)), "url": url}
    try:
        if path.exists():
            data = path.read_bytes()
            item["cached"] = True
        else:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=25) as response:
                data = response.read()
                item["resolved_url"] = response.url
                item["content_type"] = response.headers.get("Content-Type")
            if name.endswith(".pdf") and not data.startswith(b"%PDF"):
                raise ValueError("Response is not a PDF")
            path.write_bytes(data)
        item.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), retrieved_utc=datetime.now(timezone.utc).isoformat())
        if name.endswith(".pdf"):
            from pypdf import PdfReader
            reader = PdfReader(path)
            item["pages"] = len(reader.pages)
            texts = [page.extract_text() or "" for page in reader.pages]
            path.with_suffix(".txt").write_text("\n".join(f"\n=== PDF PAGE {i+1} ===\n{t}" for i, t in enumerate(texts)), encoding="utf-8")
            item["cuervo_hits"] = []
            for i, t in enumerate(texts):
                lines = t.splitlines()
                for j, line in enumerate(lines):
                    if "cuervo" in line.lower():
                        item["cuervo_hits"].append({"pdf_page": i+1, "context": "\n".join(lines[max(0,j-4):j+5])})
    except Exception as e:
        item["error"] = str(e)
    print(json.dumps(item, ensure_ascii=True), flush=True)
    return item

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, TARGETS))
    (OUT / "manifest.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
