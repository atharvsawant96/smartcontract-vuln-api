import re
def clean_code(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r"//.*?$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"/\*[\s\S]*?\*/", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
