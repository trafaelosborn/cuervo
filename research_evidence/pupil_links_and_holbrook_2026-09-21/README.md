# Pupil linkage and Holbrook follow-up

Prepared September 21, 2026. This package extends the earlier school-and-merchant report without replacing its frozen PDF or underlying first-pass census files.

First pass complete: five pupil cases, a separate Holbrook evidence audit, three additional Higgins family accounts and two archive inquiries saved as unsent Gmail drafts. The [report](B:/Meridian/Cuervo/research_evidence/pupil_links_and_holbrook_2026-09-21.md) distinguishes documented readings, retrospective family statements and unresolved links. Holbrook's printed obituary date remains unverified.

Nine full census sheets were inspected before the ten saved detail crops. `candidate_rows_prior_readings.json` preserves the earlier 56 selected readings; it is not the final interpretation. `reading_corrections.json` records two revised names and two explicitly unresolved/retained readings. No age or population statistic was changed.

`prepare_cases.py` reproduces the row selection and crops. `crop_manifest.json` records original paths, SHA-256 checksums and crop coordinates. Source originals remain in the existing census folders.

The 1940 and 1950 Cuervo census material concerns a precinct/enumeration district larger than the built village. A household match does not demonstrate continuous residence, workplace location or school attendance. Five selected family histories cannot supply a migration rate.

## Package contents

- `source_index.json`: seventeen source references, with held-file hashes and access limits.
- `pupil_linkage_cases.json`: five cases with census locators, confidence and contradictory evidence.
- `higgins_family_residence_events.json`: six residence, school and business observations, distinguished by type.
- `holbrook_audit.json`: the 1950 retail entries, later notice, date inference and remaining access/identity gaps.
- `state_archives_followup_DRAFT.md` and `unm_bond_wiest_inquiry_DRAFT.md`: reviewable inquiry bodies. The Archives Gmail draft also retains the prior quoted correspondence.
- `mail_and_draft_status.json`: recipients, Gmail identifiers, read-back verification and the new NMDOT status promise.
- `archives_draft_before_update.json` and `state_archives_local_draft_before_update.md`: preserved earlier draft versions.
- `nmdot_receipt_2026-09-21.json`: preserved parsed message content/metadata, not a raw RFC email export.
- `finalize_package.py`: generates the source register and audit records and synchronizes the local Archives draft. It does not send mail.

Newly acquired original HTML files and their download manifest are under `sources/pupil_links_and_holbrook_2026-09-21/`. Earlier source originals and the prior ten-page PDF remain unchanged. No new PDF was produced in this follow-up.
