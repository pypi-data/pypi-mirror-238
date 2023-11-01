"""
Type annotations for m2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_m2/type_defs/)

Usage::

    ```python
    from mypy_boto3_m2.type_defs import AlternateKeyTypeDef

    data: AlternateKeyTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ApplicationDeploymentLifecycleType,
    ApplicationLifecycleType,
    ApplicationVersionLifecycleType,
    BatchJobExecutionStatusType,
    BatchJobTypeType,
    DataSetTaskLifecycleType,
    DeploymentLifecycleType,
    EngineTypeType,
    EnvironmentLifecycleType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AlternateKeyTypeDef",
    "ApplicationSummaryTypeDef",
    "ApplicationVersionSummaryTypeDef",
    "FileBatchJobDefinitionTypeDef",
    "ScriptBatchJobDefinitionTypeDef",
    "FileBatchJobIdentifierTypeDef",
    "ScriptBatchJobIdentifierTypeDef",
    "CancelBatchJobExecutionRequestRequestTypeDef",
    "DefinitionTypeDef",
    "ResponseMetadataTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "HighAvailabilityConfigTypeDef",
    "ExternalLocationTypeDef",
    "DataSetImportSummaryTypeDef",
    "DataSetSummaryTypeDef",
    "RecordLengthTypeDef",
    "GdgDetailAttributesTypeDef",
    "PoDetailAttributesTypeDef",
    "PsDetailAttributesTypeDef",
    "GdgAttributesTypeDef",
    "PoAttributesTypeDef",
    "PsAttributesTypeDef",
    "DeleteApplicationFromEnvironmentRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeployedVersionSummaryTypeDef",
    "DeploymentSummaryTypeDef",
    "EfsStorageConfigurationTypeDef",
    "EngineVersionsSummaryTypeDef",
    "EnvironmentSummaryTypeDef",
    "FsxStorageConfigurationTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "LogGroupSummaryTypeDef",
    "GetApplicationVersionRequestRequestTypeDef",
    "GetBatchJobExecutionRequestRequestTypeDef",
    "GetDataSetDetailsRequestRequestTypeDef",
    "GetDataSetImportTaskRequestRequestTypeDef",
    "GetDeploymentRequestRequestTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "JobIdentifierTypeDef",
    "PaginatorConfigTypeDef",
    "ListApplicationVersionsRequestRequestTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListBatchJobDefinitionsRequestRequestTypeDef",
    "TimestampTypeDef",
    "ListDataSetImportHistoryRequestRequestTypeDef",
    "ListDataSetsRequestRequestTypeDef",
    "ListDeploymentsRequestRequestTypeDef",
    "ListEngineVersionsRequestRequestTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "MaintenanceScheduleTypeDef",
    "PrimaryKeyTypeDef",
    "StartApplicationRequestRequestTypeDef",
    "StopApplicationRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
    "BatchJobDefinitionTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateDataSetImportTaskResponseTypeDef",
    "CreateDeploymentResponseTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "GetApplicationVersionResponseTypeDef",
    "GetDeploymentResponseTypeDef",
    "GetSignedBluinsightsUrlResponseTypeDef",
    "ListApplicationVersionsResponseTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartBatchJobResponseTypeDef",
    "UpdateApplicationResponseTypeDef",
    "UpdateEnvironmentResponseTypeDef",
    "DataSetImportTaskTypeDef",
    "GetDataSetImportTaskResponseTypeDef",
    "ListDataSetsResponseTypeDef",
    "ListDeploymentsResponseTypeDef",
    "ListEngineVersionsResponseTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "StorageConfigurationTypeDef",
    "GetApplicationResponseTypeDef",
    "S3BatchJobIdentifierTypeDef",
    "ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef",
    "ListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef",
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    "ListDeploymentsRequestListDeploymentsPaginateTypeDef",
    "ListEngineVersionsRequestListEngineVersionsPaginateTypeDef",
    "ListEnvironmentsRequestListEnvironmentsPaginateTypeDef",
    "ListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef",
    "ListBatchJobExecutionsRequestRequestTypeDef",
    "PendingMaintenanceTypeDef",
    "VsamAttributesTypeDef",
    "VsamDetailAttributesTypeDef",
    "ListBatchJobDefinitionsResponseTypeDef",
    "ListDataSetImportHistoryResponseTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "BatchJobIdentifierTypeDef",
    "GetEnvironmentResponseTypeDef",
    "DatasetOrgAttributesTypeDef",
    "DatasetDetailOrgAttributesTypeDef",
    "BatchJobExecutionSummaryTypeDef",
    "GetBatchJobExecutionResponseTypeDef",
    "StartBatchJobRequestRequestTypeDef",
    "DataSetTypeDef",
    "GetDataSetDetailsResponseTypeDef",
    "ListBatchJobExecutionsResponseTypeDef",
    "DataSetImportItemTypeDef",
    "DataSetImportConfigTypeDef",
    "CreateDataSetImportTaskRequestRequestTypeDef",
)

AlternateKeyTypeDef = TypedDict(
    "AlternateKeyTypeDef",
    {
        "length": int,
        "offset": int,
        "allowDuplicates": NotRequired[bool],
        "name": NotRequired[str],
    },
)

ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "applicationArn": str,
        "applicationId": str,
        "applicationVersion": int,
        "creationTime": datetime,
        "engineType": EngineTypeType,
        "name": str,
        "status": ApplicationLifecycleType,
        "deploymentStatus": NotRequired[ApplicationDeploymentLifecycleType],
        "description": NotRequired[str],
        "environmentId": NotRequired[str],
        "lastStartTime": NotRequired[datetime],
        "roleArn": NotRequired[str],
        "versionStatus": NotRequired[ApplicationVersionLifecycleType],
    },
)

ApplicationVersionSummaryTypeDef = TypedDict(
    "ApplicationVersionSummaryTypeDef",
    {
        "applicationVersion": int,
        "creationTime": datetime,
        "status": ApplicationVersionLifecycleType,
        "statusReason": NotRequired[str],
    },
)

FileBatchJobDefinitionTypeDef = TypedDict(
    "FileBatchJobDefinitionTypeDef",
    {
        "fileName": str,
        "folderPath": NotRequired[str],
    },
)

ScriptBatchJobDefinitionTypeDef = TypedDict(
    "ScriptBatchJobDefinitionTypeDef",
    {
        "scriptName": str,
    },
)

FileBatchJobIdentifierTypeDef = TypedDict(
    "FileBatchJobIdentifierTypeDef",
    {
        "fileName": str,
        "folderPath": NotRequired[str],
    },
)

ScriptBatchJobIdentifierTypeDef = TypedDict(
    "ScriptBatchJobIdentifierTypeDef",
    {
        "scriptName": str,
    },
)

CancelBatchJobExecutionRequestRequestTypeDef = TypedDict(
    "CancelBatchJobExecutionRequestRequestTypeDef",
    {
        "applicationId": str,
        "executionId": str,
    },
)

DefinitionTypeDef = TypedDict(
    "DefinitionTypeDef",
    {
        "content": NotRequired[str],
        "s3Location": NotRequired[str],
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

CreateDeploymentRequestRequestTypeDef = TypedDict(
    "CreateDeploymentRequestRequestTypeDef",
    {
        "applicationId": str,
        "applicationVersion": int,
        "environmentId": str,
        "clientToken": NotRequired[str],
    },
)

HighAvailabilityConfigTypeDef = TypedDict(
    "HighAvailabilityConfigTypeDef",
    {
        "desiredCapacity": int,
    },
)

ExternalLocationTypeDef = TypedDict(
    "ExternalLocationTypeDef",
    {
        "s3Location": NotRequired[str],
    },
)

DataSetImportSummaryTypeDef = TypedDict(
    "DataSetImportSummaryTypeDef",
    {
        "failed": int,
        "inProgress": int,
        "pending": int,
        "succeeded": int,
        "total": int,
    },
)

DataSetSummaryTypeDef = TypedDict(
    "DataSetSummaryTypeDef",
    {
        "dataSetName": str,
        "creationTime": NotRequired[datetime],
        "dataSetOrg": NotRequired[str],
        "format": NotRequired[str],
        "lastReferencedTime": NotRequired[datetime],
        "lastUpdatedTime": NotRequired[datetime],
    },
)

RecordLengthTypeDef = TypedDict(
    "RecordLengthTypeDef",
    {
        "max": int,
        "min": int,
    },
)

GdgDetailAttributesTypeDef = TypedDict(
    "GdgDetailAttributesTypeDef",
    {
        "limit": NotRequired[int],
        "rollDisposition": NotRequired[str],
    },
)

PoDetailAttributesTypeDef = TypedDict(
    "PoDetailAttributesTypeDef",
    {
        "encoding": str,
        "format": str,
    },
)

PsDetailAttributesTypeDef = TypedDict(
    "PsDetailAttributesTypeDef",
    {
        "encoding": str,
        "format": str,
    },
)

GdgAttributesTypeDef = TypedDict(
    "GdgAttributesTypeDef",
    {
        "limit": NotRequired[int],
        "rollDisposition": NotRequired[str],
    },
)

PoAttributesTypeDef = TypedDict(
    "PoAttributesTypeDef",
    {
        "format": str,
        "memberFileExtensions": Sequence[str],
        "encoding": NotRequired[str],
    },
)

PsAttributesTypeDef = TypedDict(
    "PsAttributesTypeDef",
    {
        "format": str,
        "encoding": NotRequired[str],
    },
)

DeleteApplicationFromEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteApplicationFromEnvironmentRequestRequestTypeDef",
    {
        "applicationId": str,
        "environmentId": str,
    },
)

DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)

DeleteEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

DeployedVersionSummaryTypeDef = TypedDict(
    "DeployedVersionSummaryTypeDef",
    {
        "applicationVersion": int,
        "status": DeploymentLifecycleType,
        "statusReason": NotRequired[str],
    },
)

DeploymentSummaryTypeDef = TypedDict(
    "DeploymentSummaryTypeDef",
    {
        "applicationId": str,
        "applicationVersion": int,
        "creationTime": datetime,
        "deploymentId": str,
        "environmentId": str,
        "status": DeploymentLifecycleType,
        "statusReason": NotRequired[str],
    },
)

EfsStorageConfigurationTypeDef = TypedDict(
    "EfsStorageConfigurationTypeDef",
    {
        "fileSystemId": str,
        "mountPoint": str,
    },
)

EngineVersionsSummaryTypeDef = TypedDict(
    "EngineVersionsSummaryTypeDef",
    {
        "engineType": str,
        "engineVersion": str,
    },
)

EnvironmentSummaryTypeDef = TypedDict(
    "EnvironmentSummaryTypeDef",
    {
        "creationTime": datetime,
        "engineType": EngineTypeType,
        "engineVersion": str,
        "environmentArn": str,
        "environmentId": str,
        "instanceType": str,
        "name": str,
        "status": EnvironmentLifecycleType,
    },
)

FsxStorageConfigurationTypeDef = TypedDict(
    "FsxStorageConfigurationTypeDef",
    {
        "fileSystemId": str,
        "mountPoint": str,
    },
)

GetApplicationRequestRequestTypeDef = TypedDict(
    "GetApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)

LogGroupSummaryTypeDef = TypedDict(
    "LogGroupSummaryTypeDef",
    {
        "logGroupName": str,
        "logType": str,
    },
)

GetApplicationVersionRequestRequestTypeDef = TypedDict(
    "GetApplicationVersionRequestRequestTypeDef",
    {
        "applicationId": str,
        "applicationVersion": int,
    },
)

GetBatchJobExecutionRequestRequestTypeDef = TypedDict(
    "GetBatchJobExecutionRequestRequestTypeDef",
    {
        "applicationId": str,
        "executionId": str,
    },
)

GetDataSetDetailsRequestRequestTypeDef = TypedDict(
    "GetDataSetDetailsRequestRequestTypeDef",
    {
        "applicationId": str,
        "dataSetName": str,
    },
)

GetDataSetImportTaskRequestRequestTypeDef = TypedDict(
    "GetDataSetImportTaskRequestRequestTypeDef",
    {
        "applicationId": str,
        "taskId": str,
    },
)

GetDeploymentRequestRequestTypeDef = TypedDict(
    "GetDeploymentRequestRequestTypeDef",
    {
        "applicationId": str,
        "deploymentId": str,
    },
)

GetEnvironmentRequestRequestTypeDef = TypedDict(
    "GetEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

JobIdentifierTypeDef = TypedDict(
    "JobIdentifierTypeDef",
    {
        "fileName": NotRequired[str],
        "scriptName": NotRequired[str],
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)

ListApplicationVersionsRequestRequestTypeDef = TypedDict(
    "ListApplicationVersionsRequestRequestTypeDef",
    {
        "applicationId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "environmentId": NotRequired[str],
        "maxResults": NotRequired[int],
        "names": NotRequired[Sequence[str]],
        "nextToken": NotRequired[str],
    },
)

ListBatchJobDefinitionsRequestRequestTypeDef = TypedDict(
    "ListBatchJobDefinitionsRequestRequestTypeDef",
    {
        "applicationId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "prefix": NotRequired[str],
    },
)

TimestampTypeDef = Union[datetime, str]
ListDataSetImportHistoryRequestRequestTypeDef = TypedDict(
    "ListDataSetImportHistoryRequestRequestTypeDef",
    {
        "applicationId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListDataSetsRequestRequestTypeDef = TypedDict(
    "ListDataSetsRequestRequestTypeDef",
    {
        "applicationId": str,
        "maxResults": NotRequired[int],
        "nameFilter": NotRequired[str],
        "nextToken": NotRequired[str],
        "prefix": NotRequired[str],
    },
)

ListDeploymentsRequestRequestTypeDef = TypedDict(
    "ListDeploymentsRequestRequestTypeDef",
    {
        "applicationId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListEngineVersionsRequestRequestTypeDef = TypedDict(
    "ListEngineVersionsRequestRequestTypeDef",
    {
        "engineType": NotRequired[EngineTypeType],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListEnvironmentsRequestRequestTypeDef = TypedDict(
    "ListEnvironmentsRequestRequestTypeDef",
    {
        "engineType": NotRequired[EngineTypeType],
        "maxResults": NotRequired[int],
        "names": NotRequired[Sequence[str]],
        "nextToken": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

MaintenanceScheduleTypeDef = TypedDict(
    "MaintenanceScheduleTypeDef",
    {
        "endTime": NotRequired[datetime],
        "startTime": NotRequired[datetime],
    },
)

PrimaryKeyTypeDef = TypedDict(
    "PrimaryKeyTypeDef",
    {
        "length": int,
        "offset": int,
        "name": NotRequired[str],
    },
)

StartApplicationRequestRequestTypeDef = TypedDict(
    "StartApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)

StopApplicationRequestRequestTypeDef = TypedDict(
    "StopApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
        "forceStop": NotRequired[bool],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "UpdateEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
        "applyDuringMaintenanceWindow": NotRequired[bool],
        "desiredCapacity": NotRequired[int],
        "engineVersion": NotRequired[str],
        "forceUpdate": NotRequired[bool],
        "instanceType": NotRequired[str],
        "preferredMaintenanceWindow": NotRequired[str],
    },
)

BatchJobDefinitionTypeDef = TypedDict(
    "BatchJobDefinitionTypeDef",
    {
        "fileBatchJobDefinition": NotRequired[FileBatchJobDefinitionTypeDef],
        "scriptBatchJobDefinition": NotRequired[ScriptBatchJobDefinitionTypeDef],
    },
)

CreateApplicationRequestRequestTypeDef = TypedDict(
    "CreateApplicationRequestRequestTypeDef",
    {
        "definition": DefinitionTypeDef,
        "engineType": EngineTypeType,
        "name": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "kmsKeyId": NotRequired[str],
        "roleArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

UpdateApplicationRequestRequestTypeDef = TypedDict(
    "UpdateApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
        "currentApplicationVersion": int,
        "definition": NotRequired[DefinitionTypeDef],
        "description": NotRequired[str],
    },
)

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "applicationArn": str,
        "applicationId": str,
        "applicationVersion": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSetImportTaskResponseTypeDef = TypedDict(
    "CreateDataSetImportTaskResponseTypeDef",
    {
        "taskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeploymentResponseTypeDef = TypedDict(
    "CreateDeploymentResponseTypeDef",
    {
        "deploymentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEnvironmentResponseTypeDef = TypedDict(
    "CreateEnvironmentResponseTypeDef",
    {
        "environmentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetApplicationVersionResponseTypeDef = TypedDict(
    "GetApplicationVersionResponseTypeDef",
    {
        "applicationVersion": int,
        "creationTime": datetime,
        "definitionContent": str,
        "description": str,
        "name": str,
        "status": ApplicationVersionLifecycleType,
        "statusReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeploymentResponseTypeDef = TypedDict(
    "GetDeploymentResponseTypeDef",
    {
        "applicationId": str,
        "applicationVersion": int,
        "creationTime": datetime,
        "deploymentId": str,
        "environmentId": str,
        "status": DeploymentLifecycleType,
        "statusReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSignedBluinsightsUrlResponseTypeDef = TypedDict(
    "GetSignedBluinsightsUrlResponseTypeDef",
    {
        "signedBiUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationVersionsResponseTypeDef = TypedDict(
    "ListApplicationVersionsResponseTypeDef",
    {
        "applicationVersions": List[ApplicationVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "applications": List[ApplicationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartBatchJobResponseTypeDef = TypedDict(
    "StartBatchJobResponseTypeDef",
    {
        "executionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApplicationResponseTypeDef = TypedDict(
    "UpdateApplicationResponseTypeDef",
    {
        "applicationVersion": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEnvironmentResponseTypeDef = TypedDict(
    "UpdateEnvironmentResponseTypeDef",
    {
        "environmentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataSetImportTaskTypeDef = TypedDict(
    "DataSetImportTaskTypeDef",
    {
        "status": DataSetTaskLifecycleType,
        "summary": DataSetImportSummaryTypeDef,
        "taskId": str,
        "statusReason": NotRequired[str],
    },
)

GetDataSetImportTaskResponseTypeDef = TypedDict(
    "GetDataSetImportTaskResponseTypeDef",
    {
        "status": DataSetTaskLifecycleType,
        "summary": DataSetImportSummaryTypeDef,
        "taskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataSetsResponseTypeDef = TypedDict(
    "ListDataSetsResponseTypeDef",
    {
        "dataSets": List[DataSetSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDeploymentsResponseTypeDef = TypedDict(
    "ListDeploymentsResponseTypeDef",
    {
        "deployments": List[DeploymentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEngineVersionsResponseTypeDef = TypedDict(
    "ListEngineVersionsResponseTypeDef",
    {
        "engineVersions": List[EngineVersionsSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentsResponseTypeDef = TypedDict(
    "ListEnvironmentsResponseTypeDef",
    {
        "environments": List[EnvironmentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StorageConfigurationTypeDef = TypedDict(
    "StorageConfigurationTypeDef",
    {
        "efs": NotRequired[EfsStorageConfigurationTypeDef],
        "fsx": NotRequired[FsxStorageConfigurationTypeDef],
    },
)

GetApplicationResponseTypeDef = TypedDict(
    "GetApplicationResponseTypeDef",
    {
        "applicationArn": str,
        "applicationId": str,
        "creationTime": datetime,
        "deployedVersion": DeployedVersionSummaryTypeDef,
        "description": str,
        "engineType": EngineTypeType,
        "environmentId": str,
        "kmsKeyId": str,
        "lastStartTime": datetime,
        "latestVersion": ApplicationVersionSummaryTypeDef,
        "listenerArns": List[str],
        "listenerPorts": List[int],
        "loadBalancerDnsName": str,
        "logGroups": List[LogGroupSummaryTypeDef],
        "name": str,
        "roleArn": str,
        "status": ApplicationLifecycleType,
        "statusReason": str,
        "tags": Dict[str, str],
        "targetGroupArns": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

S3BatchJobIdentifierTypeDef = TypedDict(
    "S3BatchJobIdentifierTypeDef",
    {
        "bucket": str,
        "identifier": JobIdentifierTypeDef,
        "keyPrefix": NotRequired[str],
    },
)

ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef = TypedDict(
    "ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef",
    {
        "applicationId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "environmentId": NotRequired[str],
        "names": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef = TypedDict(
    "ListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef",
    {
        "applicationId": str,
        "prefix": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef = TypedDict(
    "ListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef",
    {
        "applicationId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDataSetsRequestListDataSetsPaginateTypeDef = TypedDict(
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    {
        "applicationId": str,
        "nameFilter": NotRequired[str],
        "prefix": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDeploymentsRequestListDeploymentsPaginateTypeDef = TypedDict(
    "ListDeploymentsRequestListDeploymentsPaginateTypeDef",
    {
        "applicationId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListEngineVersionsRequestListEngineVersionsPaginateTypeDef = TypedDict(
    "ListEngineVersionsRequestListEngineVersionsPaginateTypeDef",
    {
        "engineType": NotRequired[EngineTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListEnvironmentsRequestListEnvironmentsPaginateTypeDef = TypedDict(
    "ListEnvironmentsRequestListEnvironmentsPaginateTypeDef",
    {
        "engineType": NotRequired[EngineTypeType],
        "names": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef = TypedDict(
    "ListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef",
    {
        "applicationId": str,
        "executionIds": NotRequired[Sequence[str]],
        "jobName": NotRequired[str],
        "startedAfter": NotRequired[TimestampTypeDef],
        "startedBefore": NotRequired[TimestampTypeDef],
        "status": NotRequired[BatchJobExecutionStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListBatchJobExecutionsRequestRequestTypeDef = TypedDict(
    "ListBatchJobExecutionsRequestRequestTypeDef",
    {
        "applicationId": str,
        "executionIds": NotRequired[Sequence[str]],
        "jobName": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "startedAfter": NotRequired[TimestampTypeDef],
        "startedBefore": NotRequired[TimestampTypeDef],
        "status": NotRequired[BatchJobExecutionStatusType],
    },
)

PendingMaintenanceTypeDef = TypedDict(
    "PendingMaintenanceTypeDef",
    {
        "engineVersion": NotRequired[str],
        "schedule": NotRequired[MaintenanceScheduleTypeDef],
    },
)

VsamAttributesTypeDef = TypedDict(
    "VsamAttributesTypeDef",
    {
        "format": str,
        "alternateKeys": NotRequired[Sequence[AlternateKeyTypeDef]],
        "compressed": NotRequired[bool],
        "encoding": NotRequired[str],
        "primaryKey": NotRequired[PrimaryKeyTypeDef],
    },
)

VsamDetailAttributesTypeDef = TypedDict(
    "VsamDetailAttributesTypeDef",
    {
        "alternateKeys": NotRequired[List[AlternateKeyTypeDef]],
        "cacheAtStartup": NotRequired[bool],
        "compressed": NotRequired[bool],
        "encoding": NotRequired[str],
        "primaryKey": NotRequired[PrimaryKeyTypeDef],
        "recordFormat": NotRequired[str],
    },
)

ListBatchJobDefinitionsResponseTypeDef = TypedDict(
    "ListBatchJobDefinitionsResponseTypeDef",
    {
        "batchJobDefinitions": List[BatchJobDefinitionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataSetImportHistoryResponseTypeDef = TypedDict(
    "ListDataSetImportHistoryResponseTypeDef",
    {
        "dataSetImportTasks": List[DataSetImportTaskTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEnvironmentRequestRequestTypeDef = TypedDict(
    "CreateEnvironmentRequestRequestTypeDef",
    {
        "engineType": EngineTypeType,
        "instanceType": str,
        "name": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "engineVersion": NotRequired[str],
        "highAvailabilityConfig": NotRequired[HighAvailabilityConfigTypeDef],
        "kmsKeyId": NotRequired[str],
        "preferredMaintenanceWindow": NotRequired[str],
        "publiclyAccessible": NotRequired[bool],
        "securityGroupIds": NotRequired[Sequence[str]],
        "storageConfigurations": NotRequired[Sequence[StorageConfigurationTypeDef]],
        "subnetIds": NotRequired[Sequence[str]],
        "tags": NotRequired[Mapping[str, str]],
    },
)

BatchJobIdentifierTypeDef = TypedDict(
    "BatchJobIdentifierTypeDef",
    {
        "fileBatchJobIdentifier": NotRequired[FileBatchJobIdentifierTypeDef],
        "s3BatchJobIdentifier": NotRequired[S3BatchJobIdentifierTypeDef],
        "scriptBatchJobIdentifier": NotRequired[ScriptBatchJobIdentifierTypeDef],
    },
)

GetEnvironmentResponseTypeDef = TypedDict(
    "GetEnvironmentResponseTypeDef",
    {
        "actualCapacity": int,
        "creationTime": datetime,
        "description": str,
        "engineType": EngineTypeType,
        "engineVersion": str,
        "environmentArn": str,
        "environmentId": str,
        "highAvailabilityConfig": HighAvailabilityConfigTypeDef,
        "instanceType": str,
        "kmsKeyId": str,
        "loadBalancerArn": str,
        "name": str,
        "pendingMaintenance": PendingMaintenanceTypeDef,
        "preferredMaintenanceWindow": str,
        "publiclyAccessible": bool,
        "securityGroupIds": List[str],
        "status": EnvironmentLifecycleType,
        "statusReason": str,
        "storageConfigurations": List[StorageConfigurationTypeDef],
        "subnetIds": List[str],
        "tags": Dict[str, str],
        "vpcId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DatasetOrgAttributesTypeDef = TypedDict(
    "DatasetOrgAttributesTypeDef",
    {
        "gdg": NotRequired[GdgAttributesTypeDef],
        "po": NotRequired[PoAttributesTypeDef],
        "ps": NotRequired[PsAttributesTypeDef],
        "vsam": NotRequired[VsamAttributesTypeDef],
    },
)

DatasetDetailOrgAttributesTypeDef = TypedDict(
    "DatasetDetailOrgAttributesTypeDef",
    {
        "gdg": NotRequired[GdgDetailAttributesTypeDef],
        "po": NotRequired[PoDetailAttributesTypeDef],
        "ps": NotRequired[PsDetailAttributesTypeDef],
        "vsam": NotRequired[VsamDetailAttributesTypeDef],
    },
)

BatchJobExecutionSummaryTypeDef = TypedDict(
    "BatchJobExecutionSummaryTypeDef",
    {
        "applicationId": str,
        "executionId": str,
        "startTime": datetime,
        "status": BatchJobExecutionStatusType,
        "batchJobIdentifier": NotRequired[BatchJobIdentifierTypeDef],
        "endTime": NotRequired[datetime],
        "jobId": NotRequired[str],
        "jobName": NotRequired[str],
        "jobType": NotRequired[BatchJobTypeType],
        "returnCode": NotRequired[str],
    },
)

GetBatchJobExecutionResponseTypeDef = TypedDict(
    "GetBatchJobExecutionResponseTypeDef",
    {
        "applicationId": str,
        "batchJobIdentifier": BatchJobIdentifierTypeDef,
        "endTime": datetime,
        "executionId": str,
        "jobId": str,
        "jobName": str,
        "jobType": BatchJobTypeType,
        "jobUser": str,
        "returnCode": str,
        "startTime": datetime,
        "status": BatchJobExecutionStatusType,
        "statusReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartBatchJobRequestRequestTypeDef = TypedDict(
    "StartBatchJobRequestRequestTypeDef",
    {
        "applicationId": str,
        "batchJobIdentifier": BatchJobIdentifierTypeDef,
        "jobParams": NotRequired[Mapping[str, str]],
    },
)

DataSetTypeDef = TypedDict(
    "DataSetTypeDef",
    {
        "datasetName": str,
        "datasetOrg": DatasetOrgAttributesTypeDef,
        "recordLength": RecordLengthTypeDef,
        "relativePath": NotRequired[str],
        "storageType": NotRequired[str],
    },
)

GetDataSetDetailsResponseTypeDef = TypedDict(
    "GetDataSetDetailsResponseTypeDef",
    {
        "blocksize": int,
        "creationTime": datetime,
        "dataSetName": str,
        "dataSetOrg": DatasetDetailOrgAttributesTypeDef,
        "fileSize": int,
        "lastReferencedTime": datetime,
        "lastUpdatedTime": datetime,
        "location": str,
        "recordLength": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBatchJobExecutionsResponseTypeDef = TypedDict(
    "ListBatchJobExecutionsResponseTypeDef",
    {
        "batchJobExecutions": List[BatchJobExecutionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataSetImportItemTypeDef = TypedDict(
    "DataSetImportItemTypeDef",
    {
        "dataSet": DataSetTypeDef,
        "externalLocation": ExternalLocationTypeDef,
    },
)

DataSetImportConfigTypeDef = TypedDict(
    "DataSetImportConfigTypeDef",
    {
        "dataSets": NotRequired[Sequence[DataSetImportItemTypeDef]],
        "s3Location": NotRequired[str],
    },
)

CreateDataSetImportTaskRequestRequestTypeDef = TypedDict(
    "CreateDataSetImportTaskRequestRequestTypeDef",
    {
        "applicationId": str,
        "importConfig": DataSetImportConfigTypeDef,
        "clientToken": NotRequired[str],
    },
)
