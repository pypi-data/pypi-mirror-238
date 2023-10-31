"""
Main interface for finspace service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_finspace import (
        Client,
        ListKxEnvironmentsPaginator,
        finspaceClient,
    )

    session = Session()
    client: finspaceClient = session.client("finspace")

    list_kx_environments_paginator: ListKxEnvironmentsPaginator = client.get_paginator("list_kx_environments")
    ```
"""

from .client import finspaceClient
from .paginator import ListKxEnvironmentsPaginator

Client = finspaceClient

__all__ = ("Client", "ListKxEnvironmentsPaginator", "finspaceClient")
