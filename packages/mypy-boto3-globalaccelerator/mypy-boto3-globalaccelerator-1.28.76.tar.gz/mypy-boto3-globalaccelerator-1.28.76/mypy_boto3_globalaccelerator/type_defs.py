"""
Type annotations for globalaccelerator service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_globalaccelerator/type_defs/)

Usage::

    ```python
    from mypy_boto3_globalaccelerator.type_defs import AcceleratorAttributesTypeDef

    data: AcceleratorAttributesTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AcceleratorStatusType,
    ByoipCidrStateType,
    ClientAffinityType,
    CustomRoutingAcceleratorStatusType,
    CustomRoutingDestinationTrafficStateType,
    CustomRoutingProtocolType,
    HealthCheckProtocolType,
    HealthStateType,
    IpAddressFamilyType,
    IpAddressTypeType,
    ProtocolType,
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
    "AcceleratorAttributesTypeDef",
    "AcceleratorEventTypeDef",
    "IpSetTypeDef",
    "CustomRoutingEndpointConfigurationTypeDef",
    "CustomRoutingEndpointDescriptionTypeDef",
    "ResponseMetadataTypeDef",
    "EndpointConfigurationTypeDef",
    "EndpointDescriptionTypeDef",
    "AdvertiseByoipCidrRequestRequestTypeDef",
    "AllowCustomRoutingTrafficRequestRequestTypeDef",
    "ResourceTypeDef",
    "ByoipCidrEventTypeDef",
    "CidrAuthorizationContextTypeDef",
    "TagTypeDef",
    "CustomRoutingDestinationConfigurationTypeDef",
    "PortRangeTypeDef",
    "PortOverrideTypeDef",
    "CrossAccountResourceTypeDef",
    "CustomRoutingAcceleratorAttributesTypeDef",
    "CustomRoutingDestinationDescriptionTypeDef",
    "DeleteAcceleratorRequestRequestTypeDef",
    "DeleteCrossAccountAttachmentRequestRequestTypeDef",
    "DeleteCustomRoutingAcceleratorRequestRequestTypeDef",
    "DeleteCustomRoutingEndpointGroupRequestRequestTypeDef",
    "DeleteCustomRoutingListenerRequestRequestTypeDef",
    "DeleteEndpointGroupRequestRequestTypeDef",
    "DeleteListenerRequestRequestTypeDef",
    "DenyCustomRoutingTrafficRequestRequestTypeDef",
    "DeprovisionByoipCidrRequestRequestTypeDef",
    "DescribeAcceleratorAttributesRequestRequestTypeDef",
    "DescribeAcceleratorRequestRequestTypeDef",
    "DescribeCrossAccountAttachmentRequestRequestTypeDef",
    "DescribeCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    "DescribeCustomRoutingAcceleratorRequestRequestTypeDef",
    "DescribeCustomRoutingEndpointGroupRequestRequestTypeDef",
    "DescribeCustomRoutingListenerRequestRequestTypeDef",
    "DescribeEndpointGroupRequestRequestTypeDef",
    "DescribeListenerRequestRequestTypeDef",
    "SocketAddressTypeDef",
    "EndpointIdentifierTypeDef",
    "PaginatorConfigTypeDef",
    "ListAcceleratorsRequestRequestTypeDef",
    "ListByoipCidrsRequestRequestTypeDef",
    "ListCrossAccountAttachmentsRequestRequestTypeDef",
    "ListCrossAccountResourcesRequestRequestTypeDef",
    "ListCustomRoutingAcceleratorsRequestRequestTypeDef",
    "ListCustomRoutingEndpointGroupsRequestRequestTypeDef",
    "ListCustomRoutingListenersRequestRequestTypeDef",
    "ListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef",
    "ListCustomRoutingPortMappingsRequestRequestTypeDef",
    "ListEndpointGroupsRequestRequestTypeDef",
    "ListListenersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RemoveCustomRoutingEndpointsRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAcceleratorAttributesRequestRequestTypeDef",
    "UpdateAcceleratorRequestRequestTypeDef",
    "UpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    "UpdateCustomRoutingAcceleratorRequestRequestTypeDef",
    "WithdrawByoipCidrRequestRequestTypeDef",
    "AcceleratorTypeDef",
    "CustomRoutingAcceleratorTypeDef",
    "AddCustomRoutingEndpointsRequestRequestTypeDef",
    "AddCustomRoutingEndpointsResponseTypeDef",
    "DescribeAcceleratorAttributesResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListCrossAccountResourceAccountsResponseTypeDef",
    "UpdateAcceleratorAttributesResponseTypeDef",
    "AddEndpointsRequestRequestTypeDef",
    "AddEndpointsResponseTypeDef",
    "AttachmentTypeDef",
    "UpdateCrossAccountAttachmentRequestRequestTypeDef",
    "ByoipCidrTypeDef",
    "ProvisionByoipCidrRequestRequestTypeDef",
    "CreateAcceleratorRequestRequestTypeDef",
    "CreateCrossAccountAttachmentRequestRequestTypeDef",
    "CreateCustomRoutingAcceleratorRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateCustomRoutingEndpointGroupRequestRequestTypeDef",
    "CreateCustomRoutingListenerRequestRequestTypeDef",
    "CreateListenerRequestRequestTypeDef",
    "CustomRoutingListenerTypeDef",
    "ListenerTypeDef",
    "UpdateCustomRoutingListenerRequestRequestTypeDef",
    "UpdateListenerRequestRequestTypeDef",
    "CreateEndpointGroupRequestRequestTypeDef",
    "EndpointGroupTypeDef",
    "UpdateEndpointGroupRequestRequestTypeDef",
    "ListCrossAccountResourcesResponseTypeDef",
    "DescribeCustomRoutingAcceleratorAttributesResponseTypeDef",
    "UpdateCustomRoutingAcceleratorAttributesResponseTypeDef",
    "CustomRoutingEndpointGroupTypeDef",
    "DestinationPortMappingTypeDef",
    "PortMappingTypeDef",
    "RemoveEndpointsRequestRequestTypeDef",
    "ListAcceleratorsRequestListAcceleratorsPaginateTypeDef",
    "ListByoipCidrsRequestListByoipCidrsPaginateTypeDef",
    "ListCrossAccountAttachmentsRequestListCrossAccountAttachmentsPaginateTypeDef",
    "ListCrossAccountResourcesRequestListCrossAccountResourcesPaginateTypeDef",
    "ListCustomRoutingAcceleratorsRequestListCustomRoutingAcceleratorsPaginateTypeDef",
    "ListCustomRoutingEndpointGroupsRequestListCustomRoutingEndpointGroupsPaginateTypeDef",
    "ListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef",
    "ListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef",
    "ListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef",
    "ListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef",
    "ListListenersRequestListListenersPaginateTypeDef",
    "CreateAcceleratorResponseTypeDef",
    "DescribeAcceleratorResponseTypeDef",
    "ListAcceleratorsResponseTypeDef",
    "UpdateAcceleratorResponseTypeDef",
    "CreateCustomRoutingAcceleratorResponseTypeDef",
    "DescribeCustomRoutingAcceleratorResponseTypeDef",
    "ListCustomRoutingAcceleratorsResponseTypeDef",
    "UpdateCustomRoutingAcceleratorResponseTypeDef",
    "CreateCrossAccountAttachmentResponseTypeDef",
    "DescribeCrossAccountAttachmentResponseTypeDef",
    "ListCrossAccountAttachmentsResponseTypeDef",
    "UpdateCrossAccountAttachmentResponseTypeDef",
    "AdvertiseByoipCidrResponseTypeDef",
    "DeprovisionByoipCidrResponseTypeDef",
    "ListByoipCidrsResponseTypeDef",
    "ProvisionByoipCidrResponseTypeDef",
    "WithdrawByoipCidrResponseTypeDef",
    "CreateCustomRoutingListenerResponseTypeDef",
    "DescribeCustomRoutingListenerResponseTypeDef",
    "ListCustomRoutingListenersResponseTypeDef",
    "UpdateCustomRoutingListenerResponseTypeDef",
    "CreateListenerResponseTypeDef",
    "DescribeListenerResponseTypeDef",
    "ListListenersResponseTypeDef",
    "UpdateListenerResponseTypeDef",
    "CreateEndpointGroupResponseTypeDef",
    "DescribeEndpointGroupResponseTypeDef",
    "ListEndpointGroupsResponseTypeDef",
    "UpdateEndpointGroupResponseTypeDef",
    "CreateCustomRoutingEndpointGroupResponseTypeDef",
    "DescribeCustomRoutingEndpointGroupResponseTypeDef",
    "ListCustomRoutingEndpointGroupsResponseTypeDef",
    "ListCustomRoutingPortMappingsByDestinationResponseTypeDef",
    "ListCustomRoutingPortMappingsResponseTypeDef",
)

AcceleratorAttributesTypeDef = TypedDict(
    "AcceleratorAttributesTypeDef",
    {
        "FlowLogsEnabled": NotRequired[bool],
        "FlowLogsS3Bucket": NotRequired[str],
        "FlowLogsS3Prefix": NotRequired[str],
    },
)

AcceleratorEventTypeDef = TypedDict(
    "AcceleratorEventTypeDef",
    {
        "Message": NotRequired[str],
        "Timestamp": NotRequired[datetime],
    },
)

IpSetTypeDef = TypedDict(
    "IpSetTypeDef",
    {
        "IpFamily": NotRequired[str],
        "IpAddresses": NotRequired[List[str]],
        "IpAddressFamily": NotRequired[IpAddressFamilyType],
    },
)

CustomRoutingEndpointConfigurationTypeDef = TypedDict(
    "CustomRoutingEndpointConfigurationTypeDef",
    {
        "EndpointId": NotRequired[str],
        "AttachmentArn": NotRequired[str],
    },
)

CustomRoutingEndpointDescriptionTypeDef = TypedDict(
    "CustomRoutingEndpointDescriptionTypeDef",
    {
        "EndpointId": NotRequired[str],
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

EndpointConfigurationTypeDef = TypedDict(
    "EndpointConfigurationTypeDef",
    {
        "EndpointId": NotRequired[str],
        "Weight": NotRequired[int],
        "ClientIPPreservationEnabled": NotRequired[bool],
        "AttachmentArn": NotRequired[str],
    },
)

EndpointDescriptionTypeDef = TypedDict(
    "EndpointDescriptionTypeDef",
    {
        "EndpointId": NotRequired[str],
        "Weight": NotRequired[int],
        "HealthState": NotRequired[HealthStateType],
        "HealthReason": NotRequired[str],
        "ClientIPPreservationEnabled": NotRequired[bool],
    },
)

AdvertiseByoipCidrRequestRequestTypeDef = TypedDict(
    "AdvertiseByoipCidrRequestRequestTypeDef",
    {
        "Cidr": str,
    },
)

AllowCustomRoutingTrafficRequestRequestTypeDef = TypedDict(
    "AllowCustomRoutingTrafficRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
        "EndpointId": str,
        "DestinationAddresses": NotRequired[Sequence[str]],
        "DestinationPorts": NotRequired[Sequence[int]],
        "AllowAllTrafficToEndpoint": NotRequired[bool],
    },
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "EndpointId": str,
        "Region": NotRequired[str],
    },
)

ByoipCidrEventTypeDef = TypedDict(
    "ByoipCidrEventTypeDef",
    {
        "Message": NotRequired[str],
        "Timestamp": NotRequired[datetime],
    },
)

CidrAuthorizationContextTypeDef = TypedDict(
    "CidrAuthorizationContextTypeDef",
    {
        "Message": str,
        "Signature": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

CustomRoutingDestinationConfigurationTypeDef = TypedDict(
    "CustomRoutingDestinationConfigurationTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
        "Protocols": Sequence[CustomRoutingProtocolType],
    },
)

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "FromPort": NotRequired[int],
        "ToPort": NotRequired[int],
    },
)

PortOverrideTypeDef = TypedDict(
    "PortOverrideTypeDef",
    {
        "ListenerPort": NotRequired[int],
        "EndpointPort": NotRequired[int],
    },
)

CrossAccountResourceTypeDef = TypedDict(
    "CrossAccountResourceTypeDef",
    {
        "EndpointId": NotRequired[str],
        "AttachmentArn": NotRequired[str],
    },
)

CustomRoutingAcceleratorAttributesTypeDef = TypedDict(
    "CustomRoutingAcceleratorAttributesTypeDef",
    {
        "FlowLogsEnabled": NotRequired[bool],
        "FlowLogsS3Bucket": NotRequired[str],
        "FlowLogsS3Prefix": NotRequired[str],
    },
)

CustomRoutingDestinationDescriptionTypeDef = TypedDict(
    "CustomRoutingDestinationDescriptionTypeDef",
    {
        "FromPort": NotRequired[int],
        "ToPort": NotRequired[int],
        "Protocols": NotRequired[List[ProtocolType]],
    },
)

DeleteAcceleratorRequestRequestTypeDef = TypedDict(
    "DeleteAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DeleteCrossAccountAttachmentRequestRequestTypeDef = TypedDict(
    "DeleteCrossAccountAttachmentRequestRequestTypeDef",
    {
        "AttachmentArn": str,
    },
)

DeleteCustomRoutingAcceleratorRequestRequestTypeDef = TypedDict(
    "DeleteCustomRoutingAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DeleteCustomRoutingEndpointGroupRequestRequestTypeDef = TypedDict(
    "DeleteCustomRoutingEndpointGroupRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
    },
)

DeleteCustomRoutingListenerRequestRequestTypeDef = TypedDict(
    "DeleteCustomRoutingListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)

DeleteEndpointGroupRequestRequestTypeDef = TypedDict(
    "DeleteEndpointGroupRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
    },
)

DeleteListenerRequestRequestTypeDef = TypedDict(
    "DeleteListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)

DenyCustomRoutingTrafficRequestRequestTypeDef = TypedDict(
    "DenyCustomRoutingTrafficRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
        "EndpointId": str,
        "DestinationAddresses": NotRequired[Sequence[str]],
        "DestinationPorts": NotRequired[Sequence[int]],
        "DenyAllTrafficToEndpoint": NotRequired[bool],
    },
)

DeprovisionByoipCidrRequestRequestTypeDef = TypedDict(
    "DeprovisionByoipCidrRequestRequestTypeDef",
    {
        "Cidr": str,
    },
)

DescribeAcceleratorAttributesRequestRequestTypeDef = TypedDict(
    "DescribeAcceleratorAttributesRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DescribeAcceleratorRequestRequestTypeDef = TypedDict(
    "DescribeAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DescribeCrossAccountAttachmentRequestRequestTypeDef = TypedDict(
    "DescribeCrossAccountAttachmentRequestRequestTypeDef",
    {
        "AttachmentArn": str,
    },
)

DescribeCustomRoutingAcceleratorAttributesRequestRequestTypeDef = TypedDict(
    "DescribeCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DescribeCustomRoutingAcceleratorRequestRequestTypeDef = TypedDict(
    "DescribeCustomRoutingAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
    },
)

DescribeCustomRoutingEndpointGroupRequestRequestTypeDef = TypedDict(
    "DescribeCustomRoutingEndpointGroupRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
    },
)

DescribeCustomRoutingListenerRequestRequestTypeDef = TypedDict(
    "DescribeCustomRoutingListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)

DescribeEndpointGroupRequestRequestTypeDef = TypedDict(
    "DescribeEndpointGroupRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
    },
)

DescribeListenerRequestRequestTypeDef = TypedDict(
    "DescribeListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
    },
)

SocketAddressTypeDef = TypedDict(
    "SocketAddressTypeDef",
    {
        "IpAddress": NotRequired[str],
        "Port": NotRequired[int],
    },
)

EndpointIdentifierTypeDef = TypedDict(
    "EndpointIdentifierTypeDef",
    {
        "EndpointId": str,
        "ClientIPPreservationEnabled": NotRequired[bool],
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

ListAcceleratorsRequestRequestTypeDef = TypedDict(
    "ListAcceleratorsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListByoipCidrsRequestRequestTypeDef = TypedDict(
    "ListByoipCidrsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListCrossAccountAttachmentsRequestRequestTypeDef = TypedDict(
    "ListCrossAccountAttachmentsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListCrossAccountResourcesRequestRequestTypeDef = TypedDict(
    "ListCrossAccountResourcesRequestRequestTypeDef",
    {
        "ResourceOwnerAwsAccountId": str,
        "AcceleratorArn": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListCustomRoutingAcceleratorsRequestRequestTypeDef = TypedDict(
    "ListCustomRoutingAcceleratorsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListCustomRoutingEndpointGroupsRequestRequestTypeDef = TypedDict(
    "ListCustomRoutingEndpointGroupsRequestRequestTypeDef",
    {
        "ListenerArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListCustomRoutingListenersRequestRequestTypeDef = TypedDict(
    "ListCustomRoutingListenersRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef = TypedDict(
    "ListCustomRoutingPortMappingsByDestinationRequestRequestTypeDef",
    {
        "EndpointId": str,
        "DestinationAddress": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListCustomRoutingPortMappingsRequestRequestTypeDef = TypedDict(
    "ListCustomRoutingPortMappingsRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "EndpointGroupArn": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListEndpointGroupsRequestRequestTypeDef = TypedDict(
    "ListEndpointGroupsRequestRequestTypeDef",
    {
        "ListenerArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListListenersRequestRequestTypeDef = TypedDict(
    "ListListenersRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
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

RemoveCustomRoutingEndpointsRequestRequestTypeDef = TypedDict(
    "RemoveCustomRoutingEndpointsRequestRequestTypeDef",
    {
        "EndpointIds": Sequence[str],
        "EndpointGroupArn": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateAcceleratorAttributesRequestRequestTypeDef = TypedDict(
    "UpdateAcceleratorAttributesRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "FlowLogsEnabled": NotRequired[bool],
        "FlowLogsS3Bucket": NotRequired[str],
        "FlowLogsS3Prefix": NotRequired[str],
    },
)

UpdateAcceleratorRequestRequestTypeDef = TypedDict(
    "UpdateAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "Name": NotRequired[str],
        "IpAddressType": NotRequired[IpAddressTypeType],
        "Enabled": NotRequired[bool],
    },
)

UpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef = TypedDict(
    "UpdateCustomRoutingAcceleratorAttributesRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "FlowLogsEnabled": NotRequired[bool],
        "FlowLogsS3Bucket": NotRequired[str],
        "FlowLogsS3Prefix": NotRequired[str],
    },
)

UpdateCustomRoutingAcceleratorRequestRequestTypeDef = TypedDict(
    "UpdateCustomRoutingAcceleratorRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "Name": NotRequired[str],
        "IpAddressType": NotRequired[IpAddressTypeType],
        "Enabled": NotRequired[bool],
    },
)

WithdrawByoipCidrRequestRequestTypeDef = TypedDict(
    "WithdrawByoipCidrRequestRequestTypeDef",
    {
        "Cidr": str,
    },
)

AcceleratorTypeDef = TypedDict(
    "AcceleratorTypeDef",
    {
        "AcceleratorArn": NotRequired[str],
        "Name": NotRequired[str],
        "IpAddressType": NotRequired[IpAddressTypeType],
        "Enabled": NotRequired[bool],
        "IpSets": NotRequired[List[IpSetTypeDef]],
        "DnsName": NotRequired[str],
        "Status": NotRequired[AcceleratorStatusType],
        "CreatedTime": NotRequired[datetime],
        "LastModifiedTime": NotRequired[datetime],
        "DualStackDnsName": NotRequired[str],
        "Events": NotRequired[List[AcceleratorEventTypeDef]],
    },
)

CustomRoutingAcceleratorTypeDef = TypedDict(
    "CustomRoutingAcceleratorTypeDef",
    {
        "AcceleratorArn": NotRequired[str],
        "Name": NotRequired[str],
        "IpAddressType": NotRequired[IpAddressTypeType],
        "Enabled": NotRequired[bool],
        "IpSets": NotRequired[List[IpSetTypeDef]],
        "DnsName": NotRequired[str],
        "Status": NotRequired[CustomRoutingAcceleratorStatusType],
        "CreatedTime": NotRequired[datetime],
        "LastModifiedTime": NotRequired[datetime],
    },
)

AddCustomRoutingEndpointsRequestRequestTypeDef = TypedDict(
    "AddCustomRoutingEndpointsRequestRequestTypeDef",
    {
        "EndpointConfigurations": Sequence[CustomRoutingEndpointConfigurationTypeDef],
        "EndpointGroupArn": str,
    },
)

AddCustomRoutingEndpointsResponseTypeDef = TypedDict(
    "AddCustomRoutingEndpointsResponseTypeDef",
    {
        "EndpointDescriptions": List[CustomRoutingEndpointDescriptionTypeDef],
        "EndpointGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAcceleratorAttributesResponseTypeDef = TypedDict(
    "DescribeAcceleratorAttributesResponseTypeDef",
    {
        "AcceleratorAttributes": AcceleratorAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCrossAccountResourceAccountsResponseTypeDef = TypedDict(
    "ListCrossAccountResourceAccountsResponseTypeDef",
    {
        "ResourceOwnerAwsAccountIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAcceleratorAttributesResponseTypeDef = TypedDict(
    "UpdateAcceleratorAttributesResponseTypeDef",
    {
        "AcceleratorAttributes": AcceleratorAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddEndpointsRequestRequestTypeDef = TypedDict(
    "AddEndpointsRequestRequestTypeDef",
    {
        "EndpointConfigurations": Sequence[EndpointConfigurationTypeDef],
        "EndpointGroupArn": str,
    },
)

AddEndpointsResponseTypeDef = TypedDict(
    "AddEndpointsResponseTypeDef",
    {
        "EndpointDescriptions": List[EndpointDescriptionTypeDef],
        "EndpointGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AttachmentTypeDef = TypedDict(
    "AttachmentTypeDef",
    {
        "AttachmentArn": NotRequired[str],
        "Name": NotRequired[str],
        "Principals": NotRequired[List[str]],
        "Resources": NotRequired[List[ResourceTypeDef]],
        "LastModifiedTime": NotRequired[datetime],
        "CreatedTime": NotRequired[datetime],
    },
)

UpdateCrossAccountAttachmentRequestRequestTypeDef = TypedDict(
    "UpdateCrossAccountAttachmentRequestRequestTypeDef",
    {
        "AttachmentArn": str,
        "Name": NotRequired[str],
        "AddPrincipals": NotRequired[Sequence[str]],
        "RemovePrincipals": NotRequired[Sequence[str]],
        "AddResources": NotRequired[Sequence[ResourceTypeDef]],
        "RemoveResources": NotRequired[Sequence[ResourceTypeDef]],
    },
)

ByoipCidrTypeDef = TypedDict(
    "ByoipCidrTypeDef",
    {
        "Cidr": NotRequired[str],
        "State": NotRequired[ByoipCidrStateType],
        "Events": NotRequired[List[ByoipCidrEventTypeDef]],
    },
)

ProvisionByoipCidrRequestRequestTypeDef = TypedDict(
    "ProvisionByoipCidrRequestRequestTypeDef",
    {
        "Cidr": str,
        "CidrAuthorizationContext": CidrAuthorizationContextTypeDef,
    },
)

CreateAcceleratorRequestRequestTypeDef = TypedDict(
    "CreateAcceleratorRequestRequestTypeDef",
    {
        "Name": str,
        "IdempotencyToken": str,
        "IpAddressType": NotRequired[IpAddressTypeType],
        "IpAddresses": NotRequired[Sequence[str]],
        "Enabled": NotRequired[bool],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

CreateCrossAccountAttachmentRequestRequestTypeDef = TypedDict(
    "CreateCrossAccountAttachmentRequestRequestTypeDef",
    {
        "Name": str,
        "IdempotencyToken": str,
        "Principals": NotRequired[Sequence[str]],
        "Resources": NotRequired[Sequence[ResourceTypeDef]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

CreateCustomRoutingAcceleratorRequestRequestTypeDef = TypedDict(
    "CreateCustomRoutingAcceleratorRequestRequestTypeDef",
    {
        "Name": str,
        "IdempotencyToken": str,
        "IpAddressType": NotRequired[IpAddressTypeType],
        "IpAddresses": NotRequired[Sequence[str]],
        "Enabled": NotRequired[bool],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateCustomRoutingEndpointGroupRequestRequestTypeDef = TypedDict(
    "CreateCustomRoutingEndpointGroupRequestRequestTypeDef",
    {
        "ListenerArn": str,
        "EndpointGroupRegion": str,
        "DestinationConfigurations": Sequence[CustomRoutingDestinationConfigurationTypeDef],
        "IdempotencyToken": str,
    },
)

CreateCustomRoutingListenerRequestRequestTypeDef = TypedDict(
    "CreateCustomRoutingListenerRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "PortRanges": Sequence[PortRangeTypeDef],
        "IdempotencyToken": str,
    },
)

CreateListenerRequestRequestTypeDef = TypedDict(
    "CreateListenerRequestRequestTypeDef",
    {
        "AcceleratorArn": str,
        "PortRanges": Sequence[PortRangeTypeDef],
        "Protocol": ProtocolType,
        "IdempotencyToken": str,
        "ClientAffinity": NotRequired[ClientAffinityType],
    },
)

CustomRoutingListenerTypeDef = TypedDict(
    "CustomRoutingListenerTypeDef",
    {
        "ListenerArn": NotRequired[str],
        "PortRanges": NotRequired[List[PortRangeTypeDef]],
    },
)

ListenerTypeDef = TypedDict(
    "ListenerTypeDef",
    {
        "ListenerArn": NotRequired[str],
        "PortRanges": NotRequired[List[PortRangeTypeDef]],
        "Protocol": NotRequired[ProtocolType],
        "ClientAffinity": NotRequired[ClientAffinityType],
    },
)

UpdateCustomRoutingListenerRequestRequestTypeDef = TypedDict(
    "UpdateCustomRoutingListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
        "PortRanges": Sequence[PortRangeTypeDef],
    },
)

UpdateListenerRequestRequestTypeDef = TypedDict(
    "UpdateListenerRequestRequestTypeDef",
    {
        "ListenerArn": str,
        "PortRanges": NotRequired[Sequence[PortRangeTypeDef]],
        "Protocol": NotRequired[ProtocolType],
        "ClientAffinity": NotRequired[ClientAffinityType],
    },
)

CreateEndpointGroupRequestRequestTypeDef = TypedDict(
    "CreateEndpointGroupRequestRequestTypeDef",
    {
        "ListenerArn": str,
        "EndpointGroupRegion": str,
        "IdempotencyToken": str,
        "EndpointConfigurations": NotRequired[Sequence[EndpointConfigurationTypeDef]],
        "TrafficDialPercentage": NotRequired[float],
        "HealthCheckPort": NotRequired[int],
        "HealthCheckProtocol": NotRequired[HealthCheckProtocolType],
        "HealthCheckPath": NotRequired[str],
        "HealthCheckIntervalSeconds": NotRequired[int],
        "ThresholdCount": NotRequired[int],
        "PortOverrides": NotRequired[Sequence[PortOverrideTypeDef]],
    },
)

EndpointGroupTypeDef = TypedDict(
    "EndpointGroupTypeDef",
    {
        "EndpointGroupArn": NotRequired[str],
        "EndpointGroupRegion": NotRequired[str],
        "EndpointDescriptions": NotRequired[List[EndpointDescriptionTypeDef]],
        "TrafficDialPercentage": NotRequired[float],
        "HealthCheckPort": NotRequired[int],
        "HealthCheckProtocol": NotRequired[HealthCheckProtocolType],
        "HealthCheckPath": NotRequired[str],
        "HealthCheckIntervalSeconds": NotRequired[int],
        "ThresholdCount": NotRequired[int],
        "PortOverrides": NotRequired[List[PortOverrideTypeDef]],
    },
)

UpdateEndpointGroupRequestRequestTypeDef = TypedDict(
    "UpdateEndpointGroupRequestRequestTypeDef",
    {
        "EndpointGroupArn": str,
        "EndpointConfigurations": NotRequired[Sequence[EndpointConfigurationTypeDef]],
        "TrafficDialPercentage": NotRequired[float],
        "HealthCheckPort": NotRequired[int],
        "HealthCheckProtocol": NotRequired[HealthCheckProtocolType],
        "HealthCheckPath": NotRequired[str],
        "HealthCheckIntervalSeconds": NotRequired[int],
        "ThresholdCount": NotRequired[int],
        "PortOverrides": NotRequired[Sequence[PortOverrideTypeDef]],
    },
)

ListCrossAccountResourcesResponseTypeDef = TypedDict(
    "ListCrossAccountResourcesResponseTypeDef",
    {
        "CrossAccountResources": List[CrossAccountResourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCustomRoutingAcceleratorAttributesResponseTypeDef = TypedDict(
    "DescribeCustomRoutingAcceleratorAttributesResponseTypeDef",
    {
        "AcceleratorAttributes": CustomRoutingAcceleratorAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCustomRoutingAcceleratorAttributesResponseTypeDef = TypedDict(
    "UpdateCustomRoutingAcceleratorAttributesResponseTypeDef",
    {
        "AcceleratorAttributes": CustomRoutingAcceleratorAttributesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomRoutingEndpointGroupTypeDef = TypedDict(
    "CustomRoutingEndpointGroupTypeDef",
    {
        "EndpointGroupArn": NotRequired[str],
        "EndpointGroupRegion": NotRequired[str],
        "DestinationDescriptions": NotRequired[List[CustomRoutingDestinationDescriptionTypeDef]],
        "EndpointDescriptions": NotRequired[List[CustomRoutingEndpointDescriptionTypeDef]],
    },
)

DestinationPortMappingTypeDef = TypedDict(
    "DestinationPortMappingTypeDef",
    {
        "AcceleratorArn": NotRequired[str],
        "AcceleratorSocketAddresses": NotRequired[List[SocketAddressTypeDef]],
        "EndpointGroupArn": NotRequired[str],
        "EndpointId": NotRequired[str],
        "EndpointGroupRegion": NotRequired[str],
        "DestinationSocketAddress": NotRequired[SocketAddressTypeDef],
        "IpAddressType": NotRequired[IpAddressTypeType],
        "DestinationTrafficState": NotRequired[CustomRoutingDestinationTrafficStateType],
    },
)

PortMappingTypeDef = TypedDict(
    "PortMappingTypeDef",
    {
        "AcceleratorPort": NotRequired[int],
        "EndpointGroupArn": NotRequired[str],
        "EndpointId": NotRequired[str],
        "DestinationSocketAddress": NotRequired[SocketAddressTypeDef],
        "Protocols": NotRequired[List[CustomRoutingProtocolType]],
        "DestinationTrafficState": NotRequired[CustomRoutingDestinationTrafficStateType],
    },
)

RemoveEndpointsRequestRequestTypeDef = TypedDict(
    "RemoveEndpointsRequestRequestTypeDef",
    {
        "EndpointIdentifiers": Sequence[EndpointIdentifierTypeDef],
        "EndpointGroupArn": str,
    },
)

ListAcceleratorsRequestListAcceleratorsPaginateTypeDef = TypedDict(
    "ListAcceleratorsRequestListAcceleratorsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListByoipCidrsRequestListByoipCidrsPaginateTypeDef = TypedDict(
    "ListByoipCidrsRequestListByoipCidrsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListCrossAccountAttachmentsRequestListCrossAccountAttachmentsPaginateTypeDef = TypedDict(
    "ListCrossAccountAttachmentsRequestListCrossAccountAttachmentsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListCrossAccountResourcesRequestListCrossAccountResourcesPaginateTypeDef = TypedDict(
    "ListCrossAccountResourcesRequestListCrossAccountResourcesPaginateTypeDef",
    {
        "ResourceOwnerAwsAccountId": str,
        "AcceleratorArn": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListCustomRoutingAcceleratorsRequestListCustomRoutingAcceleratorsPaginateTypeDef = TypedDict(
    "ListCustomRoutingAcceleratorsRequestListCustomRoutingAcceleratorsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListCustomRoutingEndpointGroupsRequestListCustomRoutingEndpointGroupsPaginateTypeDef = TypedDict(
    "ListCustomRoutingEndpointGroupsRequestListCustomRoutingEndpointGroupsPaginateTypeDef",
    {
        "ListenerArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef = TypedDict(
    "ListCustomRoutingListenersRequestListCustomRoutingListenersPaginateTypeDef",
    {
        "AcceleratorArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef = TypedDict(
    "ListCustomRoutingPortMappingsByDestinationRequestListCustomRoutingPortMappingsByDestinationPaginateTypeDef",
    {
        "EndpointId": str,
        "DestinationAddress": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef = TypedDict(
    "ListCustomRoutingPortMappingsRequestListCustomRoutingPortMappingsPaginateTypeDef",
    {
        "AcceleratorArn": str,
        "EndpointGroupArn": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef = TypedDict(
    "ListEndpointGroupsRequestListEndpointGroupsPaginateTypeDef",
    {
        "ListenerArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListListenersRequestListListenersPaginateTypeDef = TypedDict(
    "ListListenersRequestListListenersPaginateTypeDef",
    {
        "AcceleratorArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

CreateAcceleratorResponseTypeDef = TypedDict(
    "CreateAcceleratorResponseTypeDef",
    {
        "Accelerator": AcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAcceleratorResponseTypeDef = TypedDict(
    "DescribeAcceleratorResponseTypeDef",
    {
        "Accelerator": AcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAcceleratorsResponseTypeDef = TypedDict(
    "ListAcceleratorsResponseTypeDef",
    {
        "Accelerators": List[AcceleratorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAcceleratorResponseTypeDef = TypedDict(
    "UpdateAcceleratorResponseTypeDef",
    {
        "Accelerator": AcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomRoutingAcceleratorResponseTypeDef = TypedDict(
    "CreateCustomRoutingAcceleratorResponseTypeDef",
    {
        "Accelerator": CustomRoutingAcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCustomRoutingAcceleratorResponseTypeDef = TypedDict(
    "DescribeCustomRoutingAcceleratorResponseTypeDef",
    {
        "Accelerator": CustomRoutingAcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomRoutingAcceleratorsResponseTypeDef = TypedDict(
    "ListCustomRoutingAcceleratorsResponseTypeDef",
    {
        "Accelerators": List[CustomRoutingAcceleratorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCustomRoutingAcceleratorResponseTypeDef = TypedDict(
    "UpdateCustomRoutingAcceleratorResponseTypeDef",
    {
        "Accelerator": CustomRoutingAcceleratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCrossAccountAttachmentResponseTypeDef = TypedDict(
    "CreateCrossAccountAttachmentResponseTypeDef",
    {
        "CrossAccountAttachment": AttachmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCrossAccountAttachmentResponseTypeDef = TypedDict(
    "DescribeCrossAccountAttachmentResponseTypeDef",
    {
        "CrossAccountAttachment": AttachmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCrossAccountAttachmentsResponseTypeDef = TypedDict(
    "ListCrossAccountAttachmentsResponseTypeDef",
    {
        "CrossAccountAttachments": List[AttachmentTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCrossAccountAttachmentResponseTypeDef = TypedDict(
    "UpdateCrossAccountAttachmentResponseTypeDef",
    {
        "CrossAccountAttachment": AttachmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AdvertiseByoipCidrResponseTypeDef = TypedDict(
    "AdvertiseByoipCidrResponseTypeDef",
    {
        "ByoipCidr": ByoipCidrTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeprovisionByoipCidrResponseTypeDef = TypedDict(
    "DeprovisionByoipCidrResponseTypeDef",
    {
        "ByoipCidr": ByoipCidrTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListByoipCidrsResponseTypeDef = TypedDict(
    "ListByoipCidrsResponseTypeDef",
    {
        "ByoipCidrs": List[ByoipCidrTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProvisionByoipCidrResponseTypeDef = TypedDict(
    "ProvisionByoipCidrResponseTypeDef",
    {
        "ByoipCidr": ByoipCidrTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WithdrawByoipCidrResponseTypeDef = TypedDict(
    "WithdrawByoipCidrResponseTypeDef",
    {
        "ByoipCidr": ByoipCidrTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomRoutingListenerResponseTypeDef = TypedDict(
    "CreateCustomRoutingListenerResponseTypeDef",
    {
        "Listener": CustomRoutingListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCustomRoutingListenerResponseTypeDef = TypedDict(
    "DescribeCustomRoutingListenerResponseTypeDef",
    {
        "Listener": CustomRoutingListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomRoutingListenersResponseTypeDef = TypedDict(
    "ListCustomRoutingListenersResponseTypeDef",
    {
        "Listeners": List[CustomRoutingListenerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCustomRoutingListenerResponseTypeDef = TypedDict(
    "UpdateCustomRoutingListenerResponseTypeDef",
    {
        "Listener": CustomRoutingListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateListenerResponseTypeDef = TypedDict(
    "CreateListenerResponseTypeDef",
    {
        "Listener": ListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeListenerResponseTypeDef = TypedDict(
    "DescribeListenerResponseTypeDef",
    {
        "Listener": ListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListListenersResponseTypeDef = TypedDict(
    "ListListenersResponseTypeDef",
    {
        "Listeners": List[ListenerTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateListenerResponseTypeDef = TypedDict(
    "UpdateListenerResponseTypeDef",
    {
        "Listener": ListenerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEndpointGroupResponseTypeDef = TypedDict(
    "CreateEndpointGroupResponseTypeDef",
    {
        "EndpointGroup": EndpointGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEndpointGroupResponseTypeDef = TypedDict(
    "DescribeEndpointGroupResponseTypeDef",
    {
        "EndpointGroup": EndpointGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEndpointGroupsResponseTypeDef = TypedDict(
    "ListEndpointGroupsResponseTypeDef",
    {
        "EndpointGroups": List[EndpointGroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEndpointGroupResponseTypeDef = TypedDict(
    "UpdateEndpointGroupResponseTypeDef",
    {
        "EndpointGroup": EndpointGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomRoutingEndpointGroupResponseTypeDef = TypedDict(
    "CreateCustomRoutingEndpointGroupResponseTypeDef",
    {
        "EndpointGroup": CustomRoutingEndpointGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCustomRoutingEndpointGroupResponseTypeDef = TypedDict(
    "DescribeCustomRoutingEndpointGroupResponseTypeDef",
    {
        "EndpointGroup": CustomRoutingEndpointGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomRoutingEndpointGroupsResponseTypeDef = TypedDict(
    "ListCustomRoutingEndpointGroupsResponseTypeDef",
    {
        "EndpointGroups": List[CustomRoutingEndpointGroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomRoutingPortMappingsByDestinationResponseTypeDef = TypedDict(
    "ListCustomRoutingPortMappingsByDestinationResponseTypeDef",
    {
        "DestinationPortMappings": List[DestinationPortMappingTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomRoutingPortMappingsResponseTypeDef = TypedDict(
    "ListCustomRoutingPortMappingsResponseTypeDef",
    {
        "PortMappings": List[PortMappingTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
