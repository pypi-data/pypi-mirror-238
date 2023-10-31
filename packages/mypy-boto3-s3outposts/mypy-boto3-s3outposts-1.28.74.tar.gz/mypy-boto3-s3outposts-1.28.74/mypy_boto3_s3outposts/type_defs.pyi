"""
Type annotations for s3outposts service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/type_defs/)

Usage::

    ```python
    from mypy_boto3_s3outposts.type_defs import CreateEndpointRequestRequestTypeDef

    data: CreateEndpointRequestRequestTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List

from .literals import EndpointAccessTypeType, EndpointStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "CreateEndpointRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteEndpointRequestRequestTypeDef",
    "FailedReasonTypeDef",
    "NetworkInterfaceTypeDef",
    "PaginatorConfigTypeDef",
    "ListEndpointsRequestRequestTypeDef",
    "ListOutpostsWithS3RequestRequestTypeDef",
    "OutpostTypeDef",
    "ListSharedEndpointsRequestRequestTypeDef",
    "CreateEndpointResultTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointTypeDef",
    "ListEndpointsRequestListEndpointsPaginateTypeDef",
    "ListOutpostsWithS3RequestListOutpostsWithS3PaginateTypeDef",
    "ListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef",
    "ListOutpostsWithS3ResultTypeDef",
    "ListEndpointsResultTypeDef",
    "ListSharedEndpointsResultTypeDef",
)

CreateEndpointRequestRequestTypeDef = TypedDict(
    "CreateEndpointRequestRequestTypeDef",
    {
        "OutpostId": str,
        "SubnetId": str,
        "SecurityGroupId": str,
        "AccessType": NotRequired[EndpointAccessTypeType],
        "CustomerOwnedIpv4Pool": NotRequired[str],
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

DeleteEndpointRequestRequestTypeDef = TypedDict(
    "DeleteEndpointRequestRequestTypeDef",
    {
        "EndpointId": str,
        "OutpostId": str,
    },
)

FailedReasonTypeDef = TypedDict(
    "FailedReasonTypeDef",
    {
        "ErrorCode": NotRequired[str],
        "Message": NotRequired[str],
    },
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "NetworkInterfaceId": NotRequired[str],
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

ListEndpointsRequestRequestTypeDef = TypedDict(
    "ListEndpointsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListOutpostsWithS3RequestRequestTypeDef = TypedDict(
    "ListOutpostsWithS3RequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

OutpostTypeDef = TypedDict(
    "OutpostTypeDef",
    {
        "OutpostArn": NotRequired[str],
        "S3OutpostArn": NotRequired[str],
        "OutpostId": NotRequired[str],
        "OwnerId": NotRequired[str],
        "CapacityInBytes": NotRequired[int],
    },
)

ListSharedEndpointsRequestRequestTypeDef = TypedDict(
    "ListSharedEndpointsRequestRequestTypeDef",
    {
        "OutpostId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

CreateEndpointResultTypeDef = TypedDict(
    "CreateEndpointResultTypeDef",
    {
        "EndpointArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "EndpointArn": NotRequired[str],
        "OutpostsId": NotRequired[str],
        "CidrBlock": NotRequired[str],
        "Status": NotRequired[EndpointStatusType],
        "CreationTime": NotRequired[datetime],
        "NetworkInterfaces": NotRequired[List[NetworkInterfaceTypeDef]],
        "VpcId": NotRequired[str],
        "SubnetId": NotRequired[str],
        "SecurityGroupId": NotRequired[str],
        "AccessType": NotRequired[EndpointAccessTypeType],
        "CustomerOwnedIpv4Pool": NotRequired[str],
        "FailedReason": NotRequired[FailedReasonTypeDef],
    },
)

ListEndpointsRequestListEndpointsPaginateTypeDef = TypedDict(
    "ListEndpointsRequestListEndpointsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListOutpostsWithS3RequestListOutpostsWithS3PaginateTypeDef = TypedDict(
    "ListOutpostsWithS3RequestListOutpostsWithS3PaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef = TypedDict(
    "ListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef",
    {
        "OutpostId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListOutpostsWithS3ResultTypeDef = TypedDict(
    "ListOutpostsWithS3ResultTypeDef",
    {
        "Outposts": List[OutpostTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEndpointsResultTypeDef = TypedDict(
    "ListEndpointsResultTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSharedEndpointsResultTypeDef = TypedDict(
    "ListSharedEndpointsResultTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
