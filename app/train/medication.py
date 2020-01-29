
import spacy
from spacy.pipeline import EntityRuler
PATH_HEALTHONTOLOGIES = "../healthontologies"
PATH_ICNP = "medication/medications.txt"


def create(debug=False):

    medication_list_file = PATH_HEALTHONTOLOGIES + "/" + PATH_ICNP
    print(f"Loading medication terms from {medication_list_file}")
    f = open(medication_list_file, mode="r", encoding="utf-8")
    words = []
    for line in f:
        words.append(line.lower().strip())

    patterns = []
    for w in words:

        term = w.lower().strip()
        n_pat = {"LOWER": term}
        pat = {"label": "MEDICATION", "pattern": [n_pat], "id": term}
        patterns.append(pat)
    return patterns


def create_nlp_pattern(nlp):
    patterns = create()
    print(f"Creating medication patterns from n={len(patterns)} terms")
    ruler = EntityRuler(nlp, patterns=patterns, overwrite_ents=True)
    return ruler


if __name__ == "__main__":
    nlp = spacy.load('nb_core_news_sm')
    ruler = create_nlp_pattern(nlp)
    ruler.to_disk("medication.jsonl")
