import xlrd
import snomed.tool
PATH_HEALTHONTOLOGIES = "../healthontologies"
PATH_SNOMED_EXCEL = "snomed/volven-8352-snomed.xlsx"


def enric_word(word: str) -> []:
    res = []
    res.append(word)
    suffixes = ["er", "en", "ene", "et", "t", "n"]
    for suf in suffixes:
        res.append(f"{word}{suf}")
    if word.endswith("e"):
        n = word[0: len(word) - 1]
        res.append(n + "nene")

    return res


def load_anatomy(debug=False):

    excel_file = PATH_HEALTHONTOLOGIES + "/" + PATH_SNOMED_EXCEL

    loc = (excel_file)
    # To open Workbook
    wb = xlrd.open_workbook(loc, encoding_override="utf-8")
    #sheet = wb.sheet_by_index(0)
    sheet = wb.sheet_by_name("Anatomisk lokalisasjon")

    # For row 0 and column 0
    sheet.cell_value(0, 0)

    # print(sheet.nrows)

    # for i in range(sheet.ncols):
    # print(sheet.cell_value(0, i))

    terms = []
    LABEL = "ANATOMY"
    for i in range(sheet.nrows):
        term_name = sheet.cell_value(i, 3)
        term_code = sheet.cell_value(i, 5)
        term_name_str = f"{term_name}".lower()
        code = snomed.tool.extract_code(term_code)
        term = (LABEL, term_name_str, code)
        terms.append(term)

    # print(terms)
    patterns = []

    for term in terms:
        words = enric_word(term[1])
        id = term[2]
        if "81745001" in id:
            print(term)

        for w in words:
            word_patterns = [{"LOWER": w}]
            pat = {"label": term[0], "pattern": word_patterns, "id": term[2]}
            #pat = {"label": term[0], "pattern": term[1], "id": term[2]}
            patterns.append(pat)
    patterns.append({"label": LABEL, "pattern": "Albuen", "id": "127949000"})
    if debug:
        print(patterns[:10])
    return patterns
