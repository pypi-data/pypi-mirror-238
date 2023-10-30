from starlette.requests import Request

from fastutils_hmarcuzzo.types.find_many_options import FindManyOptions
from fastutils_hmarcuzzo.utils.pagination_utils import PaginationUtils


class PaginationOptionsProvider(object):
    def __call__(self, request: Request) -> FindManyOptions:
        paging_params = PaginationUtils.get_pagination_from_request(request)

        return PaginationUtils.format_pagination_options(paging_params)
