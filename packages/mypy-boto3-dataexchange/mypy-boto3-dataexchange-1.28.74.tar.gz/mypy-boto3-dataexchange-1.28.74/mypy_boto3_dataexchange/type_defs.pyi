"""
Type annotations for dataexchange service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/type_defs/)

Usage::

    ```python
    from mypy_boto3_dataexchange.type_defs import ApiGatewayApiAssetTypeDef

    data: ApiGatewayApiAssetTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AssetTypeType,
    CodeType,
    JobErrorLimitNameType,
    JobErrorResourceTypesType,
    LFPermissionType,
    LFResourceTypeType,
    NotificationTypeType,
    OriginType,
    SchemaChangeTypeType,
    ServerSideEncryptionTypesType,
    StateType,
    TableTagPolicyLFPermissionType,
    TypeType,
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
    "ApiGatewayApiAssetTypeDef",
    "AssetDestinationEntryTypeDef",
    "RedshiftDataShareAssetTypeDef",
    "S3SnapshotAssetTypeDef",
    "AssetSourceEntryTypeDef",
    "AutoExportRevisionDestinationEntryTypeDef",
    "ExportServerSideEncryptionTypeDef",
    "CancelJobRequestRequestTypeDef",
    "CreateDataSetRequestRequestTypeDef",
    "OriginDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "CreateRevisionRequestRequestTypeDef",
    "TimestampTypeDef",
    "LFTagPaginatorTypeDef",
    "LFTagTypeDef",
    "DeleteAssetRequestRequestTypeDef",
    "DeleteDataSetRequestRequestTypeDef",
    "DeleteEventActionRequestRequestTypeDef",
    "DeleteRevisionRequestRequestTypeDef",
    "ImportAssetFromSignedUrlJobErrorDetailsTypeDef",
    "RevisionPublishedTypeDef",
    "ExportAssetToSignedUrlRequestDetailsTypeDef",
    "ExportAssetToSignedUrlResponseDetailsTypeDef",
    "RevisionDestinationEntryTypeDef",
    "GetAssetRequestRequestTypeDef",
    "GetDataSetRequestRequestTypeDef",
    "GetEventActionRequestRequestTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetRevisionRequestRequestTypeDef",
    "ImportAssetFromApiGatewayApiRequestDetailsTypeDef",
    "ImportAssetFromApiGatewayApiResponseDetailsTypeDef",
    "ImportAssetFromSignedUrlRequestDetailsTypeDef",
    "ImportAssetFromSignedUrlResponseDetailsTypeDef",
    "RedshiftDataShareAssetSourceEntryTypeDef",
    "KmsKeyToGrantTypeDef",
    "LakeFormationTagPolicyDetailsTypeDef",
    "PaginatorConfigTypeDef",
    "ListDataSetRevisionsRequestRequestTypeDef",
    "RevisionEntryTypeDef",
    "ListDataSetsRequestRequestTypeDef",
    "ListEventActionsRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListRevisionAssetsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RedshiftDataShareDetailsTypeDef",
    "RevokeRevisionRequestRequestTypeDef",
    "S3DataAccessDetailsTypeDef",
    "SchemaChangeDetailsTypeDef",
    "SendApiAssetRequestRequestTypeDef",
    "StartJobRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAssetRequestRequestTypeDef",
    "UpdateDataSetRequestRequestTypeDef",
    "UpdateRevisionRequestRequestTypeDef",
    "ImportAssetsFromS3RequestDetailsTypeDef",
    "ImportAssetsFromS3ResponseDetailsTypeDef",
    "AutoExportRevisionToS3RequestDetailsTypeDef",
    "ExportAssetsToS3RequestDetailsTypeDef",
    "ExportAssetsToS3ResponseDetailsTypeDef",
    "DataSetEntryTypeDef",
    "CreateDataSetResponseTypeDef",
    "CreateRevisionResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetDataSetResponseTypeDef",
    "GetRevisionResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "RevokeRevisionResponseTypeDef",
    "SendApiAssetResponseTypeDef",
    "UpdateDataSetResponseTypeDef",
    "UpdateRevisionResponseTypeDef",
    "DataUpdateRequestDetailsTypeDef",
    "DeprecationRequestDetailsTypeDef",
    "DatabaseLFTagPolicyAndPermissionsPaginatorTypeDef",
    "DatabaseLFTagPolicyPaginatorTypeDef",
    "TableLFTagPolicyAndPermissionsPaginatorTypeDef",
    "TableLFTagPolicyPaginatorTypeDef",
    "DatabaseLFTagPolicyAndPermissionsTypeDef",
    "DatabaseLFTagPolicyTypeDef",
    "TableLFTagPolicyAndPermissionsTypeDef",
    "TableLFTagPolicyTypeDef",
    "DetailsTypeDef",
    "EventTypeDef",
    "ExportRevisionsToS3RequestDetailsTypeDef",
    "ExportRevisionsToS3ResponseDetailsTypeDef",
    "ImportAssetsFromRedshiftDataSharesRequestDetailsTypeDef",
    "ImportAssetsFromRedshiftDataSharesResponseDetailsTypeDef",
    "S3DataAccessAssetSourceEntryPaginatorTypeDef",
    "S3DataAccessAssetSourceEntryTypeDef",
    "S3DataAccessAssetTypeDef",
    "ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef",
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    "ListEventActionsRequestListEventActionsPaginateTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef",
    "ListDataSetRevisionsResponseTypeDef",
    "ScopeDetailsTypeDef",
    "SchemaChangeRequestDetailsTypeDef",
    "ActionTypeDef",
    "ListDataSetsResponseTypeDef",
    "ImportAssetsFromLakeFormationTagPolicyResponseDetailsPaginatorTypeDef",
    "LFResourceDetailsPaginatorTypeDef",
    "ImportAssetsFromLakeFormationTagPolicyRequestDetailsTypeDef",
    "ImportAssetsFromLakeFormationTagPolicyResponseDetailsTypeDef",
    "LFResourceDetailsTypeDef",
    "JobErrorTypeDef",
    "CreateS3DataAccessFromS3BucketResponseDetailsPaginatorTypeDef",
    "CreateS3DataAccessFromS3BucketRequestDetailsTypeDef",
    "CreateS3DataAccessFromS3BucketResponseDetailsTypeDef",
    "NotificationDetailsTypeDef",
    "CreateEventActionRequestRequestTypeDef",
    "CreateEventActionResponseTypeDef",
    "EventActionEntryTypeDef",
    "GetEventActionResponseTypeDef",
    "UpdateEventActionRequestRequestTypeDef",
    "UpdateEventActionResponseTypeDef",
    "LFTagPolicyDetailsPaginatorTypeDef",
    "LFTagPolicyDetailsTypeDef",
    "ResponseDetailsPaginatorTypeDef",
    "RequestDetailsTypeDef",
    "ResponseDetailsTypeDef",
    "SendDataSetNotificationRequestRequestTypeDef",
    "ListEventActionsResponseTypeDef",
    "LakeFormationDataPermissionDetailsPaginatorTypeDef",
    "LakeFormationDataPermissionDetailsTypeDef",
    "JobEntryPaginatorTypeDef",
    "CreateJobRequestRequestTypeDef",
    "CreateJobResponseTypeDef",
    "GetJobResponseTypeDef",
    "JobEntryTypeDef",
    "LakeFormationDataPermissionAssetPaginatorTypeDef",
    "LakeFormationDataPermissionAssetTypeDef",
    "ListJobsResponsePaginatorTypeDef",
    "ListJobsResponseTypeDef",
    "AssetDetailsPaginatorTypeDef",
    "AssetDetailsTypeDef",
    "AssetEntryPaginatorTypeDef",
    "AssetEntryTypeDef",
    "GetAssetResponseTypeDef",
    "UpdateAssetResponseTypeDef",
    "ListRevisionAssetsResponsePaginatorTypeDef",
    "ListRevisionAssetsResponseTypeDef",
)

ApiGatewayApiAssetTypeDef = TypedDict(
    "ApiGatewayApiAssetTypeDef",
    {
        "ApiDescription": NotRequired[str],
        "ApiEndpoint": NotRequired[str],
        "ApiId": NotRequired[str],
        "ApiKey": NotRequired[str],
        "ApiName": NotRequired[str],
        "ApiSpecificationDownloadUrl": NotRequired[str],
        "ApiSpecificationDownloadUrlExpiresAt": NotRequired[datetime],
        "ProtocolType": NotRequired[Literal["REST"]],
        "Stage": NotRequired[str],
    },
)

AssetDestinationEntryTypeDef = TypedDict(
    "AssetDestinationEntryTypeDef",
    {
        "AssetId": str,
        "Bucket": str,
        "Key": NotRequired[str],
    },
)

RedshiftDataShareAssetTypeDef = TypedDict(
    "RedshiftDataShareAssetTypeDef",
    {
        "Arn": str,
    },
)

S3SnapshotAssetTypeDef = TypedDict(
    "S3SnapshotAssetTypeDef",
    {
        "Size": float,
    },
)

AssetSourceEntryTypeDef = TypedDict(
    "AssetSourceEntryTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)

AutoExportRevisionDestinationEntryTypeDef = TypedDict(
    "AutoExportRevisionDestinationEntryTypeDef",
    {
        "Bucket": str,
        "KeyPattern": NotRequired[str],
    },
)

ExportServerSideEncryptionTypeDef = TypedDict(
    "ExportServerSideEncryptionTypeDef",
    {
        "Type": ServerSideEncryptionTypesType,
        "KmsKeyArn": NotRequired[str],
    },
)

CancelJobRequestRequestTypeDef = TypedDict(
    "CancelJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

CreateDataSetRequestRequestTypeDef = TypedDict(
    "CreateDataSetRequestRequestTypeDef",
    {
        "AssetType": AssetTypeType,
        "Description": str,
        "Name": str,
        "Tags": NotRequired[Mapping[str, str]],
    },
)

OriginDetailsTypeDef = TypedDict(
    "OriginDetailsTypeDef",
    {
        "ProductId": str,
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

CreateRevisionRequestRequestTypeDef = TypedDict(
    "CreateRevisionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "Comment": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)

TimestampTypeDef = Union[datetime, str]
LFTagPaginatorTypeDef = TypedDict(
    "LFTagPaginatorTypeDef",
    {
        "TagKey": str,
        "TagValues": List[str],
    },
)

LFTagTypeDef = TypedDict(
    "LFTagTypeDef",
    {
        "TagKey": str,
        "TagValues": Sequence[str],
    },
)

DeleteAssetRequestRequestTypeDef = TypedDict(
    "DeleteAssetRequestRequestTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "RevisionId": str,
    },
)

DeleteDataSetRequestRequestTypeDef = TypedDict(
    "DeleteDataSetRequestRequestTypeDef",
    {
        "DataSetId": str,
    },
)

DeleteEventActionRequestRequestTypeDef = TypedDict(
    "DeleteEventActionRequestRequestTypeDef",
    {
        "EventActionId": str,
    },
)

DeleteRevisionRequestRequestTypeDef = TypedDict(
    "DeleteRevisionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
    },
)

ImportAssetFromSignedUrlJobErrorDetailsTypeDef = TypedDict(
    "ImportAssetFromSignedUrlJobErrorDetailsTypeDef",
    {
        "AssetName": str,
    },
)

RevisionPublishedTypeDef = TypedDict(
    "RevisionPublishedTypeDef",
    {
        "DataSetId": str,
    },
)

ExportAssetToSignedUrlRequestDetailsTypeDef = TypedDict(
    "ExportAssetToSignedUrlRequestDetailsTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "RevisionId": str,
    },
)

ExportAssetToSignedUrlResponseDetailsTypeDef = TypedDict(
    "ExportAssetToSignedUrlResponseDetailsTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "RevisionId": str,
        "SignedUrl": NotRequired[str],
        "SignedUrlExpiresAt": NotRequired[datetime],
    },
)

RevisionDestinationEntryTypeDef = TypedDict(
    "RevisionDestinationEntryTypeDef",
    {
        "Bucket": str,
        "RevisionId": str,
        "KeyPattern": NotRequired[str],
    },
)

GetAssetRequestRequestTypeDef = TypedDict(
    "GetAssetRequestRequestTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "RevisionId": str,
    },
)

GetDataSetRequestRequestTypeDef = TypedDict(
    "GetDataSetRequestRequestTypeDef",
    {
        "DataSetId": str,
    },
)

GetEventActionRequestRequestTypeDef = TypedDict(
    "GetEventActionRequestRequestTypeDef",
    {
        "EventActionId": str,
    },
)

GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

GetRevisionRequestRequestTypeDef = TypedDict(
    "GetRevisionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
    },
)

ImportAssetFromApiGatewayApiRequestDetailsTypeDef = TypedDict(
    "ImportAssetFromApiGatewayApiRequestDetailsTypeDef",
    {
        "ApiId": str,
        "ApiName": str,
        "ApiSpecificationMd5Hash": str,
        "DataSetId": str,
        "ProtocolType": Literal["REST"],
        "RevisionId": str,
        "Stage": str,
        "ApiDescription": NotRequired[str],
        "ApiKey": NotRequired[str],
    },
)

ImportAssetFromApiGatewayApiResponseDetailsTypeDef = TypedDict(
    "ImportAssetFromApiGatewayApiResponseDetailsTypeDef",
    {
        "ApiId": str,
        "ApiName": str,
        "ApiSpecificationMd5Hash": str,
        "ApiSpecificationUploadUrl": str,
        "ApiSpecificationUploadUrlExpiresAt": datetime,
        "DataSetId": str,
        "ProtocolType": Literal["REST"],
        "RevisionId": str,
        "Stage": str,
        "ApiDescription": NotRequired[str],
        "ApiKey": NotRequired[str],
    },
)

ImportAssetFromSignedUrlRequestDetailsTypeDef = TypedDict(
    "ImportAssetFromSignedUrlRequestDetailsTypeDef",
    {
        "AssetName": str,
        "DataSetId": str,
        "Md5Hash": str,
        "RevisionId": str,
    },
)

ImportAssetFromSignedUrlResponseDetailsTypeDef = TypedDict(
    "ImportAssetFromSignedUrlResponseDetailsTypeDef",
    {
        "AssetName": str,
        "DataSetId": str,
        "RevisionId": str,
        "Md5Hash": NotRequired[str],
        "SignedUrl": NotRequired[str],
        "SignedUrlExpiresAt": NotRequired[datetime],
    },
)

RedshiftDataShareAssetSourceEntryTypeDef = TypedDict(
    "RedshiftDataShareAssetSourceEntryTypeDef",
    {
        "DataShareArn": str,
    },
)

KmsKeyToGrantTypeDef = TypedDict(
    "KmsKeyToGrantTypeDef",
    {
        "KmsKeyArn": str,
    },
)

LakeFormationTagPolicyDetailsTypeDef = TypedDict(
    "LakeFormationTagPolicyDetailsTypeDef",
    {
        "Database": NotRequired[str],
        "Table": NotRequired[str],
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

ListDataSetRevisionsRequestRequestTypeDef = TypedDict(
    "ListDataSetRevisionsRequestRequestTypeDef",
    {
        "DataSetId": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

RevisionEntryTypeDef = TypedDict(
    "RevisionEntryTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "UpdatedAt": datetime,
        "Comment": NotRequired[str],
        "Finalized": NotRequired[bool],
        "SourceId": NotRequired[str],
        "RevocationComment": NotRequired[str],
        "Revoked": NotRequired[bool],
        "RevokedAt": NotRequired[datetime],
    },
)

ListDataSetsRequestRequestTypeDef = TypedDict(
    "ListDataSetsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "Origin": NotRequired[str],
    },
)

ListEventActionsRequestRequestTypeDef = TypedDict(
    "ListEventActionsRequestRequestTypeDef",
    {
        "EventSourceId": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "DataSetId": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "RevisionId": NotRequired[str],
    },
)

ListRevisionAssetsRequestRequestTypeDef = TypedDict(
    "ListRevisionAssetsRequestRequestTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

RedshiftDataShareDetailsTypeDef = TypedDict(
    "RedshiftDataShareDetailsTypeDef",
    {
        "Arn": str,
        "Database": str,
        "Function": NotRequired[str],
        "Table": NotRequired[str],
        "Schema": NotRequired[str],
        "View": NotRequired[str],
    },
)

RevokeRevisionRequestRequestTypeDef = TypedDict(
    "RevokeRevisionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
        "RevocationComment": str,
    },
)

S3DataAccessDetailsTypeDef = TypedDict(
    "S3DataAccessDetailsTypeDef",
    {
        "KeyPrefixes": NotRequired[Sequence[str]],
        "Keys": NotRequired[Sequence[str]],
    },
)

SchemaChangeDetailsTypeDef = TypedDict(
    "SchemaChangeDetailsTypeDef",
    {
        "Name": str,
        "Type": SchemaChangeTypeType,
        "Description": NotRequired[str],
    },
)

SendApiAssetRequestRequestTypeDef = TypedDict(
    "SendApiAssetRequestRequestTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "RevisionId": str,
        "Body": NotRequired[str],
        "QueryStringParameters": NotRequired[Mapping[str, str]],
        "RequestHeaders": NotRequired[Mapping[str, str]],
        "Method": NotRequired[str],
        "Path": NotRequired[str],
    },
)

StartJobRequestRequestTypeDef = TypedDict(
    "StartJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateAssetRequestRequestTypeDef = TypedDict(
    "UpdateAssetRequestRequestTypeDef",
    {
        "AssetId": str,
        "DataSetId": str,
        "Name": str,
        "RevisionId": str,
    },
)

UpdateDataSetRequestRequestTypeDef = TypedDict(
    "UpdateDataSetRequestRequestTypeDef",
    {
        "DataSetId": str,
        "Description": NotRequired[str],
        "Name": NotRequired[str],
    },
)

UpdateRevisionRequestRequestTypeDef = TypedDict(
    "UpdateRevisionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
        "Comment": NotRequired[str],
        "Finalized": NotRequired[bool],
    },
)

ImportAssetsFromS3RequestDetailsTypeDef = TypedDict(
    "ImportAssetsFromS3RequestDetailsTypeDef",
    {
        "AssetSources": Sequence[AssetSourceEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
    },
)

ImportAssetsFromS3ResponseDetailsTypeDef = TypedDict(
    "ImportAssetsFromS3ResponseDetailsTypeDef",
    {
        "AssetSources": List[AssetSourceEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
    },
)

AutoExportRevisionToS3RequestDetailsTypeDef = TypedDict(
    "AutoExportRevisionToS3RequestDetailsTypeDef",
    {
        "RevisionDestination": AutoExportRevisionDestinationEntryTypeDef,
        "Encryption": NotRequired[ExportServerSideEncryptionTypeDef],
    },
)

ExportAssetsToS3RequestDetailsTypeDef = TypedDict(
    "ExportAssetsToS3RequestDetailsTypeDef",
    {
        "AssetDestinations": Sequence[AssetDestinationEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
        "Encryption": NotRequired[ExportServerSideEncryptionTypeDef],
    },
)

ExportAssetsToS3ResponseDetailsTypeDef = TypedDict(
    "ExportAssetsToS3ResponseDetailsTypeDef",
    {
        "AssetDestinations": List[AssetDestinationEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
        "Encryption": NotRequired[ExportServerSideEncryptionTypeDef],
    },
)

DataSetEntryTypeDef = TypedDict(
    "DataSetEntryTypeDef",
    {
        "Arn": str,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": OriginType,
        "UpdatedAt": datetime,
        "OriginDetails": NotRequired[OriginDetailsTypeDef],
        "SourceId": NotRequired[str],
    },
)

CreateDataSetResponseTypeDef = TypedDict(
    "CreateDataSetResponseTypeDef",
    {
        "Arn": str,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": OriginType,
        "OriginDetails": OriginDetailsTypeDef,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRevisionResponseTypeDef = TypedDict(
    "CreateRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
        "RevocationComment": str,
        "Revoked": bool,
        "RevokedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDataSetResponseTypeDef = TypedDict(
    "GetDataSetResponseTypeDef",
    {
        "Arn": str,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": OriginType,
        "OriginDetails": OriginDetailsTypeDef,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRevisionResponseTypeDef = TypedDict(
    "GetRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "Tags": Dict[str, str],
        "UpdatedAt": datetime,
        "RevocationComment": str,
        "Revoked": bool,
        "RevokedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RevokeRevisionResponseTypeDef = TypedDict(
    "RevokeRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "UpdatedAt": datetime,
        "RevocationComment": str,
        "Revoked": bool,
        "RevokedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SendApiAssetResponseTypeDef = TypedDict(
    "SendApiAssetResponseTypeDef",
    {
        "Body": str,
        "ResponseHeaders": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSetResponseTypeDef = TypedDict(
    "UpdateDataSetResponseTypeDef",
    {
        "Arn": str,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "Description": str,
        "Id": str,
        "Name": str,
        "Origin": OriginType,
        "OriginDetails": OriginDetailsTypeDef,
        "SourceId": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRevisionResponseTypeDef = TypedDict(
    "UpdateRevisionResponseTypeDef",
    {
        "Arn": str,
        "Comment": str,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Finalized": bool,
        "Id": str,
        "SourceId": str,
        "UpdatedAt": datetime,
        "RevocationComment": str,
        "Revoked": bool,
        "RevokedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataUpdateRequestDetailsTypeDef = TypedDict(
    "DataUpdateRequestDetailsTypeDef",
    {
        "DataUpdatedAt": NotRequired[TimestampTypeDef],
    },
)

DeprecationRequestDetailsTypeDef = TypedDict(
    "DeprecationRequestDetailsTypeDef",
    {
        "DeprecationAt": TimestampTypeDef,
    },
)

DatabaseLFTagPolicyAndPermissionsPaginatorTypeDef = TypedDict(
    "DatabaseLFTagPolicyAndPermissionsPaginatorTypeDef",
    {
        "Expression": List[LFTagPaginatorTypeDef],
        "Permissions": List[Literal["DESCRIBE"]],
    },
)

DatabaseLFTagPolicyPaginatorTypeDef = TypedDict(
    "DatabaseLFTagPolicyPaginatorTypeDef",
    {
        "Expression": List[LFTagPaginatorTypeDef],
    },
)

TableLFTagPolicyAndPermissionsPaginatorTypeDef = TypedDict(
    "TableLFTagPolicyAndPermissionsPaginatorTypeDef",
    {
        "Expression": List[LFTagPaginatorTypeDef],
        "Permissions": List[TableTagPolicyLFPermissionType],
    },
)

TableLFTagPolicyPaginatorTypeDef = TypedDict(
    "TableLFTagPolicyPaginatorTypeDef",
    {
        "Expression": List[LFTagPaginatorTypeDef],
    },
)

DatabaseLFTagPolicyAndPermissionsTypeDef = TypedDict(
    "DatabaseLFTagPolicyAndPermissionsTypeDef",
    {
        "Expression": Sequence[LFTagTypeDef],
        "Permissions": Sequence[Literal["DESCRIBE"]],
    },
)

DatabaseLFTagPolicyTypeDef = TypedDict(
    "DatabaseLFTagPolicyTypeDef",
    {
        "Expression": List[LFTagTypeDef],
    },
)

TableLFTagPolicyAndPermissionsTypeDef = TypedDict(
    "TableLFTagPolicyAndPermissionsTypeDef",
    {
        "Expression": Sequence[LFTagTypeDef],
        "Permissions": Sequence[TableTagPolicyLFPermissionType],
    },
)

TableLFTagPolicyTypeDef = TypedDict(
    "TableLFTagPolicyTypeDef",
    {
        "Expression": List[LFTagTypeDef],
    },
)

DetailsTypeDef = TypedDict(
    "DetailsTypeDef",
    {
        "ImportAssetFromSignedUrlJobErrorDetails": NotRequired[
            ImportAssetFromSignedUrlJobErrorDetailsTypeDef
        ],
        "ImportAssetsFromS3JobErrorDetails": NotRequired[List[AssetSourceEntryTypeDef]],
    },
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "RevisionPublished": NotRequired[RevisionPublishedTypeDef],
    },
)

ExportRevisionsToS3RequestDetailsTypeDef = TypedDict(
    "ExportRevisionsToS3RequestDetailsTypeDef",
    {
        "DataSetId": str,
        "RevisionDestinations": Sequence[RevisionDestinationEntryTypeDef],
        "Encryption": NotRequired[ExportServerSideEncryptionTypeDef],
    },
)

ExportRevisionsToS3ResponseDetailsTypeDef = TypedDict(
    "ExportRevisionsToS3ResponseDetailsTypeDef",
    {
        "DataSetId": str,
        "RevisionDestinations": List[RevisionDestinationEntryTypeDef],
        "Encryption": NotRequired[ExportServerSideEncryptionTypeDef],
        "EventActionArn": NotRequired[str],
    },
)

ImportAssetsFromRedshiftDataSharesRequestDetailsTypeDef = TypedDict(
    "ImportAssetsFromRedshiftDataSharesRequestDetailsTypeDef",
    {
        "AssetSources": Sequence[RedshiftDataShareAssetSourceEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
    },
)

ImportAssetsFromRedshiftDataSharesResponseDetailsTypeDef = TypedDict(
    "ImportAssetsFromRedshiftDataSharesResponseDetailsTypeDef",
    {
        "AssetSources": List[RedshiftDataShareAssetSourceEntryTypeDef],
        "DataSetId": str,
        "RevisionId": str,
    },
)

S3DataAccessAssetSourceEntryPaginatorTypeDef = TypedDict(
    "S3DataAccessAssetSourceEntryPaginatorTypeDef",
    {
        "Bucket": str,
        "KeyPrefixes": NotRequired[List[str]],
        "Keys": NotRequired[List[str]],
        "KmsKeysToGrant": NotRequired[List[KmsKeyToGrantTypeDef]],
    },
)

S3DataAccessAssetSourceEntryTypeDef = TypedDict(
    "S3DataAccessAssetSourceEntryTypeDef",
    {
        "Bucket": str,
        "KeyPrefixes": NotRequired[Sequence[str]],
        "Keys": NotRequired[Sequence[str]],
        "KmsKeysToGrant": NotRequired[Sequence[KmsKeyToGrantTypeDef]],
    },
)

S3DataAccessAssetTypeDef = TypedDict(
    "S3DataAccessAssetTypeDef",
    {
        "Bucket": str,
        "KeyPrefixes": NotRequired[List[str]],
        "Keys": NotRequired[List[str]],
        "S3AccessPointAlias": NotRequired[str],
        "S3AccessPointArn": NotRequired[str],
        "KmsKeysToGrant": NotRequired[List[KmsKeyToGrantTypeDef]],
    },
)

ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef = TypedDict(
    "ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef",
    {
        "DataSetId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDataSetsRequestListDataSetsPaginateTypeDef = TypedDict(
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    {
        "Origin": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListEventActionsRequestListEventActionsPaginateTypeDef = TypedDict(
    "ListEventActionsRequestListEventActionsPaginateTypeDef",
    {
        "EventSourceId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "ListJobsRequestListJobsPaginateTypeDef",
    {
        "DataSetId": NotRequired[str],
        "RevisionId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef = TypedDict(
    "ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef",
    {
        "DataSetId": str,
        "RevisionId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDataSetRevisionsResponseTypeDef = TypedDict(
    "ListDataSetRevisionsResponseTypeDef",
    {
        "NextToken": str,
        "Revisions": List[RevisionEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ScopeDetailsTypeDef = TypedDict(
    "ScopeDetailsTypeDef",
    {
        "LakeFormationTagPolicies": NotRequired[Sequence[LakeFormationTagPolicyDetailsTypeDef]],
        "RedshiftDataShares": NotRequired[Sequence[RedshiftDataShareDetailsTypeDef]],
        "S3DataAccesses": NotRequired[Sequence[S3DataAccessDetailsTypeDef]],
    },
)

SchemaChangeRequestDetailsTypeDef = TypedDict(
    "SchemaChangeRequestDetailsTypeDef",
    {
        "SchemaChangeAt": TimestampTypeDef,
        "Changes": NotRequired[Sequence[SchemaChangeDetailsTypeDef]],
    },
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "ExportRevisionToS3": NotRequired[AutoExportRevisionToS3RequestDetailsTypeDef],
    },
)

ListDataSetsResponseTypeDef = TypedDict(
    "ListDataSetsResponseTypeDef",
    {
        "DataSets": List[DataSetEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportAssetsFromLakeFormationTagPolicyResponseDetailsPaginatorTypeDef = TypedDict(
    "ImportAssetsFromLakeFormationTagPolicyResponseDetailsPaginatorTypeDef",
    {
        "CatalogId": str,
        "RoleArn": str,
        "DataSetId": str,
        "RevisionId": str,
        "Database": NotRequired[DatabaseLFTagPolicyAndPermissionsPaginatorTypeDef],
        "Table": NotRequired[TableLFTagPolicyAndPermissionsPaginatorTypeDef],
    },
)

LFResourceDetailsPaginatorTypeDef = TypedDict(
    "LFResourceDetailsPaginatorTypeDef",
    {
        "Database": NotRequired[DatabaseLFTagPolicyPaginatorTypeDef],
        "Table": NotRequired[TableLFTagPolicyPaginatorTypeDef],
    },
)

ImportAssetsFromLakeFormationTagPolicyRequestDetailsTypeDef = TypedDict(
    "ImportAssetsFromLakeFormationTagPolicyRequestDetailsTypeDef",
    {
        "CatalogId": str,
        "RoleArn": str,
        "DataSetId": str,
        "RevisionId": str,
        "Database": NotRequired[DatabaseLFTagPolicyAndPermissionsTypeDef],
        "Table": NotRequired[TableLFTagPolicyAndPermissionsTypeDef],
    },
)

ImportAssetsFromLakeFormationTagPolicyResponseDetailsTypeDef = TypedDict(
    "ImportAssetsFromLakeFormationTagPolicyResponseDetailsTypeDef",
    {
        "CatalogId": str,
        "RoleArn": str,
        "DataSetId": str,
        "RevisionId": str,
        "Database": NotRequired[DatabaseLFTagPolicyAndPermissionsTypeDef],
        "Table": NotRequired[TableLFTagPolicyAndPermissionsTypeDef],
    },
)

LFResourceDetailsTypeDef = TypedDict(
    "LFResourceDetailsTypeDef",
    {
        "Database": NotRequired[DatabaseLFTagPolicyTypeDef],
        "Table": NotRequired[TableLFTagPolicyTypeDef],
    },
)

JobErrorTypeDef = TypedDict(
    "JobErrorTypeDef",
    {
        "Code": CodeType,
        "Message": str,
        "Details": NotRequired[DetailsTypeDef],
        "LimitName": NotRequired[JobErrorLimitNameType],
        "LimitValue": NotRequired[float],
        "ResourceId": NotRequired[str],
        "ResourceType": NotRequired[JobErrorResourceTypesType],
    },
)

CreateS3DataAccessFromS3BucketResponseDetailsPaginatorTypeDef = TypedDict(
    "CreateS3DataAccessFromS3BucketResponseDetailsPaginatorTypeDef",
    {
        "AssetSource": S3DataAccessAssetSourceEntryPaginatorTypeDef,
        "DataSetId": str,
        "RevisionId": str,
    },
)

CreateS3DataAccessFromS3BucketRequestDetailsTypeDef = TypedDict(
    "CreateS3DataAccessFromS3BucketRequestDetailsTypeDef",
    {
        "AssetSource": S3DataAccessAssetSourceEntryTypeDef,
        "DataSetId": str,
        "RevisionId": str,
    },
)

CreateS3DataAccessFromS3BucketResponseDetailsTypeDef = TypedDict(
    "CreateS3DataAccessFromS3BucketResponseDetailsTypeDef",
    {
        "AssetSource": S3DataAccessAssetSourceEntryTypeDef,
        "DataSetId": str,
        "RevisionId": str,
    },
)

NotificationDetailsTypeDef = TypedDict(
    "NotificationDetailsTypeDef",
    {
        "DataUpdate": NotRequired[DataUpdateRequestDetailsTypeDef],
        "Deprecation": NotRequired[DeprecationRequestDetailsTypeDef],
        "SchemaChange": NotRequired[SchemaChangeRequestDetailsTypeDef],
    },
)

CreateEventActionRequestRequestTypeDef = TypedDict(
    "CreateEventActionRequestRequestTypeDef",
    {
        "Action": ActionTypeDef,
        "Event": EventTypeDef,
    },
)

CreateEventActionResponseTypeDef = TypedDict(
    "CreateEventActionResponseTypeDef",
    {
        "Action": ActionTypeDef,
        "Arn": str,
        "CreatedAt": datetime,
        "Event": EventTypeDef,
        "Id": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventActionEntryTypeDef = TypedDict(
    "EventActionEntryTypeDef",
    {
        "Action": ActionTypeDef,
        "Arn": str,
        "CreatedAt": datetime,
        "Event": EventTypeDef,
        "Id": str,
        "UpdatedAt": datetime,
    },
)

GetEventActionResponseTypeDef = TypedDict(
    "GetEventActionResponseTypeDef",
    {
        "Action": ActionTypeDef,
        "Arn": str,
        "CreatedAt": datetime,
        "Event": EventTypeDef,
        "Id": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEventActionRequestRequestTypeDef = TypedDict(
    "UpdateEventActionRequestRequestTypeDef",
    {
        "EventActionId": str,
        "Action": NotRequired[ActionTypeDef],
    },
)

UpdateEventActionResponseTypeDef = TypedDict(
    "UpdateEventActionResponseTypeDef",
    {
        "Action": ActionTypeDef,
        "Arn": str,
        "CreatedAt": datetime,
        "Event": EventTypeDef,
        "Id": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LFTagPolicyDetailsPaginatorTypeDef = TypedDict(
    "LFTagPolicyDetailsPaginatorTypeDef",
    {
        "CatalogId": str,
        "ResourceType": LFResourceTypeType,
        "ResourceDetails": LFResourceDetailsPaginatorTypeDef,
    },
)

LFTagPolicyDetailsTypeDef = TypedDict(
    "LFTagPolicyDetailsTypeDef",
    {
        "CatalogId": str,
        "ResourceType": LFResourceTypeType,
        "ResourceDetails": LFResourceDetailsTypeDef,
    },
)

ResponseDetailsPaginatorTypeDef = TypedDict(
    "ResponseDetailsPaginatorTypeDef",
    {
        "ExportAssetToSignedUrl": NotRequired[ExportAssetToSignedUrlResponseDetailsTypeDef],
        "ExportAssetsToS3": NotRequired[ExportAssetsToS3ResponseDetailsTypeDef],
        "ExportRevisionsToS3": NotRequired[ExportRevisionsToS3ResponseDetailsTypeDef],
        "ImportAssetFromSignedUrl": NotRequired[ImportAssetFromSignedUrlResponseDetailsTypeDef],
        "ImportAssetsFromS3": NotRequired[ImportAssetsFromS3ResponseDetailsTypeDef],
        "ImportAssetsFromRedshiftDataShares": NotRequired[
            ImportAssetsFromRedshiftDataSharesResponseDetailsTypeDef
        ],
        "ImportAssetFromApiGatewayApi": NotRequired[
            ImportAssetFromApiGatewayApiResponseDetailsTypeDef
        ],
        "CreateS3DataAccessFromS3Bucket": NotRequired[
            CreateS3DataAccessFromS3BucketResponseDetailsPaginatorTypeDef
        ],
        "ImportAssetsFromLakeFormationTagPolicy": NotRequired[
            ImportAssetsFromLakeFormationTagPolicyResponseDetailsPaginatorTypeDef
        ],
    },
)

RequestDetailsTypeDef = TypedDict(
    "RequestDetailsTypeDef",
    {
        "ExportAssetToSignedUrl": NotRequired[ExportAssetToSignedUrlRequestDetailsTypeDef],
        "ExportAssetsToS3": NotRequired[ExportAssetsToS3RequestDetailsTypeDef],
        "ExportRevisionsToS3": NotRequired[ExportRevisionsToS3RequestDetailsTypeDef],
        "ImportAssetFromSignedUrl": NotRequired[ImportAssetFromSignedUrlRequestDetailsTypeDef],
        "ImportAssetsFromS3": NotRequired[ImportAssetsFromS3RequestDetailsTypeDef],
        "ImportAssetsFromRedshiftDataShares": NotRequired[
            ImportAssetsFromRedshiftDataSharesRequestDetailsTypeDef
        ],
        "ImportAssetFromApiGatewayApi": NotRequired[
            ImportAssetFromApiGatewayApiRequestDetailsTypeDef
        ],
        "CreateS3DataAccessFromS3Bucket": NotRequired[
            CreateS3DataAccessFromS3BucketRequestDetailsTypeDef
        ],
        "ImportAssetsFromLakeFormationTagPolicy": NotRequired[
            ImportAssetsFromLakeFormationTagPolicyRequestDetailsTypeDef
        ],
    },
)

ResponseDetailsTypeDef = TypedDict(
    "ResponseDetailsTypeDef",
    {
        "ExportAssetToSignedUrl": NotRequired[ExportAssetToSignedUrlResponseDetailsTypeDef],
        "ExportAssetsToS3": NotRequired[ExportAssetsToS3ResponseDetailsTypeDef],
        "ExportRevisionsToS3": NotRequired[ExportRevisionsToS3ResponseDetailsTypeDef],
        "ImportAssetFromSignedUrl": NotRequired[ImportAssetFromSignedUrlResponseDetailsTypeDef],
        "ImportAssetsFromS3": NotRequired[ImportAssetsFromS3ResponseDetailsTypeDef],
        "ImportAssetsFromRedshiftDataShares": NotRequired[
            ImportAssetsFromRedshiftDataSharesResponseDetailsTypeDef
        ],
        "ImportAssetFromApiGatewayApi": NotRequired[
            ImportAssetFromApiGatewayApiResponseDetailsTypeDef
        ],
        "CreateS3DataAccessFromS3Bucket": NotRequired[
            CreateS3DataAccessFromS3BucketResponseDetailsTypeDef
        ],
        "ImportAssetsFromLakeFormationTagPolicy": NotRequired[
            ImportAssetsFromLakeFormationTagPolicyResponseDetailsTypeDef
        ],
    },
)

SendDataSetNotificationRequestRequestTypeDef = TypedDict(
    "SendDataSetNotificationRequestRequestTypeDef",
    {
        "DataSetId": str,
        "Type": NotificationTypeType,
        "Scope": NotRequired[ScopeDetailsTypeDef],
        "ClientToken": NotRequired[str],
        "Comment": NotRequired[str],
        "Details": NotRequired[NotificationDetailsTypeDef],
    },
)

ListEventActionsResponseTypeDef = TypedDict(
    "ListEventActionsResponseTypeDef",
    {
        "EventActions": List[EventActionEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LakeFormationDataPermissionDetailsPaginatorTypeDef = TypedDict(
    "LakeFormationDataPermissionDetailsPaginatorTypeDef",
    {
        "LFTagPolicy": NotRequired[LFTagPolicyDetailsPaginatorTypeDef],
    },
)

LakeFormationDataPermissionDetailsTypeDef = TypedDict(
    "LakeFormationDataPermissionDetailsTypeDef",
    {
        "LFTagPolicy": NotRequired[LFTagPolicyDetailsTypeDef],
    },
)

JobEntryPaginatorTypeDef = TypedDict(
    "JobEntryPaginatorTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Details": ResponseDetailsPaginatorTypeDef,
        "Id": str,
        "State": StateType,
        "Type": TypeType,
        "UpdatedAt": datetime,
        "Errors": NotRequired[List[JobErrorTypeDef]],
    },
)

CreateJobRequestRequestTypeDef = TypedDict(
    "CreateJobRequestRequestTypeDef",
    {
        "Details": RequestDetailsTypeDef,
        "Type": TypeType,
    },
)

CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Details": ResponseDetailsTypeDef,
        "Errors": List[JobErrorTypeDef],
        "Id": str,
        "State": StateType,
        "Type": TypeType,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobResponseTypeDef = TypedDict(
    "GetJobResponseTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Details": ResponseDetailsTypeDef,
        "Errors": List[JobErrorTypeDef],
        "Id": str,
        "State": StateType,
        "Type": TypeType,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobEntryTypeDef = TypedDict(
    "JobEntryTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Details": ResponseDetailsTypeDef,
        "Id": str,
        "State": StateType,
        "Type": TypeType,
        "UpdatedAt": datetime,
        "Errors": NotRequired[List[JobErrorTypeDef]],
    },
)

LakeFormationDataPermissionAssetPaginatorTypeDef = TypedDict(
    "LakeFormationDataPermissionAssetPaginatorTypeDef",
    {
        "LakeFormationDataPermissionDetails": LakeFormationDataPermissionDetailsPaginatorTypeDef,
        "LakeFormationDataPermissionType": Literal["LFTagPolicy"],
        "Permissions": List[LFPermissionType],
        "RoleArn": NotRequired[str],
    },
)

LakeFormationDataPermissionAssetTypeDef = TypedDict(
    "LakeFormationDataPermissionAssetTypeDef",
    {
        "LakeFormationDataPermissionDetails": LakeFormationDataPermissionDetailsTypeDef,
        "LakeFormationDataPermissionType": Literal["LFTagPolicy"],
        "Permissions": List[LFPermissionType],
        "RoleArn": NotRequired[str],
    },
)

ListJobsResponsePaginatorTypeDef = TypedDict(
    "ListJobsResponsePaginatorTypeDef",
    {
        "Jobs": List[JobEntryPaginatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef",
    {
        "Jobs": List[JobEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssetDetailsPaginatorTypeDef = TypedDict(
    "AssetDetailsPaginatorTypeDef",
    {
        "S3SnapshotAsset": NotRequired[S3SnapshotAssetTypeDef],
        "RedshiftDataShareAsset": NotRequired[RedshiftDataShareAssetTypeDef],
        "ApiGatewayApiAsset": NotRequired[ApiGatewayApiAssetTypeDef],
        "S3DataAccessAsset": NotRequired[S3DataAccessAssetTypeDef],
        "LakeFormationDataPermissionAsset": NotRequired[
            LakeFormationDataPermissionAssetPaginatorTypeDef
        ],
    },
)

AssetDetailsTypeDef = TypedDict(
    "AssetDetailsTypeDef",
    {
        "S3SnapshotAsset": NotRequired[S3SnapshotAssetTypeDef],
        "RedshiftDataShareAsset": NotRequired[RedshiftDataShareAssetTypeDef],
        "ApiGatewayApiAsset": NotRequired[ApiGatewayApiAssetTypeDef],
        "S3DataAccessAsset": NotRequired[S3DataAccessAssetTypeDef],
        "LakeFormationDataPermissionAsset": NotRequired[LakeFormationDataPermissionAssetTypeDef],
    },
)

AssetEntryPaginatorTypeDef = TypedDict(
    "AssetEntryPaginatorTypeDef",
    {
        "Arn": str,
        "AssetDetails": AssetDetailsPaginatorTypeDef,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "Name": str,
        "RevisionId": str,
        "UpdatedAt": datetime,
        "SourceId": NotRequired[str],
    },
)

AssetEntryTypeDef = TypedDict(
    "AssetEntryTypeDef",
    {
        "Arn": str,
        "AssetDetails": AssetDetailsTypeDef,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "Name": str,
        "RevisionId": str,
        "UpdatedAt": datetime,
        "SourceId": NotRequired[str],
    },
)

GetAssetResponseTypeDef = TypedDict(
    "GetAssetResponseTypeDef",
    {
        "Arn": str,
        "AssetDetails": AssetDetailsTypeDef,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "Name": str,
        "RevisionId": str,
        "SourceId": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssetResponseTypeDef = TypedDict(
    "UpdateAssetResponseTypeDef",
    {
        "Arn": str,
        "AssetDetails": AssetDetailsTypeDef,
        "AssetType": AssetTypeType,
        "CreatedAt": datetime,
        "DataSetId": str,
        "Id": str,
        "Name": str,
        "RevisionId": str,
        "SourceId": str,
        "UpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRevisionAssetsResponsePaginatorTypeDef = TypedDict(
    "ListRevisionAssetsResponsePaginatorTypeDef",
    {
        "Assets": List[AssetEntryPaginatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRevisionAssetsResponseTypeDef = TypedDict(
    "ListRevisionAssetsResponseTypeDef",
    {
        "Assets": List[AssetEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
