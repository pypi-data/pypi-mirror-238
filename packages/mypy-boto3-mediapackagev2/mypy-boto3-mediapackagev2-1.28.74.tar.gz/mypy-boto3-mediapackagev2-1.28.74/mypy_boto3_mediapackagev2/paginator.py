"""
Type annotations for mediapackagev2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mediapackagev2.client import mediapackagev2Client
    from mypy_boto3_mediapackagev2.paginator import (
        ListChannelGroupsPaginator,
        ListChannelsPaginator,
        ListOriginEndpointsPaginator,
    )

    session = Session()
    client: mediapackagev2Client = session.client("mediapackagev2")

    list_channel_groups_paginator: ListChannelGroupsPaginator = client.get_paginator("list_channel_groups")
    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_origin_endpoints_paginator: ListOriginEndpointsPaginator = client.get_paginator("list_origin_endpoints")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListChannelGroupsResponseTypeDef,
    ListChannelsResponseTypeDef,
    ListOriginEndpointsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListChannelGroupsPaginator", "ListChannelsPaginator", "ListOriginEndpointsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChannelGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2.html#mediapackagev2.Paginator.ListChannelGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listchannelgroupspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListChannelGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2.html#mediapackagev2.Paginator.ListChannelGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listchannelgroupspaginator)
        """


class ListChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2.html#mediapackagev2.Paginator.ListChannels)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listchannelspaginator)
    """

    def paginate(
        self, *, ChannelGroupName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2.html#mediapackagev2.Paginator.ListChannels.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listchannelspaginator)
        """


class ListOriginEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2.html#mediapackagev2.Paginator.ListOriginEndpoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listoriginendpointspaginator)
    """

    def paginate(
        self,
        *,
        ChannelGroupName: str,
        ChannelName: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOriginEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2.html#mediapackagev2.Paginator.ListOriginEndpoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/paginators/#listoriginendpointspaginator)
        """
