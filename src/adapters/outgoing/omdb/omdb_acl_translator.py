import logging
import re
from typing import Callable, Any, Dict
from domain.model.MovieAggregate import MovieAggregate
from domain.model.value.ImdbId import ImdbId

logger = logging.getLogger(__name__)


class OmdbACLTranslator:
    def __init__(self, attribute_handlers: Dict[str, Callable[[Any], Any]] = None):
        """
        Initialize the OmdbACLTranslator with a dictionary of attribute handlers.
        This class is based on the chain of responsibility pattern,
        where each handler filters or transforms the data.
        I decided to make the handlers injectable for testing purposes.
        """
        self.attribute_handlers: Dict[str, Callable[[Any], Any]] = attribute_handlers or {}

    def register_handlers(self) -> None:
        """
        Registers the default attribute handlers.
        This can be extended or overridden for custom behavior.
        """
        self.attribute_handlers.update({
            "year": self.handle_year,
            "imdb_id": self.handle_imdb_id,
            "title": self.handle_title,
            "genre": self.handle_genre,
            "director": self.handle_director,
            "actors": self.handle_actors,
            "imdb_rating": self.handle_imdb_rating,
            "plot": self.handle_plot,
        })

    def fallback_handler(self, attribute: str, value: Any) -> None:
        """
        Fallback handler for attributes without a specific handler.
        Logs and ignores unsupported attributes.
        """
        logger.info(f"No handler for attribute '{attribute}' — discarding it.")
        return None

    def process_attributes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes attributes from the raw data using the attribute handlers.
        Falls back on the fallback_handler for unsupported attributes.
        """
        output = {}
        for key, value in data.items():
            handler = self.attribute_handlers.get(key, self.fallback_handler)
            result = handler(key, value) if handler else None
            if result is not None:
                output[key] = result
        return output

    def translate_omdb_to_domain_dict(self, raw: dict) -> dict[str, Any]:
        """
        Translates raw OMDb data into a sanitized domain dictionary.
        """
        return self.process_attributes(raw)

    def translate_omdb_to_domain_type(self, raw: dict) -> MovieAggregate:
        """
        Translates raw OMDb data into a MovieAggregate object.
        """
        clean_data = self.translate_omdb_to_domain_dict(raw)
        logger.info(f"Translating OMDb data to MovieAggregate: {clean_data}")
        return MovieAggregate(
            imdb_id=ImdbId(clean_data["imdb_id"]),
            title=clean_data["title"],
            year=clean_data["year"],
            genre=clean_data["genre"],
            director=clean_data["director"],
            actors=clean_data["actors"],
            imdb_rating=clean_data["imdb_rating"],
            plot=clean_data["plot"],
        )

    @staticmethod
    def get_year_interpretation(value: str) -> str:
        """
        Extracts a four-digit year from a string, if possible.
        """
        year_digits = re.sub(r"\D", "", value)
        return None if len(year_digits) < 4 else year_digits[:4]

    # Default handlers
    def handle_year(self, key: str, value: Any) -> str | None:
        if value and isinstance(value, (int, str)):
            try:
                return self.get_year_interpretation(str(value))
            except ValueError:
                return None
        return None

    def handle_imdb_id(self, key: str, value: Any) -> str:
        return value.strip() if isinstance(value, str) else None

    def handle_title(self, key: str, value: Any) -> str:
        return value.strip() if isinstance(value, str) else None

    def handle_genre(self, key: str, value: Any) -> str:
        return value.strip() if isinstance(value, str) else None

    def handle_director(self, key: str, value: Any) -> str:
        return value.strip() if isinstance(value, str) else None

    def handle_imdb_rating(self, key: str, value: Any) -> str:
        return value.strip() if isinstance(value, str) else None

    def handle_actors(self, key: str, value: Any) -> Any:
        return value

    def handle_plot(self, key: str, value: Any) -> str:
        return value.strip() if isinstance(value, str) else None
