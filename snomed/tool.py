def extract_code(term: str) -> str:
    if term is None:
        return "NONE"
    elif len(term) == 0:
        return "NONE"
    elif "|" in term:
        arr = term.split("|")
        return arr[0].strip()
    else:
        return term
