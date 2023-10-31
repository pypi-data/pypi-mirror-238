"""
Type annotations for finspace service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_finspace.client import finspaceClient
    from mypy_boto3_finspace.paginator import (
        ListKxEnvironmentsPaginator,
    )

    session = Session()
    client: finspaceClient = session.client("finspace")

    list_kx_environments_paginator: ListKxEnvironmentsPaginator = client.get_paginator("list_kx_environments")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListKxEnvironmentsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListKxEnvironmentsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListKxEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#finspace.Paginator.ListKxEnvironments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/paginators/#listkxenvironmentspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListKxEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#finspace.Paginator.ListKxEnvironments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/paginators/#listkxenvironmentspaginator)
        """
