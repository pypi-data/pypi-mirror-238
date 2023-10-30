from typing import TypeVar, Optional

from fastapi import Query, Depends
from starlette.requests import Request

from fastutils_hmarcuzzo.constants.regex_expressions import (
    REGEX_ORDER_BY_QUERY,
    REGEX_ALPHANUMERIC_WITH_UNDERSCORE as ALPHANUMERIC_WITH_UNDERSCORE,
)
from fastutils_hmarcuzzo.decorators.simple_pagination_decorator import PaginationOptionsProvider
from fastutils_hmarcuzzo.types.find_many_options import FindManyOptions
from fastutils_hmarcuzzo.utils.pagination_utils import PaginationUtils

E = TypeVar("E")


class PaginationWithSearchProvider(PaginationOptionsProvider):
    def __init__(
        self,
        entity: E,
        use_search: bool = True,
        use_sort: bool = True,
        use_columns: bool = False,
        use_search_all: bool = False,
    ):
        self.entity = entity

        self.use_search = use_search
        self.use_sort = use_sort
        self.use_columns = use_columns
        self.use_search_all = use_search_all

    def __call__(
        self,
        request: Request,
        search: list[str]
        | None = Query(
            default=None,
            regex=f"^{ALPHANUMERIC_WITH_UNDERSCORE}:{ALPHANUMERIC_WITH_UNDERSCORE}$",
            example=["field:value"],
        ),
        sort: list[str]
        | None = Query(
            default=None,
            regex=f"^{ALPHANUMERIC_WITH_UNDERSCORE}:{REGEX_ORDER_BY_QUERY}",
            example=["field:by"],
        ),
        columns: list[str]
        | None = Query(
            default=None,
            regex=f"^{ALPHANUMERIC_WITH_UNDERSCORE}$",
            example=["field"],
        ),
        search_all: str
        | None = Query(
            default=None,
            example=["value"],
        ),
    ) -> FindManyOptions:
        paging_params = super().__call__(request)

        return paging_params
