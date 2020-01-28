import numpy as np
from snomed import tool
import spacy
from spacy.pipeline import EntityRuler
import anatomy
import icnp
import medication


def load_anatomy_patterns(nlp, debug=False) -> EntityRuler:

    patterns = anatomy.load_anatomy(debug)
    ruler = EntityRuler(nlp, patterns=patterns, overwrite_ents=True)

    ruler.add_patterns(patterns)
    return ruler


def load_ruler_from_file(nlp,  file="anatomy.jsonl") -> EntityRuler:

    ruler = EntityRuler(nlp, overwrite_ents=True).from_disk(file)
    return ruler


def load_spacy(model="nb_core_news_sm", file="combined.jsonl"):
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

    ruler.add_patterns(patterns)

    nlp.add_pipe(ruler)
    return nlp


if __name__ == "__main__":
    print("Main")
    func = "ALL"
    nlp = spacy.load('nb_core_news_sm')
    if "WRITE" in func:
        ruler = load_anatomy_patterns(nlp)
        ruler.to_disk("anatomy.jsonl")
    elif "LOAD" in func:
        ruler = load_ruler_from_file(nlp)
    elif "ALL":
        ana_patterns = anatomy.load_anatomy()
        icnp_patterns = icnp.load_patterns()
        medication_patterns = medication.create()
        patterns = np.concatenate(
            (ana_patterns, icnp_patterns, medication_patterns))
        ruler = EntityRuler(nlp, patterns=patterns, overwrite_ents=True)
        ruler.to_disk("combined.jsonl")
