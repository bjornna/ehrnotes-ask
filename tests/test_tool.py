from snomed import tool
import snomed


word = "89545001 | Face structure (body structure)"

code = tool.extract_code(word)

print(code)
