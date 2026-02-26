import spacy
import unicodedata

nlp = spacy.load("en_core_web_trf")

def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def clean_affiliations(raw: str) -> list:
    raw = raw.strip().replace("-", " ")
    results = []
    for aff in [a.strip() for a in raw.split(";") if a.strip()]:
        parts = [p.strip() for p in aff.split(",")]
        if not parts:
            continue
        country = parts[-1]
        doc = nlp(aff)
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        if not orgs:
            results.append(f"{aff} ({country})")
            continue
        selected = orgs[-1].strip()
        if "department" in selected.lower():
            results.append(f"{aff} ({country})")
            continue
        results.append(f"{selected} ({country})")
    return results