# Zenodo metadata formats

The root `.zenodo.json` is the flat GitHub-integration override. `zenodo-deposition.json` wraps exactly the same metadata for the documented legacy deposition API; it is not a native InvenioRDM record object. Merely uploading a JSON file does not import its fields.

The published legacy JSON Schema omits the documented `version` and `language` fields despite rejecting unknown properties. `format-validation.json` therefore distinguishes validation of the other exact fields against that original schema from validation with exactly those two properties added. No remote acceptance or authenticated API write is claimed.

Publication date and a new DOI are deliberately not invented. The existing base DOI is only a prior record. Check actual date, version, rights and destination identifiers before publication. The HTML description is for an HTML/source-capable editor or API field; the CommonMark file is a companion, not an assumption that the API renders raw Markdown.
