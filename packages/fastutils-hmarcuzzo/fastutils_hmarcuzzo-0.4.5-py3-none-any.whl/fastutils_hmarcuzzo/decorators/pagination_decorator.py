from typing import TypeVar, Optional

from fastapi import Query, Depends
from starlette.requests import Request

from fastutils_hmarcuzzo.constants.regex_expressions import (
    REGEX_ORDER_BY_QUERY,
    REGEX_ALPHANUMERIC_WITH_UNDERSCORE as ALPHANUMERIC_WITH_UNDERSCORE,
)
from fastutils_hmarcuzzo.types.find_many_options import FindManyOptions
from fastutils_hmarcuzzo.utils.pagination_utils import PaginationUtils

E = TypeVar("E")


class PaginationOptionsProvider(object):
    def __call__(self, request: Request) -> FindManyOptions:
        paging_params = PaginationUtils.get_pagination_from_request(request)

        return PaginationUtils.format_pagination_options(paging_params)


class PaginationWithSearchProvider(object):
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
        search: list[str] | None = Depends(None),
        sort: list[str] | None = Depends(None),
        columns: list[str] | None = Depends(None),
        search_all: str | None = Depends(None),
    ) -> FindManyOptions:
        paging_params = PaginationUtils.get_pagination_from_request(request)

        search = Depends(self._search_query())
        sort = Depends(self._sort_query())
        columns = Depends(self._columns_query())
        search_all = Depends(self._search_all_query())

        return PaginationUtils.format_pagination_options(paging_params)

    def _search_query(self) -> Optional[Query]:
        return (
            Query(
                default=None,
                regex=f"^{ALPHANUMERIC_WITH_UNDERSCORE}:{ALPHANUMERIC_WITH_UNDERSCORE}$",
                example=["field:value"],
            )
            if self.use_search
            else None
        )

    def _sort_query(self) -> Optional[Query]:
        return (
            Query(
                default=None,
                regex=f"^{ALPHANUMERIC_WITH_UNDERSCORE}:{REGEX_ORDER_BY_QUERY}",
                example=["field:by"],
            )
            if self.use_sort
            else None
        )

    def _columns_query(self) -> Optional[Query]:
        return (
            Query(
                default=None,
                regex=f"^{ALPHANUMERIC_WITH_UNDERSCORE}$",
                example=["field"],
            )
            if self.use_columns
            else None
        )

    def _search_all_query(self) -> Optional[Query]:
        return (
            Query(
                default=None,
                example=["value"],
            )
            if self.use_search_all
            else None
        )
