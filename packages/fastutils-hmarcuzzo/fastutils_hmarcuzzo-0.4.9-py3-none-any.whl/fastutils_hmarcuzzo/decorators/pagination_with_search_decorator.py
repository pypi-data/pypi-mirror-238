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

    def apply_pagination_options(self):
        def decorator(func):
            def wrapper(*args, **kwargs):
                attributes = ["search", "sort", "columns", "search_all"]
                query_funcs = [
                    self._search_query,
                    self._sort_query,
                    self._columns_query,
                    self._search_all_query,
                ]
                use_objects = [
                    self.use_search,
                    self.use_sort,
                    self.use_columns,
                    self.use_search_all,
                ]

                kwargs.update(
                    {
                        attr: query_func(use_obj)
                        for attr, query_func, use_obj in zip(attributes, query_funcs, use_objects)
                    }
                )
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @apply_pagination_options()
    def __call__(
        self,
        request: Request,
        search: list[str] | None = None,
        sort: list[str] | None = None,
        columns: list[str] | None = None,
        search_all: str | None = None,
    ) -> FindManyOptions:
        paging_params = PaginationUtils.get_pagination_from_request(request)

        return PaginationUtils.format_pagination_options(paging_params)

    @staticmethod
    def _search_query(use_search) -> Optional[Query]:
        return (
            Query(
                default=None,
                regex=f"^{ALPHANUMERIC_WITH_UNDERSCORE}:{ALPHANUMERIC_WITH_UNDERSCORE}$",
                example=["field:value"],
            )
            if use_search
            else None
        )

    @staticmethod
    def _sort_query(use_sort) -> Optional[Query]:
        return (
            Query(
                default=None,
                regex=f"^{ALPHANUMERIC_WITH_UNDERSCORE}:{REGEX_ORDER_BY_QUERY}",
                example=["field:by"],
            )
            if use_sort
            else None
        )

    @staticmethod
    def _columns_query(use_columns) -> Optional[Query]:
        return (
            Query(
                default=None,
                regex=f"^{ALPHANUMERIC_WITH_UNDERSCORE}$",
                example=["field"],
            )
            if use_columns
            else None
        )

    @staticmethod
    def _search_all_query(use_search_all) -> Optional[Query]:
        return (
            Query(
                default=None,
                example=["value"],
            )
            if use_search_all
            else None
        )
