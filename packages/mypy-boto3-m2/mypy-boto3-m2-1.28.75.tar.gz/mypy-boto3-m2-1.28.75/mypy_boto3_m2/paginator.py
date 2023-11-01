"""
Type annotations for m2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_m2.client import MainframeModernizationClient
    from mypy_boto3_m2.paginator import (
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
        ListBatchJobDefinitionsPaginator,
        ListBatchJobExecutionsPaginator,
        ListDataSetImportHistoryPaginator,
        ListDataSetsPaginator,
        ListDeploymentsPaginator,
        ListEngineVersionsPaginator,
        ListEnvironmentsPaginator,
    )

    session = Session()
    client: MainframeModernizationClient = session.client("m2")

    list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_batch_job_definitions_paginator: ListBatchJobDefinitionsPaginator = client.get_paginator("list_batch_job_definitions")
    list_batch_job_executions_paginator: ListBatchJobExecutionsPaginator = client.get_paginator("list_batch_job_executions")
    list_data_set_import_history_paginator: ListDataSetImportHistoryPaginator = client.get_paginator("list_data_set_import_history")
    list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
    list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
    list_engine_versions_paginator: ListEngineVersionsPaginator = client.get_paginator("list_engine_versions")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""

from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import BatchJobExecutionStatusType, EngineTypeType
from .type_defs import (
    ListApplicationsResponseTypeDef,
    ListApplicationVersionsResponseTypeDef,
    ListBatchJobDefinitionsResponseTypeDef,
    ListBatchJobExecutionsResponseTypeDef,
    ListDataSetImportHistoryResponseTypeDef,
    ListDataSetsResponseTypeDef,
    ListDeploymentsResponseTypeDef,
    ListEngineVersionsResponseTypeDef,
    ListEnvironmentsResponseTypeDef,
    PaginatorConfigTypeDef,
    TimestampTypeDef,
)

__all__ = (
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
    "ListBatchJobDefinitionsPaginator",
    "ListBatchJobExecutionsPaginator",
    "ListDataSetImportHistoryPaginator",
    "ListDataSetsPaginator",
    "ListDeploymentsPaginator",
    "ListEngineVersionsPaginator",
    "ListEnvironmentsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListApplicationVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listapplicationversionspaginator)
    """

    def paginate(
        self, *, applicationId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListApplicationVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listapplicationversionspaginator)
        """


class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListApplications)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listapplicationspaginator)
    """

    def paginate(
        self,
        *,
        environmentId: str = ...,
        names: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListApplications.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listapplicationspaginator)
        """


class ListBatchJobDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListBatchJobDefinitions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listbatchjobdefinitionspaginator)
    """

    def paginate(
        self,
        *,
        applicationId: str,
        prefix: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBatchJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListBatchJobDefinitions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listbatchjobdefinitionspaginator)
        """


class ListBatchJobExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListBatchJobExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listbatchjobexecutionspaginator)
    """

    def paginate(
        self,
        *,
        applicationId: str,
        executionIds: Sequence[str] = ...,
        jobName: str = ...,
        startedAfter: TimestampTypeDef = ...,
        startedBefore: TimestampTypeDef = ...,
        status: BatchJobExecutionStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBatchJobExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListBatchJobExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listbatchjobexecutionspaginator)
        """


class ListDataSetImportHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListDataSetImportHistory)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listdatasetimporthistorypaginator)
    """

    def paginate(
        self, *, applicationId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDataSetImportHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListDataSetImportHistory.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listdatasetimporthistorypaginator)
        """


class ListDataSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListDataSets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listdatasetspaginator)
    """

    def paginate(
        self,
        *,
        applicationId: str,
        nameFilter: str = ...,
        prefix: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListDataSets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listdatasetspaginator)
        """


class ListDeploymentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListDeployments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listdeploymentspaginator)
    """

    def paginate(
        self, *, applicationId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListDeployments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listdeploymentspaginator)
        """


class ListEngineVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListEngineVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listengineversionspaginator)
    """

    def paginate(
        self, *, engineType: EngineTypeType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEngineVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListEngineVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listengineversionspaginator)
        """


class ListEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListEnvironments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listenvironmentspaginator)
    """

    def paginate(
        self,
        *,
        engineType: EngineTypeType = ...,
        names: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2.html#MainframeModernization.Paginator.ListEnvironments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/paginators/#listenvironmentspaginator)
        """
