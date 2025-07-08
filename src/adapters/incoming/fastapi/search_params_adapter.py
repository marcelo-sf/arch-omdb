from typing import Optional, TypedDict
from fastapi import HTTPException
from adapters.incoming.fastapi.schemas import MovieSearchParams


class AdaptedSearchParams(TypedDict):
    title: Optional[str]
    year: Optional[int]


class SearchParamsAdapter:
    @staticmethod
    async def adapt(json_payload: Optional[MovieSearchParams], params: Optional[MovieSearchParams]) -> AdaptedSearchParams:
        """
        Selects query string params or JSON payload using the rules:
        - If both params and JSON have title but one lacks year, the one with both overrides the other.
        - If both have title and year, the query string (params) takes precedence.

        :param json_payload: The FastAPI request object
        :param params: The query string parameters
        :return: An AdaptedSearchParams object
        """

        if json_payload is None and params is None:
            raise HTTPException(status_code=422, detail="at least`title` is required for movie search.")

        title_from_json = json_payload.title if json_payload is not None else None
        year_from_json = json_payload.year if json_payload is not None else None

        title_from_params = params.title if params is not None else None
        year_from_params = params.year if params is not None else None

        return SearchParamsAdapter.get_params_override_rules(title_from_json, title_from_params, year_from_json,
                                                             year_from_params)

    @staticmethod
    def get_params_override_rules(
            title_from_json: Optional[str],
            title_from_params: Optional[str],
            year_from_json: Optional[int],
            year_from_params: Optional[int]
    ) -> AdaptedSearchParams:

        result = AdaptedSearchParams(title="", year=None)

        if title_from_params and year_from_params:
            result = AdaptedSearchParams(title=title_from_params, year=year_from_params)
        elif title_from_json and year_from_json:
            result = AdaptedSearchParams(title=title_from_json, year=year_from_json)
        elif title_from_params:
            result = AdaptedSearchParams(title=title_from_params, year=year_from_json)
        elif title_from_json:
            result = AdaptedSearchParams(title=title_from_json, year=year_from_params)

        print(f"Search params override rules: {result}")
        return result
