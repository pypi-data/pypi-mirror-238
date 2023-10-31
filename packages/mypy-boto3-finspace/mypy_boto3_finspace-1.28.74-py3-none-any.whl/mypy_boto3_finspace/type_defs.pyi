"""
Type annotations for finspace service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/type_defs/)

Usage::

    ```python
    from mypy_boto3_finspace.type_defs import AutoScalingConfigurationTypeDef

    data: AutoScalingConfigurationTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ChangesetStatusType,
    ChangeTypeType,
    EnvironmentStatusType,
    ErrorDetailsType,
    FederationModeType,
    KxAzModeType,
    KxClusterCodeDeploymentStrategyType,
    KxClusterStatusType,
    KxClusterTypeType,
    KxDeploymentStrategyType,
    RuleActionType,
    dnsStatusType,
    tgwStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AutoScalingConfigurationTypeDef",
    "CapacityConfigurationTypeDef",
    "ChangeRequestTypeDef",
    "CodeConfigurationTypeDef",
    "FederationParametersTypeDef",
    "SuperuserParametersTypeDef",
    "ResponseMetadataTypeDef",
    "ErrorInfoTypeDef",
    "KxCacheStorageConfigurationTypeDef",
    "KxCommandLineArgumentTypeDef",
    "KxSavedownStorageConfigurationTypeDef",
    "VpcConfigurationTypeDef",
    "CreateKxDatabaseRequestRequestTypeDef",
    "CreateKxEnvironmentRequestRequestTypeDef",
    "CreateKxUserRequestRequestTypeDef",
    "CustomDNSServerTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeleteKxClusterRequestRequestTypeDef",
    "DeleteKxDatabaseRequestRequestTypeDef",
    "DeleteKxEnvironmentRequestRequestTypeDef",
    "DeleteKxUserRequestRequestTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "GetKxChangesetRequestRequestTypeDef",
    "GetKxClusterRequestRequestTypeDef",
    "GetKxConnectionStringRequestRequestTypeDef",
    "GetKxDatabaseRequestRequestTypeDef",
    "GetKxEnvironmentRequestRequestTypeDef",
    "GetKxUserRequestRequestTypeDef",
    "IcmpTypeCodeTypeDef",
    "KxChangesetListEntryTypeDef",
    "KxClusterCodeDeploymentConfigurationTypeDef",
    "KxClusterTypeDef",
    "KxDatabaseCacheConfigurationTypeDef",
    "KxDatabaseListEntryTypeDef",
    "KxDeploymentConfigurationTypeDef",
    "KxNodeTypeDef",
    "KxUserTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListKxChangesetsRequestRequestTypeDef",
    "ListKxClusterNodesRequestRequestTypeDef",
    "ListKxClustersRequestRequestTypeDef",
    "ListKxDatabasesRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListKxEnvironmentsRequestRequestTypeDef",
    "ListKxUsersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PortRangeTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateKxDatabaseRequestRequestTypeDef",
    "UpdateKxEnvironmentRequestRequestTypeDef",
    "UpdateKxUserRequestRequestTypeDef",
    "CreateKxChangesetRequestRequestTypeDef",
    "EnvironmentTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "CreateKxDatabaseResponseTypeDef",
    "CreateKxEnvironmentResponseTypeDef",
    "CreateKxUserResponseTypeDef",
    "GetKxConnectionStringResponseTypeDef",
    "GetKxDatabaseResponseTypeDef",
    "GetKxUserResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateKxDatabaseResponseTypeDef",
    "UpdateKxUserResponseTypeDef",
    "CreateKxChangesetResponseTypeDef",
    "GetKxChangesetResponseTypeDef",
    "ListKxChangesetsResponseTypeDef",
    "UpdateKxClusterCodeConfigurationRequestRequestTypeDef",
    "ListKxClustersResponseTypeDef",
    "KxDatabaseConfigurationTypeDef",
    "ListKxDatabasesResponseTypeDef",
    "ListKxClusterNodesResponseTypeDef",
    "ListKxUsersResponseTypeDef",
    "ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef",
    "NetworkACLEntryTypeDef",
    "GetEnvironmentResponseTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "UpdateEnvironmentResponseTypeDef",
    "CreateKxClusterRequestRequestTypeDef",
    "CreateKxClusterResponseTypeDef",
    "GetKxClusterResponseTypeDef",
    "UpdateKxClusterDatabasesRequestRequestTypeDef",
    "TransitGatewayConfigurationTypeDef",
    "GetKxEnvironmentResponseTypeDef",
    "KxEnvironmentTypeDef",
    "UpdateKxEnvironmentNetworkRequestRequestTypeDef",
    "UpdateKxEnvironmentNetworkResponseTypeDef",
    "UpdateKxEnvironmentResponseTypeDef",
    "ListKxEnvironmentsResponseTypeDef",
)

AutoScalingConfigurationTypeDef = TypedDict(
    "AutoScalingConfigurationTypeDef",
    {
        "minNodeCount": NotRequired[int],
        "maxNodeCount": NotRequired[int],
        "autoScalingMetric": NotRequired[Literal["CPU_UTILIZATION_PERCENTAGE"]],
        "metricTarget": NotRequired[float],
        "scaleInCooldownSeconds": NotRequired[float],
        "scaleOutCooldownSeconds": NotRequired[float],
    },
)

CapacityConfigurationTypeDef = TypedDict(
    "CapacityConfigurationTypeDef",
    {
        "nodeType": NotRequired[str],
        "nodeCount": NotRequired[int],
    },
)

ChangeRequestTypeDef = TypedDict(
    "ChangeRequestTypeDef",
    {
        "changeType": ChangeTypeType,
        "dbPath": str,
        "s3Path": NotRequired[str],
    },
)

CodeConfigurationTypeDef = TypedDict(
    "CodeConfigurationTypeDef",
    {
        "s3Bucket": NotRequired[str],
        "s3Key": NotRequired[str],
        "s3ObjectVersion": NotRequired[str],
    },
)

FederationParametersTypeDef = TypedDict(
    "FederationParametersTypeDef",
    {
        "samlMetadataDocument": NotRequired[str],
        "samlMetadataURL": NotRequired[str],
        "applicationCallBackURL": NotRequired[str],
        "federationURN": NotRequired[str],
        "federationProviderName": NotRequired[str],
        "attributeMap": NotRequired[Mapping[str, str]],
    },
)

SuperuserParametersTypeDef = TypedDict(
    "SuperuserParametersTypeDef",
    {
        "emailAddress": str,
        "firstName": str,
        "lastName": str,
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

ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "errorMessage": NotRequired[str],
        "errorType": NotRequired[ErrorDetailsType],
    },
)

KxCacheStorageConfigurationTypeDef = TypedDict(
    "KxCacheStorageConfigurationTypeDef",
    {
        "type": str,
        "size": int,
    },
)

KxCommandLineArgumentTypeDef = TypedDict(
    "KxCommandLineArgumentTypeDef",
    {
        "key": NotRequired[str],
        "value": NotRequired[str],
    },
)

KxSavedownStorageConfigurationTypeDef = TypedDict(
    "KxSavedownStorageConfigurationTypeDef",
    {
        "type": Literal["SDS01"],
        "size": int,
    },
)

VpcConfigurationTypeDef = TypedDict(
    "VpcConfigurationTypeDef",
    {
        "vpcId": NotRequired[str],
        "securityGroupIds": NotRequired[Sequence[str]],
        "subnetIds": NotRequired[Sequence[str]],
        "ipAddressType": NotRequired[Literal["IP_V4"]],
    },
)

CreateKxDatabaseRequestRequestTypeDef = TypedDict(
    "CreateKxDatabaseRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "clientToken": str,
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

CreateKxEnvironmentRequestRequestTypeDef = TypedDict(
    "CreateKxEnvironmentRequestRequestTypeDef",
    {
        "name": str,
        "kmsKeyId": str,
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "clientToken": NotRequired[str],
    },
)

CreateKxUserRequestRequestTypeDef = TypedDict(
    "CreateKxUserRequestRequestTypeDef",
    {
        "environmentId": str,
        "userName": str,
        "iamRole": str,
        "tags": NotRequired[Mapping[str, str]],
        "clientToken": NotRequired[str],
    },
)

CustomDNSServerTypeDef = TypedDict(
    "CustomDNSServerTypeDef",
    {
        "customDNSServerName": str,
        "customDNSServerIP": str,
    },
)

DeleteEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

DeleteKxClusterRequestRequestTypeDef = TypedDict(
    "DeleteKxClusterRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
        "clientToken": NotRequired[str],
    },
)

DeleteKxDatabaseRequestRequestTypeDef = TypedDict(
    "DeleteKxDatabaseRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "clientToken": str,
    },
)

DeleteKxEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteKxEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

DeleteKxUserRequestRequestTypeDef = TypedDict(
    "DeleteKxUserRequestRequestTypeDef",
    {
        "userName": str,
        "environmentId": str,
    },
)

GetEnvironmentRequestRequestTypeDef = TypedDict(
    "GetEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

GetKxChangesetRequestRequestTypeDef = TypedDict(
    "GetKxChangesetRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "changesetId": str,
    },
)

GetKxClusterRequestRequestTypeDef = TypedDict(
    "GetKxClusterRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
    },
)

GetKxConnectionStringRequestRequestTypeDef = TypedDict(
    "GetKxConnectionStringRequestRequestTypeDef",
    {
        "userArn": str,
        "environmentId": str,
        "clusterName": str,
    },
)

GetKxDatabaseRequestRequestTypeDef = TypedDict(
    "GetKxDatabaseRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
    },
)

GetKxEnvironmentRequestRequestTypeDef = TypedDict(
    "GetKxEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

GetKxUserRequestRequestTypeDef = TypedDict(
    "GetKxUserRequestRequestTypeDef",
    {
        "userName": str,
        "environmentId": str,
    },
)

IcmpTypeCodeTypeDef = TypedDict(
    "IcmpTypeCodeTypeDef",
    {
        "type": int,
        "code": int,
    },
)

KxChangesetListEntryTypeDef = TypedDict(
    "KxChangesetListEntryTypeDef",
    {
        "changesetId": NotRequired[str],
        "createdTimestamp": NotRequired[datetime],
        "activeFromTimestamp": NotRequired[datetime],
        "lastModifiedTimestamp": NotRequired[datetime],
        "status": NotRequired[ChangesetStatusType],
    },
)

KxClusterCodeDeploymentConfigurationTypeDef = TypedDict(
    "KxClusterCodeDeploymentConfigurationTypeDef",
    {
        "deploymentStrategy": KxClusterCodeDeploymentStrategyType,
    },
)

KxClusterTypeDef = TypedDict(
    "KxClusterTypeDef",
    {
        "status": NotRequired[KxClusterStatusType],
        "statusReason": NotRequired[str],
        "clusterName": NotRequired[str],
        "clusterType": NotRequired[KxClusterTypeType],
        "clusterDescription": NotRequired[str],
        "releaseLabel": NotRequired[str],
        "initializationScript": NotRequired[str],
        "executionRole": NotRequired[str],
        "azMode": NotRequired[KxAzModeType],
        "availabilityZoneId": NotRequired[str],
        "lastModifiedTimestamp": NotRequired[datetime],
        "createdTimestamp": NotRequired[datetime],
    },
)

KxDatabaseCacheConfigurationTypeDef = TypedDict(
    "KxDatabaseCacheConfigurationTypeDef",
    {
        "cacheType": str,
        "dbPaths": Sequence[str],
    },
)

KxDatabaseListEntryTypeDef = TypedDict(
    "KxDatabaseListEntryTypeDef",
    {
        "databaseName": NotRequired[str],
        "createdTimestamp": NotRequired[datetime],
        "lastModifiedTimestamp": NotRequired[datetime],
    },
)

KxDeploymentConfigurationTypeDef = TypedDict(
    "KxDeploymentConfigurationTypeDef",
    {
        "deploymentStrategy": KxDeploymentStrategyType,
    },
)

KxNodeTypeDef = TypedDict(
    "KxNodeTypeDef",
    {
        "nodeId": NotRequired[str],
        "availabilityZoneId": NotRequired[str],
        "launchTime": NotRequired[datetime],
    },
)

KxUserTypeDef = TypedDict(
    "KxUserTypeDef",
    {
        "userArn": NotRequired[str],
        "userName": NotRequired[str],
        "iamRole": NotRequired[str],
        "createTimestamp": NotRequired[datetime],
        "updateTimestamp": NotRequired[datetime],
    },
)

ListEnvironmentsRequestRequestTypeDef = TypedDict(
    "ListEnvironmentsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListKxChangesetsRequestRequestTypeDef = TypedDict(
    "ListKxChangesetsRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListKxClusterNodesRequestRequestTypeDef = TypedDict(
    "ListKxClusterNodesRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListKxClustersRequestRequestTypeDef = TypedDict(
    "ListKxClustersRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterType": NotRequired[KxClusterTypeType],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListKxDatabasesRequestRequestTypeDef = TypedDict(
    "ListKxDatabasesRequestRequestTypeDef",
    {
        "environmentId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
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

ListKxEnvironmentsRequestRequestTypeDef = TypedDict(
    "ListKxEnvironmentsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListKxUsersRequestRequestTypeDef = TypedDict(
    "ListKxUsersRequestRequestTypeDef",
    {
        "environmentId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "from": int,
        "to": int,
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

UpdateKxDatabaseRequestRequestTypeDef = TypedDict(
    "UpdateKxDatabaseRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "clientToken": str,
        "description": NotRequired[str],
    },
)

UpdateKxEnvironmentRequestRequestTypeDef = TypedDict(
    "UpdateKxEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)

UpdateKxUserRequestRequestTypeDef = TypedDict(
    "UpdateKxUserRequestRequestTypeDef",
    {
        "environmentId": str,
        "userName": str,
        "iamRole": str,
        "clientToken": NotRequired[str],
    },
)

CreateKxChangesetRequestRequestTypeDef = TypedDict(
    "CreateKxChangesetRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "changeRequests": Sequence[ChangeRequestTypeDef],
        "clientToken": str,
    },
)

EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "name": NotRequired[str],
        "environmentId": NotRequired[str],
        "awsAccountId": NotRequired[str],
        "status": NotRequired[EnvironmentStatusType],
        "environmentUrl": NotRequired[str],
        "description": NotRequired[str],
        "environmentArn": NotRequired[str],
        "sageMakerStudioDomainUrl": NotRequired[str],
        "kmsKeyId": NotRequired[str],
        "dedicatedServiceAccountId": NotRequired[str],
        "federationMode": NotRequired[FederationModeType],
        "federationParameters": NotRequired[FederationParametersTypeDef],
    },
)

UpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "UpdateEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
        "federationMode": NotRequired[FederationModeType],
        "federationParameters": NotRequired[FederationParametersTypeDef],
    },
)

CreateEnvironmentRequestRequestTypeDef = TypedDict(
    "CreateEnvironmentRequestRequestTypeDef",
    {
        "name": str,
        "description": NotRequired[str],
        "kmsKeyId": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "federationMode": NotRequired[FederationModeType],
        "federationParameters": NotRequired[FederationParametersTypeDef],
        "superuserParameters": NotRequired[SuperuserParametersTypeDef],
        "dataBundles": NotRequired[Sequence[str]],
    },
)

CreateEnvironmentResponseTypeDef = TypedDict(
    "CreateEnvironmentResponseTypeDef",
    {
        "environmentId": str,
        "environmentArn": str,
        "environmentUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKxDatabaseResponseTypeDef = TypedDict(
    "CreateKxDatabaseResponseTypeDef",
    {
        "databaseName": str,
        "databaseArn": str,
        "environmentId": str,
        "description": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKxEnvironmentResponseTypeDef = TypedDict(
    "CreateKxEnvironmentResponseTypeDef",
    {
        "name": str,
        "status": EnvironmentStatusType,
        "environmentId": str,
        "description": str,
        "environmentArn": str,
        "kmsKeyId": str,
        "creationTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKxUserResponseTypeDef = TypedDict(
    "CreateKxUserResponseTypeDef",
    {
        "userName": str,
        "userArn": str,
        "environmentId": str,
        "iamRole": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxConnectionStringResponseTypeDef = TypedDict(
    "GetKxConnectionStringResponseTypeDef",
    {
        "signedConnectionString": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxDatabaseResponseTypeDef = TypedDict(
    "GetKxDatabaseResponseTypeDef",
    {
        "databaseName": str,
        "databaseArn": str,
        "environmentId": str,
        "description": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "lastCompletedChangesetId": str,
        "numBytes": int,
        "numChangesets": int,
        "numFiles": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxUserResponseTypeDef = TypedDict(
    "GetKxUserResponseTypeDef",
    {
        "userName": str,
        "userArn": str,
        "environmentId": str,
        "iamRole": str,
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

UpdateKxDatabaseResponseTypeDef = TypedDict(
    "UpdateKxDatabaseResponseTypeDef",
    {
        "databaseName": str,
        "environmentId": str,
        "description": str,
        "lastModifiedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateKxUserResponseTypeDef = TypedDict(
    "UpdateKxUserResponseTypeDef",
    {
        "userName": str,
        "userArn": str,
        "environmentId": str,
        "iamRole": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKxChangesetResponseTypeDef = TypedDict(
    "CreateKxChangesetResponseTypeDef",
    {
        "changesetId": str,
        "databaseName": str,
        "environmentId": str,
        "changeRequests": List[ChangeRequestTypeDef],
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "status": ChangesetStatusType,
        "errorInfo": ErrorInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxChangesetResponseTypeDef = TypedDict(
    "GetKxChangesetResponseTypeDef",
    {
        "changesetId": str,
        "databaseName": str,
        "environmentId": str,
        "changeRequests": List[ChangeRequestTypeDef],
        "createdTimestamp": datetime,
        "activeFromTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "status": ChangesetStatusType,
        "errorInfo": ErrorInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxChangesetsResponseTypeDef = TypedDict(
    "ListKxChangesetsResponseTypeDef",
    {
        "kxChangesets": List[KxChangesetListEntryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateKxClusterCodeConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateKxClusterCodeConfigurationRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
        "code": CodeConfigurationTypeDef,
        "clientToken": NotRequired[str],
        "initializationScript": NotRequired[str],
        "commandLineArguments": NotRequired[Sequence[KxCommandLineArgumentTypeDef]],
        "deploymentConfiguration": NotRequired[KxClusterCodeDeploymentConfigurationTypeDef],
    },
)

ListKxClustersResponseTypeDef = TypedDict(
    "ListKxClustersResponseTypeDef",
    {
        "kxClusterSummaries": List[KxClusterTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

KxDatabaseConfigurationTypeDef = TypedDict(
    "KxDatabaseConfigurationTypeDef",
    {
        "databaseName": str,
        "cacheConfigurations": NotRequired[Sequence[KxDatabaseCacheConfigurationTypeDef]],
        "changesetId": NotRequired[str],
    },
)

ListKxDatabasesResponseTypeDef = TypedDict(
    "ListKxDatabasesResponseTypeDef",
    {
        "kxDatabases": List[KxDatabaseListEntryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxClusterNodesResponseTypeDef = TypedDict(
    "ListKxClusterNodesResponseTypeDef",
    {
        "nodes": List[KxNodeTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxUsersResponseTypeDef = TypedDict(
    "ListKxUsersResponseTypeDef",
    {
        "users": List[KxUserTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef = TypedDict(
    "ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

NetworkACLEntryTypeDef = TypedDict(
    "NetworkACLEntryTypeDef",
    {
        "ruleNumber": int,
        "protocol": str,
        "ruleAction": RuleActionType,
        "cidrBlock": str,
        "portRange": NotRequired[PortRangeTypeDef],
        "icmpTypeCode": NotRequired[IcmpTypeCodeTypeDef],
    },
)

GetEnvironmentResponseTypeDef = TypedDict(
    "GetEnvironmentResponseTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentsResponseTypeDef = TypedDict(
    "ListEnvironmentsResponseTypeDef",
    {
        "environments": List[EnvironmentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEnvironmentResponseTypeDef = TypedDict(
    "UpdateEnvironmentResponseTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKxClusterRequestRequestTypeDef = TypedDict(
    "CreateKxClusterRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
        "clusterType": KxClusterTypeType,
        "capacityConfiguration": CapacityConfigurationTypeDef,
        "releaseLabel": str,
        "azMode": KxAzModeType,
        "clientToken": NotRequired[str],
        "databases": NotRequired[Sequence[KxDatabaseConfigurationTypeDef]],
        "cacheStorageConfigurations": NotRequired[Sequence[KxCacheStorageConfigurationTypeDef]],
        "autoScalingConfiguration": NotRequired[AutoScalingConfigurationTypeDef],
        "clusterDescription": NotRequired[str],
        "vpcConfiguration": NotRequired[VpcConfigurationTypeDef],
        "initializationScript": NotRequired[str],
        "commandLineArguments": NotRequired[Sequence[KxCommandLineArgumentTypeDef]],
        "code": NotRequired[CodeConfigurationTypeDef],
        "executionRole": NotRequired[str],
        "savedownStorageConfiguration": NotRequired[KxSavedownStorageConfigurationTypeDef],
        "availabilityZoneId": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

CreateKxClusterResponseTypeDef = TypedDict(
    "CreateKxClusterResponseTypeDef",
    {
        "environmentId": str,
        "status": KxClusterStatusType,
        "statusReason": str,
        "clusterName": str,
        "clusterType": KxClusterTypeType,
        "databases": List[KxDatabaseConfigurationTypeDef],
        "cacheStorageConfigurations": List[KxCacheStorageConfigurationTypeDef],
        "autoScalingConfiguration": AutoScalingConfigurationTypeDef,
        "clusterDescription": str,
        "capacityConfiguration": CapacityConfigurationTypeDef,
        "releaseLabel": str,
        "vpcConfiguration": VpcConfigurationTypeDef,
        "initializationScript": str,
        "commandLineArguments": List[KxCommandLineArgumentTypeDef],
        "code": CodeConfigurationTypeDef,
        "executionRole": str,
        "lastModifiedTimestamp": datetime,
        "savedownStorageConfiguration": KxSavedownStorageConfigurationTypeDef,
        "azMode": KxAzModeType,
        "availabilityZoneId": str,
        "createdTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxClusterResponseTypeDef = TypedDict(
    "GetKxClusterResponseTypeDef",
    {
        "status": KxClusterStatusType,
        "statusReason": str,
        "clusterName": str,
        "clusterType": KxClusterTypeType,
        "databases": List[KxDatabaseConfigurationTypeDef],
        "cacheStorageConfigurations": List[KxCacheStorageConfigurationTypeDef],
        "autoScalingConfiguration": AutoScalingConfigurationTypeDef,
        "clusterDescription": str,
        "capacityConfiguration": CapacityConfigurationTypeDef,
        "releaseLabel": str,
        "vpcConfiguration": VpcConfigurationTypeDef,
        "initializationScript": str,
        "commandLineArguments": List[KxCommandLineArgumentTypeDef],
        "code": CodeConfigurationTypeDef,
        "executionRole": str,
        "lastModifiedTimestamp": datetime,
        "savedownStorageConfiguration": KxSavedownStorageConfigurationTypeDef,
        "azMode": KxAzModeType,
        "availabilityZoneId": str,
        "createdTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateKxClusterDatabasesRequestRequestTypeDef = TypedDict(
    "UpdateKxClusterDatabasesRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
        "databases": Sequence[KxDatabaseConfigurationTypeDef],
        "clientToken": NotRequired[str],
        "deploymentConfiguration": NotRequired[KxDeploymentConfigurationTypeDef],
    },
)

TransitGatewayConfigurationTypeDef = TypedDict(
    "TransitGatewayConfigurationTypeDef",
    {
        "transitGatewayID": str,
        "routableCIDRSpace": str,
        "attachmentNetworkAclConfiguration": NotRequired[List[NetworkACLEntryTypeDef]],
    },
)

GetKxEnvironmentResponseTypeDef = TypedDict(
    "GetKxEnvironmentResponseTypeDef",
    {
        "name": str,
        "environmentId": str,
        "awsAccountId": str,
        "status": EnvironmentStatusType,
        "tgwStatus": tgwStatusType,
        "dnsStatus": dnsStatusType,
        "errorMessage": str,
        "description": str,
        "environmentArn": str,
        "kmsKeyId": str,
        "dedicatedServiceAccountId": str,
        "transitGatewayConfiguration": TransitGatewayConfigurationTypeDef,
        "customDNSConfiguration": List[CustomDNSServerTypeDef],
        "creationTimestamp": datetime,
        "updateTimestamp": datetime,
        "availabilityZoneIds": List[str],
        "certificateAuthorityArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

KxEnvironmentTypeDef = TypedDict(
    "KxEnvironmentTypeDef",
    {
        "name": NotRequired[str],
        "environmentId": NotRequired[str],
        "awsAccountId": NotRequired[str],
        "status": NotRequired[EnvironmentStatusType],
        "tgwStatus": NotRequired[tgwStatusType],
        "dnsStatus": NotRequired[dnsStatusType],
        "errorMessage": NotRequired[str],
        "description": NotRequired[str],
        "environmentArn": NotRequired[str],
        "kmsKeyId": NotRequired[str],
        "dedicatedServiceAccountId": NotRequired[str],
        "transitGatewayConfiguration": NotRequired[TransitGatewayConfigurationTypeDef],
        "customDNSConfiguration": NotRequired[List[CustomDNSServerTypeDef]],
        "creationTimestamp": NotRequired[datetime],
        "updateTimestamp": NotRequired[datetime],
        "availabilityZoneIds": NotRequired[List[str]],
        "certificateAuthorityArn": NotRequired[str],
    },
)

UpdateKxEnvironmentNetworkRequestRequestTypeDef = TypedDict(
    "UpdateKxEnvironmentNetworkRequestRequestTypeDef",
    {
        "environmentId": str,
        "transitGatewayConfiguration": NotRequired[TransitGatewayConfigurationTypeDef],
        "customDNSConfiguration": NotRequired[Sequence[CustomDNSServerTypeDef]],
        "clientToken": NotRequired[str],
    },
)

UpdateKxEnvironmentNetworkResponseTypeDef = TypedDict(
    "UpdateKxEnvironmentNetworkResponseTypeDef",
    {
        "name": str,
        "environmentId": str,
        "awsAccountId": str,
        "status": EnvironmentStatusType,
        "tgwStatus": tgwStatusType,
        "dnsStatus": dnsStatusType,
        "errorMessage": str,
        "description": str,
        "environmentArn": str,
        "kmsKeyId": str,
        "dedicatedServiceAccountId": str,
        "transitGatewayConfiguration": TransitGatewayConfigurationTypeDef,
        "customDNSConfiguration": List[CustomDNSServerTypeDef],
        "creationTimestamp": datetime,
        "updateTimestamp": datetime,
        "availabilityZoneIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateKxEnvironmentResponseTypeDef = TypedDict(
    "UpdateKxEnvironmentResponseTypeDef",
    {
        "name": str,
        "environmentId": str,
        "awsAccountId": str,
        "status": EnvironmentStatusType,
        "tgwStatus": tgwStatusType,
        "dnsStatus": dnsStatusType,
        "errorMessage": str,
        "description": str,
        "environmentArn": str,
        "kmsKeyId": str,
        "dedicatedServiceAccountId": str,
        "transitGatewayConfiguration": TransitGatewayConfigurationTypeDef,
        "customDNSConfiguration": List[CustomDNSServerTypeDef],
        "creationTimestamp": datetime,
        "updateTimestamp": datetime,
        "availabilityZoneIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxEnvironmentsResponseTypeDef = TypedDict(
    "ListKxEnvironmentsResponseTypeDef",
    {
        "environments": List[KxEnvironmentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
