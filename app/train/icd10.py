import spacy
from spacy.pipeline import EntityRuler
import xlrd
PATH_HEALTHONTOLOGIES = "../healthontologies"
PATH_ICNP = "icd10/ICD-10-2020-Norsk.xlsx"


def load_icd10(debug=False):
    excel_file = PATH_HEALTHONTOLOGIES + "/" + PATH_ICNP
    loc = (excel_file)
    wb = xlrd.open_workbook(loc, encoding_override="utf-8")
    sheet = wb.sheet_by_index(1)

    print(sheet.nrows)
    terms = []
    rows_to_rad = sheet.nrows

    for i in range(2, rows_to_rad):
        code = sheet.cell_value(i, 0)
        term_text = sheet.cell_value(i, 1)
        term_long_text = sheet.cell_value(i, 2)
        res = (code, term_text, term_long_text)
        terms.append(res)

    return terms


def create_patterns(terms):
    patterns = []
    for term in terms:
        code = term[0]
        term_text = f"{term[1]}"
        term_patterns = []
        for word in term_text.lower().split():
            n_pat = {"LOWER": word}
            term_patterns.append(n_pat)
        pat = {"label": "ICD10", "pattern": term_patterns, "id": code}
        patterns.append(pat)
    return patterns


def create(debug=False):
    return create_patterns(load_icd10())


def create_nlp_pattern(nlp, patterns):
    ruler = EntityRuler(nlp, patterns=patterns, overwrite_ents=True)
    return ruler


if __name__ == "__main__":
    result = load_icd10()
    patterns = create_patterns(result)
    nlp = spacy.load('nb_core_news_sm')
    ruler = create_nlp_pattern(nlp, patterns)
    ruler.to_disk("icd10.jsonl")
