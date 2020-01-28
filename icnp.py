import spacy
from spacy.pipeline import EntityRuler
import xlrd
PATH_HEALTHONTOLOGIES = "../healthontologies"
PATH_ICNP = "icnp/icnp_no_out.xlsx"


def load_icnp(axis_filter="F", debug=False):
    excel_file = PATH_HEALTHONTOLOGIES + "/" + PATH_ICNP
    loc = (excel_file)
    wb = xlrd.open_workbook(loc, encoding_override="utf-8")

    sheet = wb.sheet_by_index(0)
    print(sheet.nrows)
    terms = []

    for i in range(1, sheet.nrows):
        code = sheet.cell_value(i, 1)
        axis = sheet.cell_value(i, 2)
        term = sheet.cell_value(i, 3)
        term_text = "{}".format(term).lower().split()
        if axis in axis_filter:
            res = (code, axis, term_text)
            terms.append(res)

    return terms


def create_pattern(terms):
    patterns = []
    for term in terms:
        code = term[0]
        axis = "ICNP_" + term[1]
        wors = term[2]
        word_pattern = []
        for word in wors:
            n_pat = {"LOWER": word}
            word_pattern.append(n_pat)

        pat = {"label": axis, "pattern": word_pattern, "id": code}
        patterns.append(pat)
    return patterns


def create_nlp_pattern(nlp, patterns):
    ruler = EntityRuler(nlp, patterns=patterns, overwrite_ents=True)
    return ruler


def load_patterns():
    terms = load_icnp(axis_filter="F", debug=False)
    # print(terms)
    patterns = create_pattern(terms)
    return patterns


if __name__ == "__main__":
    terms = load_icnp(axis_filter="F", debug=False)
    # print(terms)
    patterns = create_pattern(terms)
    nlp = spacy.load('nb_core_news_sm')
    ruler = create_nlp_pattern(nlp, patterns)
    ruler.to_disk("icnp_f.jsonl")
