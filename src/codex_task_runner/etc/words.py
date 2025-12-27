import re


def words(text: str) -> list[str]:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return [w for w in s.split() if w]
