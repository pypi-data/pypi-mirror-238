"""
Type annotations for mediapackagev2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackagev2/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediapackagev2.type_defs import ChannelGroupListConfigurationTypeDef

    data: ChannelGroupListConfigurationTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    CmafEncryptionMethodType,
    ContainerTypeType,
    DrmSystemType,
    PresetSpeke20AudioType,
    PresetSpeke20VideoType,
    ScteFilterType,
    TsEncryptionMethodType,
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
    "ChannelGroupListConfigurationTypeDef",
    "ChannelListConfigurationTypeDef",
    "CreateChannelGroupRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "IngestEndpointTypeDef",
    "ScteHlsTypeDef",
    "DeleteChannelGroupRequestRequestTypeDef",
    "DeleteChannelPolicyRequestRequestTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeleteOriginEndpointPolicyRequestRequestTypeDef",
    "DeleteOriginEndpointRequestRequestTypeDef",
    "EncryptionContractConfigurationTypeDef",
    "EncryptionMethodTypeDef",
    "TimestampTypeDef",
    "GetChannelGroupRequestRequestTypeDef",
    "GetChannelPolicyRequestRequestTypeDef",
    "GetChannelRequestRequestTypeDef",
    "GetOriginEndpointPolicyRequestRequestTypeDef",
    "GetOriginEndpointRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListChannelGroupsRequestRequestTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListHlsManifestConfigurationTypeDef",
    "ListLowLatencyHlsManifestConfigurationTypeDef",
    "ListOriginEndpointsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutChannelPolicyRequestRequestTypeDef",
    "PutOriginEndpointPolicyRequestRequestTypeDef",
    "ScteTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateChannelGroupRequestRequestTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "CreateChannelGroupResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetChannelGroupResponseTypeDef",
    "GetChannelPolicyResponseTypeDef",
    "GetOriginEndpointPolicyResponseTypeDef",
    "ListChannelGroupsResponseTypeDef",
    "ListChannelsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateChannelGroupResponseTypeDef",
    "CreateChannelResponseTypeDef",
    "GetChannelResponseTypeDef",
    "UpdateChannelResponseTypeDef",
    "SpekeKeyProviderTypeDef",
    "FilterConfigurationTypeDef",
    "ListChannelGroupsRequestListChannelGroupsPaginateTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef",
    "OriginEndpointListConfigurationTypeDef",
    "EncryptionTypeDef",
    "CreateHlsManifestConfigurationTypeDef",
    "CreateLowLatencyHlsManifestConfigurationTypeDef",
    "GetHlsManifestConfigurationTypeDef",
    "GetLowLatencyHlsManifestConfigurationTypeDef",
    "ListOriginEndpointsResponseTypeDef",
    "SegmentTypeDef",
    "CreateOriginEndpointRequestRequestTypeDef",
    "CreateOriginEndpointResponseTypeDef",
    "GetOriginEndpointResponseTypeDef",
    "UpdateOriginEndpointRequestRequestTypeDef",
    "UpdateOriginEndpointResponseTypeDef",
)

ChannelGroupListConfigurationTypeDef = TypedDict(
    "ChannelGroupListConfigurationTypeDef",
    {
        "ChannelGroupName": str,
        "Arn": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": NotRequired[str],
    },
)

ChannelListConfigurationTypeDef = TypedDict(
    "ChannelListConfigurationTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelGroupName": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": NotRequired[str],
    },
)

CreateChannelGroupRequestRequestTypeDef = TypedDict(
    "CreateChannelGroupRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ClientToken": NotRequired[str],
        "Description": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
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

CreateChannelRequestRequestTypeDef = TypedDict(
    "CreateChannelRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "ClientToken": NotRequired[str],
        "Description": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)

IngestEndpointTypeDef = TypedDict(
    "IngestEndpointTypeDef",
    {
        "Id": NotRequired[str],
        "Url": NotRequired[str],
    },
)

ScteHlsTypeDef = TypedDict(
    "ScteHlsTypeDef",
    {
        "AdMarkerHls": NotRequired[Literal["DATERANGE"]],
    },
)

DeleteChannelGroupRequestRequestTypeDef = TypedDict(
    "DeleteChannelGroupRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
    },
)

DeleteChannelPolicyRequestRequestTypeDef = TypedDict(
    "DeleteChannelPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)

DeleteChannelRequestRequestTypeDef = TypedDict(
    "DeleteChannelRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)

DeleteOriginEndpointPolicyRequestRequestTypeDef = TypedDict(
    "DeleteOriginEndpointPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
    },
)

DeleteOriginEndpointRequestRequestTypeDef = TypedDict(
    "DeleteOriginEndpointRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
    },
)

EncryptionContractConfigurationTypeDef = TypedDict(
    "EncryptionContractConfigurationTypeDef",
    {
        "PresetSpeke20Audio": PresetSpeke20AudioType,
        "PresetSpeke20Video": PresetSpeke20VideoType,
    },
)

EncryptionMethodTypeDef = TypedDict(
    "EncryptionMethodTypeDef",
    {
        "TsEncryptionMethod": NotRequired[TsEncryptionMethodType],
        "CmafEncryptionMethod": NotRequired[CmafEncryptionMethodType],
    },
)

TimestampTypeDef = Union[datetime, str]
GetChannelGroupRequestRequestTypeDef = TypedDict(
    "GetChannelGroupRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
    },
)

GetChannelPolicyRequestRequestTypeDef = TypedDict(
    "GetChannelPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)

GetChannelRequestRequestTypeDef = TypedDict(
    "GetChannelRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
    },
)

GetOriginEndpointPolicyRequestRequestTypeDef = TypedDict(
    "GetOriginEndpointPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
    },
)

GetOriginEndpointRequestRequestTypeDef = TypedDict(
    "GetOriginEndpointRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
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

ListChannelGroupsRequestRequestTypeDef = TypedDict(
    "ListChannelGroupsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListChannelsRequestRequestTypeDef = TypedDict(
    "ListChannelsRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListHlsManifestConfigurationTypeDef = TypedDict(
    "ListHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
        "ChildManifestName": NotRequired[str],
        "Url": NotRequired[str],
    },
)

ListLowLatencyHlsManifestConfigurationTypeDef = TypedDict(
    "ListLowLatencyHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
        "ChildManifestName": NotRequired[str],
        "Url": NotRequired[str],
    },
)

ListOriginEndpointsRequestRequestTypeDef = TypedDict(
    "ListOriginEndpointsRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
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

PutChannelPolicyRequestRequestTypeDef = TypedDict(
    "PutChannelPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "Policy": str,
    },
)

PutOriginEndpointPolicyRequestRequestTypeDef = TypedDict(
    "PutOriginEndpointPolicyRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "Policy": str,
    },
)

ScteTypeDef = TypedDict(
    "ScteTypeDef",
    {
        "ScteFilter": NotRequired[Sequence[ScteFilterType]],
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

UpdateChannelGroupRequestRequestTypeDef = TypedDict(
    "UpdateChannelGroupRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "Description": NotRequired[str],
    },
)

UpdateChannelRequestRequestTypeDef = TypedDict(
    "UpdateChannelRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "Description": NotRequired[str],
    },
)

CreateChannelGroupResponseTypeDef = TypedDict(
    "CreateChannelGroupResponseTypeDef",
    {
        "ChannelGroupName": str,
        "Arn": str,
        "EgressDomain": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetChannelGroupResponseTypeDef = TypedDict(
    "GetChannelGroupResponseTypeDef",
    {
        "ChannelGroupName": str,
        "Arn": str,
        "EgressDomain": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetChannelPolicyResponseTypeDef = TypedDict(
    "GetChannelPolicyResponseTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOriginEndpointPolicyResponseTypeDef = TypedDict(
    "GetOriginEndpointPolicyResponseTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListChannelGroupsResponseTypeDef = TypedDict(
    "ListChannelGroupsResponseTypeDef",
    {
        "Items": List[ChannelGroupListConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListChannelsResponseTypeDef = TypedDict(
    "ListChannelsResponseTypeDef",
    {
        "Items": List[ChannelListConfigurationTypeDef],
        "NextToken": str,
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

UpdateChannelGroupResponseTypeDef = TypedDict(
    "UpdateChannelGroupResponseTypeDef",
    {
        "ChannelGroupName": str,
        "Arn": str,
        "EgressDomain": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateChannelResponseTypeDef = TypedDict(
    "CreateChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelGroupName": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "IngestEndpoints": List[IngestEndpointTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetChannelResponseTypeDef = TypedDict(
    "GetChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelGroupName": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "IngestEndpoints": List[IngestEndpointTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateChannelResponseTypeDef = TypedDict(
    "UpdateChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelName": str,
        "ChannelGroupName": str,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "IngestEndpoints": List[IngestEndpointTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SpekeKeyProviderTypeDef = TypedDict(
    "SpekeKeyProviderTypeDef",
    {
        "EncryptionContractConfiguration": EncryptionContractConfigurationTypeDef,
        "ResourceId": str,
        "DrmSystems": Sequence[DrmSystemType],
        "RoleArn": str,
        "Url": str,
    },
)

FilterConfigurationTypeDef = TypedDict(
    "FilterConfigurationTypeDef",
    {
        "ManifestFilter": NotRequired[str],
        "Start": NotRequired[TimestampTypeDef],
        "End": NotRequired[TimestampTypeDef],
        "TimeDelaySeconds": NotRequired[int],
    },
)

ListChannelGroupsRequestListChannelGroupsPaginateTypeDef = TypedDict(
    "ListChannelGroupsRequestListChannelGroupsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListChannelsRequestListChannelsPaginateTypeDef = TypedDict(
    "ListChannelsRequestListChannelsPaginateTypeDef",
    {
        "ChannelGroupName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef = TypedDict(
    "ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

OriginEndpointListConfigurationTypeDef = TypedDict(
    "OriginEndpointListConfigurationTypeDef",
    {
        "Arn": str,
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
        "Description": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "ModifiedAt": NotRequired[datetime],
        "HlsManifests": NotRequired[List[ListHlsManifestConfigurationTypeDef]],
        "LowLatencyHlsManifests": NotRequired[List[ListLowLatencyHlsManifestConfigurationTypeDef]],
    },
)

EncryptionTypeDef = TypedDict(
    "EncryptionTypeDef",
    {
        "EncryptionMethod": EncryptionMethodTypeDef,
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
        "ConstantInitializationVector": NotRequired[str],
        "KeyRotationIntervalSeconds": NotRequired[int],
    },
)

CreateHlsManifestConfigurationTypeDef = TypedDict(
    "CreateHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
        "ChildManifestName": NotRequired[str],
        "ScteHls": NotRequired[ScteHlsTypeDef],
        "ManifestWindowSeconds": NotRequired[int],
        "ProgramDateTimeIntervalSeconds": NotRequired[int],
        "FilterConfiguration": NotRequired[FilterConfigurationTypeDef],
    },
)

CreateLowLatencyHlsManifestConfigurationTypeDef = TypedDict(
    "CreateLowLatencyHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
        "ChildManifestName": NotRequired[str],
        "ScteHls": NotRequired[ScteHlsTypeDef],
        "ManifestWindowSeconds": NotRequired[int],
        "ProgramDateTimeIntervalSeconds": NotRequired[int],
        "FilterConfiguration": NotRequired[FilterConfigurationTypeDef],
    },
)

GetHlsManifestConfigurationTypeDef = TypedDict(
    "GetHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
        "Url": str,
        "ChildManifestName": NotRequired[str],
        "ManifestWindowSeconds": NotRequired[int],
        "ProgramDateTimeIntervalSeconds": NotRequired[int],
        "ScteHls": NotRequired[ScteHlsTypeDef],
        "FilterConfiguration": NotRequired[FilterConfigurationTypeDef],
    },
)

GetLowLatencyHlsManifestConfigurationTypeDef = TypedDict(
    "GetLowLatencyHlsManifestConfigurationTypeDef",
    {
        "ManifestName": str,
        "Url": str,
        "ChildManifestName": NotRequired[str],
        "ManifestWindowSeconds": NotRequired[int],
        "ProgramDateTimeIntervalSeconds": NotRequired[int],
        "ScteHls": NotRequired[ScteHlsTypeDef],
        "FilterConfiguration": NotRequired[FilterConfigurationTypeDef],
    },
)

ListOriginEndpointsResponseTypeDef = TypedDict(
    "ListOriginEndpointsResponseTypeDef",
    {
        "Items": List[OriginEndpointListConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SegmentTypeDef = TypedDict(
    "SegmentTypeDef",
    {
        "SegmentDurationSeconds": NotRequired[int],
        "SegmentName": NotRequired[str],
        "TsUseAudioRenditionGroup": NotRequired[bool],
        "IncludeIframeOnlyStreams": NotRequired[bool],
        "TsIncludeDvbSubtitles": NotRequired[bool],
        "Scte": NotRequired[ScteTypeDef],
        "Encryption": NotRequired[EncryptionTypeDef],
    },
)

CreateOriginEndpointRequestRequestTypeDef = TypedDict(
    "CreateOriginEndpointRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
        "Segment": NotRequired[SegmentTypeDef],
        "ClientToken": NotRequired[str],
        "Description": NotRequired[str],
        "StartoverWindowSeconds": NotRequired[int],
        "HlsManifests": NotRequired[Sequence[CreateHlsManifestConfigurationTypeDef]],
        "LowLatencyHlsManifests": NotRequired[
            Sequence[CreateLowLatencyHlsManifestConfigurationTypeDef]
        ],
        "Tags": NotRequired[Mapping[str, str]],
    },
)

CreateOriginEndpointResponseTypeDef = TypedDict(
    "CreateOriginEndpointResponseTypeDef",
    {
        "Arn": str,
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
        "Segment": SegmentTypeDef,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "StartoverWindowSeconds": int,
        "HlsManifests": List[GetHlsManifestConfigurationTypeDef],
        "LowLatencyHlsManifests": List[GetLowLatencyHlsManifestConfigurationTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOriginEndpointResponseTypeDef = TypedDict(
    "GetOriginEndpointResponseTypeDef",
    {
        "Arn": str,
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
        "Segment": SegmentTypeDef,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "StartoverWindowSeconds": int,
        "HlsManifests": List[GetHlsManifestConfigurationTypeDef],
        "LowLatencyHlsManifests": List[GetLowLatencyHlsManifestConfigurationTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateOriginEndpointRequestRequestTypeDef = TypedDict(
    "UpdateOriginEndpointRequestRequestTypeDef",
    {
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
        "Segment": NotRequired[SegmentTypeDef],
        "Description": NotRequired[str],
        "StartoverWindowSeconds": NotRequired[int],
        "HlsManifests": NotRequired[Sequence[CreateHlsManifestConfigurationTypeDef]],
        "LowLatencyHlsManifests": NotRequired[
            Sequence[CreateLowLatencyHlsManifestConfigurationTypeDef]
        ],
    },
)

UpdateOriginEndpointResponseTypeDef = TypedDict(
    "UpdateOriginEndpointResponseTypeDef",
    {
        "Arn": str,
        "ChannelGroupName": str,
        "ChannelName": str,
        "OriginEndpointName": str,
        "ContainerType": ContainerTypeType,
        "Segment": SegmentTypeDef,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "Description": str,
        "StartoverWindowSeconds": int,
        "HlsManifests": List[GetHlsManifestConfigurationTypeDef],
        "LowLatencyHlsManifests": List[GetLowLatencyHlsManifestConfigurationTypeDef],
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
