import numpy as np

import spacy
from spacy.pipeline import EntityRuler
from app.train import anatomy, icnp, medication, icd10


def load_anatomy_patterns(nlp, debug=False) -> EntityRuler:

    patterns = anatomy.load_anatomy(debug)
    ruler = EntityRuler(nlp, patterns=patterns, overwrite_ents=True)

    ruler.add_patterns(patterns)
    return ruler


def load_ruler_from_file(nlp, file="combined.jsonl") -> EntityRuler:
    print(f"Loading EntityRuler with patterns from file={file}")

    ruler = EntityRuler(nlp, overwrite_ents=True).from_disk(file)
    return ruler


def load_spacy(model="nb_core_news_sm", file="combined.jsonl"):
    """Loading a SPACY nlp model and load patterns from the given file (default= combined.jsonl)"""
    print(f"Loading SPACY with model={model} from file={file}")
    nlp = spacy.load(model)
    ruler = load_ruler_from_file(nlp, file)
    patterns = [
        {"label": "LATERALITET", "pattern": "venstre", "id": "SIN"},
        {"label": "LATERALITET", "pattern": "høyre", "id": "DXT"},
        {"label": "SYMPTOM", "pattern": "Smerte", "id": "PAIN"},
        {"label": "OBSERVATION", "pattern": "BP", "id": "BLOOD_PRESSURE"},
        {"label": "OBSERVATION", "pattern": "BT", "id": "BLOOD_PRESSURE"},
        {"label": "OBSERVATION", "pattern": "puls", "id": "PULSE"},
        {"label": "OBSERVATION", "pattern": "Puls", "id": "PULSE"},
        {"label": "OBSERVATION", "pattern": "resp", "id": "RESP"},
        {"label": "OBSERVATION", "pattern": "Resp", "id": "RESP"},
        {"label": "OBSERVATION", "pattern": "temp", "id": "BODY_TEMP"},
        {"label": "OBSERVATION", "pattern": "Temp", "id": "BODY_TEMP"},
        {"label": "OBSERVATION", "pattern": "temperatur", "id": "BODY_TEMP"},
        {"label": "OBSERVATION", "pattern": "Temperatur", "id": "BODY_TEMP"},

        {"label": "LAB", "pattern": "hb", "id": "HB"},
        {"label": "LAB", "pattern": "Hb", "id": "HB"},
        {"label": "LAB", "pattern": "CRP", "id": "CRB"},

        {"label": "UNIT", "pattern": "C", "id": "CEL"},
        {"label": "UNIT", "pattern": "mmHg", "id": "MMHG"}

    ]
    print(f"Loading custom patterns of size={len(patterns)}")
    ruler.add_patterns(patterns)

    nlp.add_pipe(ruler)
    print("Finished loading SPACY")
    return nlp


def load_all_patterns(file="combined.jsonl"):
    """Loading ANATOMY, ICNP, MEDICATION, ICD10 patterns into a combined pattern which is saved in file """

    ana_patterns = anatomy.load_anatomy()
    icnp_patterns = icnp.load_patterns()
    medication_patterns = medication.create()
    icd10_patterns = icd10.create()
    patterns = np.concatenate(
        (ana_patterns, icnp_patterns, medication_patterns, icd10_patterns))
    ruler = EntityRuler(nlp, patterns=patterns, overwrite_ents=True)
    ruler.to_disk(file)


if __name__ == "__main__":
    print("Main")
    timebudget.set_quiet()  # don't show measurements as they happen
    timebudget.report_at_exit()  # Generate report when the program exits
    func = "ALL"
    nlp = spacy.load('nb_core_news_sm')
    if "WRITE" in func:
        ruler = load_anatomy_patterns(nlp)
        ruler.to_disk("anatomy.jsonl")
    elif "LOAD" in func:
        ruler = load_ruler_from_file(nlp)
    elif "ALL":
        load_all_patterns()
