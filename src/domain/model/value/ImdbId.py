import re

class ImdbId:
    _pattern = re.compile(r"^tt\d+$")

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("ImdbId must be a string")
        if not self._pattern.match(value):
            raise ValueError(f"ImdbId must match 'tt<digits>', got {value!r}")
        self.value = value

    def __eq__(self, other):
        return isinstance(other, ImdbId) and self.value == other.value

    def __repr__(self):
        return f"ImdbId({self.value!r})"
