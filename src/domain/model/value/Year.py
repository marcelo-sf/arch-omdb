import datetime

class Year:
    def __init__(self, value):
        if value is None:
            self.value = None
            return
        try:
            year = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Year must be an integer, got {value!r}")
        current = datetime.datetime.now().year

        # The earliest film listed on IMDb is "Passage de Venus", also known as the 1874 Venus transit.
        if year < 1874 or year > current:
            raise ValueError(f"Year must be between 1874 and {current}, got {year}")
        self.value = year

    def __eq__(self, other):
        return isinstance(other, Year) and self.value == other.value

    def __repr__(self):
        return f"Year({self.value})"
