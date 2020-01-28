
import spacy
from spacy.pipeline import EntityRuler


def create():
    words = ["Simvastatin", "Laktulose", "Paracet",
             "Bactrim", "cloxacillin", "Gentamycin", "Afipran"]
    patterns = []
    for w in words:
        term = w.lower()
        n_pat = {"LOWER": term}
        pat = {"label": "MEDICATION", "pattern": [n_pat], "id": term}
        patterns.append(pat)
    return patterns


def create_nlp_pattern(nlp):
    patterns = create()
    ruler = EntityRuler(nlp, patterns=patterns, overwrite_ents=True)
    return ruler


if __name__ == "__main__":
    nlp = spacy.load('nb_core_news_sm')
    ruler = create_nlp_pattern(nlp)
    ruler.to_disk("medication.jsonl")
