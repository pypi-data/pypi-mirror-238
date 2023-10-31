"""
Type annotations for redshift-serverless service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_redshift_serverless.client import RedshiftServerlessClient
    from mypy_boto3_redshift_serverless.paginator import (
        ListCustomDomainAssociationsPaginator,
        ListEndpointAccessPaginator,
        ListNamespacesPaginator,
        ListRecoveryPointsPaginator,
        ListSnapshotsPaginator,
        ListTableRestoreStatusPaginator,
        ListUsageLimitsPaginator,
        ListWorkgroupsPaginator,
    )

    session = Session()
    client: RedshiftServerlessClient = session.client("redshift-serverless")

    list_custom_domain_associations_paginator: ListCustomDomainAssociationsPaginator = client.get_paginator("list_custom_domain_associations")
    list_endpoint_access_paginator: ListEndpointAccessPaginator = client.get_paginator("list_endpoint_access")
    list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
    list_recovery_points_paginator: ListRecoveryPointsPaginator = client.get_paginator("list_recovery_points")
    list_snapshots_paginator: ListSnapshotsPaginator = client.get_paginator("list_snapshots")
    list_table_restore_status_paginator: ListTableRestoreStatusPaginator = client.get_paginator("list_table_restore_status")
    list_usage_limits_paginator: ListUsageLimitsPaginator = client.get_paginator("list_usage_limits")
    list_workgroups_paginator: ListWorkgroupsPaginator = client.get_paginator("list_workgroups")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import UsageLimitUsageTypeType
from .type_defs import (
    ListCustomDomainAssociationsResponseTypeDef,
    ListEndpointAccessResponseTypeDef,
    ListNamespacesResponseTypeDef,
    ListRecoveryPointsResponseTypeDef,
    ListSnapshotsResponseTypeDef,
    ListTableRestoreStatusResponseTypeDef,
    ListUsageLimitsResponseTypeDef,
    ListWorkgroupsResponseTypeDef,
    PaginatorConfigTypeDef,
    TimestampTypeDef,
)

__all__ = (
    "ListCustomDomainAssociationsPaginator",
    "ListEndpointAccessPaginator",
    "ListNamespacesPaginator",
    "ListRecoveryPointsPaginator",
    "ListSnapshotsPaginator",
    "ListTableRestoreStatusPaginator",
    "ListUsageLimitsPaginator",
    "ListWorkgroupsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListCustomDomainAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListCustomDomainAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listcustomdomainassociationspaginator)
    """

    def paginate(
        self,
        *,
        customDomainCertificateArn: str = ...,
        customDomainName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCustomDomainAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListCustomDomainAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listcustomdomainassociationspaginator)
        """


class ListEndpointAccessPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListEndpointAccess)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listendpointaccesspaginator)
    """

    def paginate(
        self,
        *,
        vpcId: str = ...,
        workgroupName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEndpointAccessResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListEndpointAccess.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listendpointaccesspaginator)
        """


class ListNamespacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListNamespaces)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listnamespacespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListNamespaces.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listnamespacespaginator)
        """


class ListRecoveryPointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListRecoveryPoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listrecoverypointspaginator)
    """

    def paginate(
        self,
        *,
        endTime: TimestampTypeDef = ...,
        namespaceArn: str = ...,
        namespaceName: str = ...,
        startTime: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRecoveryPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListRecoveryPoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listrecoverypointspaginator)
        """


class ListSnapshotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListSnapshots)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listsnapshotspaginator)
    """

    def paginate(
        self,
        *,
        endTime: TimestampTypeDef = ...,
        namespaceArn: str = ...,
        namespaceName: str = ...,
        ownerAccount: str = ...,
        startTime: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListSnapshots.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listsnapshotspaginator)
        """


class ListTableRestoreStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListTableRestoreStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listtablerestorestatuspaginator)
    """

    def paginate(
        self,
        *,
        namespaceName: str = ...,
        workgroupName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTableRestoreStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListTableRestoreStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listtablerestorestatuspaginator)
        """


class ListUsageLimitsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListUsageLimits)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listusagelimitspaginator)
    """

    def paginate(
        self,
        *,
        resourceArn: str = ...,
        usageType: UsageLimitUsageTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUsageLimitsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListUsageLimits.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listusagelimitspaginator)
        """


class ListWorkgroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListWorkgroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listworkgroupspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkgroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Paginator.ListWorkgroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_serverless/paginators/#listworkgroupspaginator)
        """
