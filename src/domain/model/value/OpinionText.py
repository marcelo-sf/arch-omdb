class OpinionText:
    MAX_LENGTH = 1000

    def __init__(self, text: str):
        if not isinstance(text, str):
            raise ValueError("OpinionText must be a string")
        txt = text.strip()
        if not txt:
            raise ValueError("OpinionText cannot be empty")
        if len(txt) > self.MAX_LENGTH:
            raise ValueError(f"OpinionText cannot exceed {self.MAX_LENGTH} characters")
        self.value = txt

    def __eq__(self, other):
        return isinstance(other, OpinionText) and self.value == other.value

    def __repr__(self):
        return f"OpinionText({self.value!r})"
