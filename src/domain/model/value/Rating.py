class Rating:
    def __init__(self, value):
        try:
            rating = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Rating must be an integer, got {value!r}")
        if rating < 1 or rating > 10:
            raise ValueError("Rating must be between 1 and 10")
        self.value = rating

    def __eq__(self, other):
        return isinstance(other, Rating) and self.value == other.value

    def __repr__(self):
        return f"Rating({self.value})"
