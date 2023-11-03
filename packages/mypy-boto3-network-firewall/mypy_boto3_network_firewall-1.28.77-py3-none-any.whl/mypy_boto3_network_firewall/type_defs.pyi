"""
Type annotations for network-firewall service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_network_firewall/type_defs/)

Usage::

    ```python
    from mypy_boto3_network_firewall.type_defs import AddressTypeDef

    data: AddressTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AttachmentStatusType,
    ConfigurationSyncStateType,
    EncryptionTypeType,
    FirewallStatusValueType,
    GeneratedRulesTypeType,
    IdentifiedTypeType,
    IPAddressTypeType,
    LogDestinationTypeType,
    LogTypeType,
    PerObjectSyncStatusType,
    ResourceManagedStatusType,
    ResourceManagedTypeType,
    ResourceStatusType,
    RevocationCheckActionType,
    RuleGroupTypeType,
    RuleOrderType,
    StatefulActionType,
    StatefulRuleDirectionType,
    StatefulRuleProtocolType,
    StreamExceptionPolicyType,
    TargetTypeType,
    TCPFlagType,
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
    "AddressTypeDef",
    "AnalysisResultTypeDef",
    "AssociateFirewallPolicyRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SubnetMappingTypeDef",
    "AttachmentTypeDef",
    "IPSetMetadataTypeDef",
    "CheckCertificateRevocationStatusActionsTypeDef",
    "EncryptionConfigurationTypeDef",
    "TagTypeDef",
    "SourceMetadataTypeDef",
    "DeleteFirewallPolicyRequestRequestTypeDef",
    "DeleteFirewallRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteRuleGroupRequestRequestTypeDef",
    "DeleteTLSInspectionConfigurationRequestRequestTypeDef",
    "DescribeFirewallPolicyRequestRequestTypeDef",
    "DescribeFirewallRequestRequestTypeDef",
    "DescribeLoggingConfigurationRequestRequestTypeDef",
    "DescribeResourcePolicyRequestRequestTypeDef",
    "DescribeRuleGroupMetadataRequestRequestTypeDef",
    "StatefulRuleOptionsTypeDef",
    "DescribeRuleGroupRequestRequestTypeDef",
    "DescribeTLSInspectionConfigurationRequestRequestTypeDef",
    "DimensionTypeDef",
    "DisassociateSubnetsRequestRequestTypeDef",
    "FirewallMetadataTypeDef",
    "FirewallPolicyMetadataTypeDef",
    "StatefulEngineOptionsTypeDef",
    "StatelessRuleGroupReferenceTypeDef",
    "HeaderTypeDef",
    "IPSetReferenceTypeDef",
    "IPSetTypeDef",
    "PaginatorConfigTypeDef",
    "ListFirewallPoliciesRequestRequestTypeDef",
    "ListFirewallsRequestRequestTypeDef",
    "ListRuleGroupsRequestRequestTypeDef",
    "RuleGroupMetadataTypeDef",
    "ListTLSInspectionConfigurationsRequestRequestTypeDef",
    "TLSInspectionConfigurationMetadataTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "LogDestinationConfigTypeDef",
    "PortRangeTypeDef",
    "TCPFlagFieldTypeDef",
    "PerObjectStatusTypeDef",
    "PortSetTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "RuleOptionTypeDef",
    "RulesSourceListTypeDef",
    "ServerCertificateTypeDef",
    "StatefulRuleGroupOverrideTypeDef",
    "TlsCertificateDataTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFirewallDeleteProtectionRequestRequestTypeDef",
    "UpdateFirewallDescriptionRequestRequestTypeDef",
    "UpdateFirewallPolicyChangeProtectionRequestRequestTypeDef",
    "UpdateSubnetChangeProtectionRequestRequestTypeDef",
    "AssociateFirewallPolicyResponseTypeDef",
    "DescribeResourcePolicyResponseTypeDef",
    "UpdateFirewallDeleteProtectionResponseTypeDef",
    "UpdateFirewallDescriptionResponseTypeDef",
    "UpdateFirewallPolicyChangeProtectionResponseTypeDef",
    "UpdateSubnetChangeProtectionResponseTypeDef",
    "AssociateSubnetsRequestRequestTypeDef",
    "AssociateSubnetsResponseTypeDef",
    "DisassociateSubnetsResponseTypeDef",
    "CIDRSummaryTypeDef",
    "UpdateFirewallEncryptionConfigurationRequestRequestTypeDef",
    "UpdateFirewallEncryptionConfigurationResponseTypeDef",
    "CreateFirewallRequestRequestTypeDef",
    "FirewallPolicyResponseTypeDef",
    "FirewallTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "RuleGroupResponseTypeDef",
    "DescribeRuleGroupMetadataResponseTypeDef",
    "PublishMetricActionTypeDef",
    "ListFirewallsResponseTypeDef",
    "ListFirewallPoliciesResponseTypeDef",
    "ReferenceSetsTypeDef",
    "PolicyVariablesTypeDef",
    "ListFirewallPoliciesRequestListFirewallPoliciesPaginateTypeDef",
    "ListFirewallsRequestListFirewallsPaginateTypeDef",
    "ListRuleGroupsRequestListRuleGroupsPaginateTypeDef",
    "ListTLSInspectionConfigurationsRequestListTLSInspectionConfigurationsPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListRuleGroupsResponseTypeDef",
    "ListTLSInspectionConfigurationsResponseTypeDef",
    "LoggingConfigurationTypeDef",
    "ServerCertificateScopeTypeDef",
    "MatchAttributesTypeDef",
    "SyncStateTypeDef",
    "RuleVariablesTypeDef",
    "StatefulRuleTypeDef",
    "StatefulRuleGroupReferenceTypeDef",
    "TLSInspectionConfigurationResponseTypeDef",
    "CapacityUsageSummaryTypeDef",
    "CreateFirewallPolicyResponseTypeDef",
    "DeleteFirewallPolicyResponseTypeDef",
    "UpdateFirewallPolicyResponseTypeDef",
    "CreateRuleGroupResponseTypeDef",
    "DeleteRuleGroupResponseTypeDef",
    "UpdateRuleGroupResponseTypeDef",
    "ActionDefinitionTypeDef",
    "DescribeLoggingConfigurationResponseTypeDef",
    "UpdateLoggingConfigurationRequestRequestTypeDef",
    "UpdateLoggingConfigurationResponseTypeDef",
    "ServerCertificateConfigurationTypeDef",
    "RuleDefinitionTypeDef",
    "CreateTLSInspectionConfigurationResponseTypeDef",
    "DeleteTLSInspectionConfigurationResponseTypeDef",
    "UpdateTLSInspectionConfigurationResponseTypeDef",
    "FirewallStatusTypeDef",
    "CustomActionTypeDef",
    "TLSInspectionConfigurationTypeDef",
    "StatelessRuleTypeDef",
    "CreateFirewallResponseTypeDef",
    "DeleteFirewallResponseTypeDef",
    "DescribeFirewallResponseTypeDef",
    "FirewallPolicyTypeDef",
    "CreateTLSInspectionConfigurationRequestRequestTypeDef",
    "DescribeTLSInspectionConfigurationResponseTypeDef",
    "UpdateTLSInspectionConfigurationRequestRequestTypeDef",
    "StatelessRulesAndCustomActionsTypeDef",
    "CreateFirewallPolicyRequestRequestTypeDef",
    "DescribeFirewallPolicyResponseTypeDef",
    "UpdateFirewallPolicyRequestRequestTypeDef",
    "RulesSourceTypeDef",
    "RuleGroupTypeDef",
    "CreateRuleGroupRequestRequestTypeDef",
    "DescribeRuleGroupResponseTypeDef",
    "UpdateRuleGroupRequestRequestTypeDef",
)

AddressTypeDef = TypedDict(
    "AddressTypeDef",
    {
        "AddressDefinition": str,
    },
)

AnalysisResultTypeDef = TypedDict(
    "AnalysisResultTypeDef",
    {
        "IdentifiedRuleIds": NotRequired[List[str]],
        "IdentifiedType": NotRequired[IdentifiedTypeType],
        "AnalysisDetail": NotRequired[str],
    },
)

AssociateFirewallPolicyRequestRequestTypeDef = TypedDict(
    "AssociateFirewallPolicyRequestRequestTypeDef",
    {
        "FirewallPolicyArn": str,
        "UpdateToken": NotRequired[str],
        "FirewallArn": NotRequired[str],
        "FirewallName": NotRequired[str],
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

SubnetMappingTypeDef = TypedDict(
    "SubnetMappingTypeDef",
    {
        "SubnetId": str,
        "IPAddressType": NotRequired[IPAddressTypeType],
    },
)

AttachmentTypeDef = TypedDict(
    "AttachmentTypeDef",
    {
        "SubnetId": NotRequired[str],
        "EndpointId": NotRequired[str],
        "Status": NotRequired[AttachmentStatusType],
        "StatusMessage": NotRequired[str],
    },
)

IPSetMetadataTypeDef = TypedDict(
    "IPSetMetadataTypeDef",
    {
        "ResolvedCIDRCount": NotRequired[int],
    },
)

CheckCertificateRevocationStatusActionsTypeDef = TypedDict(
    "CheckCertificateRevocationStatusActionsTypeDef",
    {
        "RevokedStatusAction": NotRequired[RevocationCheckActionType],
        "UnknownStatusAction": NotRequired[RevocationCheckActionType],
    },
)

EncryptionConfigurationTypeDef = TypedDict(
    "EncryptionConfigurationTypeDef",
    {
        "Type": EncryptionTypeType,
        "KeyId": NotRequired[str],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

SourceMetadataTypeDef = TypedDict(
    "SourceMetadataTypeDef",
    {
        "SourceArn": NotRequired[str],
        "SourceUpdateToken": NotRequired[str],
    },
)

DeleteFirewallPolicyRequestRequestTypeDef = TypedDict(
    "DeleteFirewallPolicyRequestRequestTypeDef",
    {
        "FirewallPolicyName": NotRequired[str],
        "FirewallPolicyArn": NotRequired[str],
    },
)

DeleteFirewallRequestRequestTypeDef = TypedDict(
    "DeleteFirewallRequestRequestTypeDef",
    {
        "FirewallName": NotRequired[str],
        "FirewallArn": NotRequired[str],
    },
)

DeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "DeleteResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DeleteRuleGroupRequestRequestTypeDef = TypedDict(
    "DeleteRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupName": NotRequired[str],
        "RuleGroupArn": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
    },
)

DeleteTLSInspectionConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteTLSInspectionConfigurationRequestRequestTypeDef",
    {
        "TLSInspectionConfigurationArn": NotRequired[str],
        "TLSInspectionConfigurationName": NotRequired[str],
    },
)

DescribeFirewallPolicyRequestRequestTypeDef = TypedDict(
    "DescribeFirewallPolicyRequestRequestTypeDef",
    {
        "FirewallPolicyName": NotRequired[str],
        "FirewallPolicyArn": NotRequired[str],
    },
)

DescribeFirewallRequestRequestTypeDef = TypedDict(
    "DescribeFirewallRequestRequestTypeDef",
    {
        "FirewallName": NotRequired[str],
        "FirewallArn": NotRequired[str],
    },
)

DescribeLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeLoggingConfigurationRequestRequestTypeDef",
    {
        "FirewallArn": NotRequired[str],
        "FirewallName": NotRequired[str],
    },
)

DescribeResourcePolicyRequestRequestTypeDef = TypedDict(
    "DescribeResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DescribeRuleGroupMetadataRequestRequestTypeDef = TypedDict(
    "DescribeRuleGroupMetadataRequestRequestTypeDef",
    {
        "RuleGroupName": NotRequired[str],
        "RuleGroupArn": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
    },
)

StatefulRuleOptionsTypeDef = TypedDict(
    "StatefulRuleOptionsTypeDef",
    {
        "RuleOrder": NotRequired[RuleOrderType],
    },
)

DescribeRuleGroupRequestRequestTypeDef = TypedDict(
    "DescribeRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupName": NotRequired[str],
        "RuleGroupArn": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
        "AnalyzeRuleGroup": NotRequired[bool],
    },
)

DescribeTLSInspectionConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeTLSInspectionConfigurationRequestRequestTypeDef",
    {
        "TLSInspectionConfigurationArn": NotRequired[str],
        "TLSInspectionConfigurationName": NotRequired[str],
    },
)

DimensionTypeDef = TypedDict(
    "DimensionTypeDef",
    {
        "Value": str,
    },
)

DisassociateSubnetsRequestRequestTypeDef = TypedDict(
    "DisassociateSubnetsRequestRequestTypeDef",
    {
        "SubnetIds": Sequence[str],
        "UpdateToken": NotRequired[str],
        "FirewallArn": NotRequired[str],
        "FirewallName": NotRequired[str],
    },
)

FirewallMetadataTypeDef = TypedDict(
    "FirewallMetadataTypeDef",
    {
        "FirewallName": NotRequired[str],
        "FirewallArn": NotRequired[str],
    },
)

FirewallPolicyMetadataTypeDef = TypedDict(
    "FirewallPolicyMetadataTypeDef",
    {
        "Name": NotRequired[str],
        "Arn": NotRequired[str],
    },
)

StatefulEngineOptionsTypeDef = TypedDict(
    "StatefulEngineOptionsTypeDef",
    {
        "RuleOrder": NotRequired[RuleOrderType],
        "StreamExceptionPolicy": NotRequired[StreamExceptionPolicyType],
    },
)

StatelessRuleGroupReferenceTypeDef = TypedDict(
    "StatelessRuleGroupReferenceTypeDef",
    {
        "ResourceArn": str,
        "Priority": int,
    },
)

HeaderTypeDef = TypedDict(
    "HeaderTypeDef",
    {
        "Protocol": StatefulRuleProtocolType,
        "Source": str,
        "SourcePort": str,
        "Direction": StatefulRuleDirectionType,
        "Destination": str,
        "DestinationPort": str,
    },
)

IPSetReferenceTypeDef = TypedDict(
    "IPSetReferenceTypeDef",
    {
        "ReferenceArn": NotRequired[str],
    },
)

IPSetTypeDef = TypedDict(
    "IPSetTypeDef",
    {
        "Definition": Sequence[str],
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

ListFirewallPoliciesRequestRequestTypeDef = TypedDict(
    "ListFirewallPoliciesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListFirewallsRequestRequestTypeDef = TypedDict(
    "ListFirewallsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "VpcIds": NotRequired[Sequence[str]],
        "MaxResults": NotRequired[int],
    },
)

ListRuleGroupsRequestRequestTypeDef = TypedDict(
    "ListRuleGroupsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Scope": NotRequired[ResourceManagedStatusType],
        "ManagedType": NotRequired[ResourceManagedTypeType],
        "Type": NotRequired[RuleGroupTypeType],
    },
)

RuleGroupMetadataTypeDef = TypedDict(
    "RuleGroupMetadataTypeDef",
    {
        "Name": NotRequired[str],
        "Arn": NotRequired[str],
    },
)

ListTLSInspectionConfigurationsRequestRequestTypeDef = TypedDict(
    "ListTLSInspectionConfigurationsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

TLSInspectionConfigurationMetadataTypeDef = TypedDict(
    "TLSInspectionConfigurationMetadataTypeDef",
    {
        "Name": NotRequired[str],
        "Arn": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

LogDestinationConfigTypeDef = TypedDict(
    "LogDestinationConfigTypeDef",
    {
        "LogType": LogTypeType,
        "LogDestinationType": LogDestinationTypeType,
        "LogDestination": Dict[str, str],
    },
)

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
    },
)

TCPFlagFieldTypeDef = TypedDict(
    "TCPFlagFieldTypeDef",
    {
        "Flags": Sequence[TCPFlagType],
        "Masks": NotRequired[Sequence[TCPFlagType]],
    },
)

PerObjectStatusTypeDef = TypedDict(
    "PerObjectStatusTypeDef",
    {
        "SyncStatus": NotRequired[PerObjectSyncStatusType],
        "UpdateToken": NotRequired[str],
    },
)

PortSetTypeDef = TypedDict(
    "PortSetTypeDef",
    {
        "Definition": NotRequired[Sequence[str]],
    },
)

PutResourcePolicyRequestRequestTypeDef = TypedDict(
    "PutResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Policy": str,
    },
)

RuleOptionTypeDef = TypedDict(
    "RuleOptionTypeDef",
    {
        "Keyword": str,
        "Settings": NotRequired[Sequence[str]],
    },
)

RulesSourceListTypeDef = TypedDict(
    "RulesSourceListTypeDef",
    {
        "Targets": Sequence[str],
        "TargetTypes": Sequence[TargetTypeType],
        "GeneratedRulesType": GeneratedRulesTypeType,
    },
)

ServerCertificateTypeDef = TypedDict(
    "ServerCertificateTypeDef",
    {
        "ResourceArn": NotRequired[str],
    },
)

StatefulRuleGroupOverrideTypeDef = TypedDict(
    "StatefulRuleGroupOverrideTypeDef",
    {
        "Action": NotRequired[Literal["DROP_TO_ALERT"]],
    },
)

TlsCertificateDataTypeDef = TypedDict(
    "TlsCertificateDataTypeDef",
    {
        "CertificateArn": NotRequired[str],
        "CertificateSerial": NotRequired[str],
        "Status": NotRequired[str],
        "StatusMessage": NotRequired[str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateFirewallDeleteProtectionRequestRequestTypeDef = TypedDict(
    "UpdateFirewallDeleteProtectionRequestRequestTypeDef",
    {
        "DeleteProtection": bool,
        "UpdateToken": NotRequired[str],
        "FirewallArn": NotRequired[str],
        "FirewallName": NotRequired[str],
    },
)

UpdateFirewallDescriptionRequestRequestTypeDef = TypedDict(
    "UpdateFirewallDescriptionRequestRequestTypeDef",
    {
        "UpdateToken": NotRequired[str],
        "FirewallArn": NotRequired[str],
        "FirewallName": NotRequired[str],
        "Description": NotRequired[str],
    },
)

UpdateFirewallPolicyChangeProtectionRequestRequestTypeDef = TypedDict(
    "UpdateFirewallPolicyChangeProtectionRequestRequestTypeDef",
    {
        "FirewallPolicyChangeProtection": bool,
        "UpdateToken": NotRequired[str],
        "FirewallArn": NotRequired[str],
        "FirewallName": NotRequired[str],
    },
)

UpdateSubnetChangeProtectionRequestRequestTypeDef = TypedDict(
    "UpdateSubnetChangeProtectionRequestRequestTypeDef",
    {
        "SubnetChangeProtection": bool,
        "UpdateToken": NotRequired[str],
        "FirewallArn": NotRequired[str],
        "FirewallName": NotRequired[str],
    },
)

AssociateFirewallPolicyResponseTypeDef = TypedDict(
    "AssociateFirewallPolicyResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "FirewallPolicyArn": str,
        "UpdateToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeResourcePolicyResponseTypeDef = TypedDict(
    "DescribeResourcePolicyResponseTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallDeleteProtectionResponseTypeDef = TypedDict(
    "UpdateFirewallDeleteProtectionResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "DeleteProtection": bool,
        "UpdateToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallDescriptionResponseTypeDef = TypedDict(
    "UpdateFirewallDescriptionResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "Description": str,
        "UpdateToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallPolicyChangeProtectionResponseTypeDef = TypedDict(
    "UpdateFirewallPolicyChangeProtectionResponseTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
        "FirewallPolicyChangeProtection": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSubnetChangeProtectionResponseTypeDef = TypedDict(
    "UpdateSubnetChangeProtectionResponseTypeDef",
    {
        "UpdateToken": str,
        "FirewallArn": str,
        "FirewallName": str,
        "SubnetChangeProtection": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateSubnetsRequestRequestTypeDef = TypedDict(
    "AssociateSubnetsRequestRequestTypeDef",
    {
        "SubnetMappings": Sequence[SubnetMappingTypeDef],
        "UpdateToken": NotRequired[str],
        "FirewallArn": NotRequired[str],
        "FirewallName": NotRequired[str],
    },
)

AssociateSubnetsResponseTypeDef = TypedDict(
    "AssociateSubnetsResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "SubnetMappings": List[SubnetMappingTypeDef],
        "UpdateToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateSubnetsResponseTypeDef = TypedDict(
    "DisassociateSubnetsResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "SubnetMappings": List[SubnetMappingTypeDef],
        "UpdateToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CIDRSummaryTypeDef = TypedDict(
    "CIDRSummaryTypeDef",
    {
        "AvailableCIDRCount": NotRequired[int],
        "UtilizedCIDRCount": NotRequired[int],
        "IPSetReferences": NotRequired[Dict[str, IPSetMetadataTypeDef]],
    },
)

UpdateFirewallEncryptionConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateFirewallEncryptionConfigurationRequestRequestTypeDef",
    {
        "UpdateToken": NotRequired[str],
        "FirewallArn": NotRequired[str],
        "FirewallName": NotRequired[str],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
    },
)

UpdateFirewallEncryptionConfigurationResponseTypeDef = TypedDict(
    "UpdateFirewallEncryptionConfigurationResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "UpdateToken": str,
        "EncryptionConfiguration": EncryptionConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFirewallRequestRequestTypeDef = TypedDict(
    "CreateFirewallRequestRequestTypeDef",
    {
        "FirewallName": str,
        "FirewallPolicyArn": str,
        "VpcId": str,
        "SubnetMappings": Sequence[SubnetMappingTypeDef],
        "DeleteProtection": NotRequired[bool],
        "SubnetChangeProtection": NotRequired[bool],
        "FirewallPolicyChangeProtection": NotRequired[bool],
        "Description": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
    },
)

FirewallPolicyResponseTypeDef = TypedDict(
    "FirewallPolicyResponseTypeDef",
    {
        "FirewallPolicyName": str,
        "FirewallPolicyArn": str,
        "FirewallPolicyId": str,
        "Description": NotRequired[str],
        "FirewallPolicyStatus": NotRequired[ResourceStatusType],
        "Tags": NotRequired[List[TagTypeDef]],
        "ConsumedStatelessRuleCapacity": NotRequired[int],
        "ConsumedStatefulRuleCapacity": NotRequired[int],
        "NumberOfAssociations": NotRequired[int],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "LastModifiedTime": NotRequired[datetime],
    },
)

FirewallTypeDef = TypedDict(
    "FirewallTypeDef",
    {
        "FirewallPolicyArn": str,
        "VpcId": str,
        "SubnetMappings": List[SubnetMappingTypeDef],
        "FirewallId": str,
        "FirewallName": NotRequired[str],
        "FirewallArn": NotRequired[str],
        "DeleteProtection": NotRequired[bool],
        "SubnetChangeProtection": NotRequired[bool],
        "FirewallPolicyChangeProtection": NotRequired[bool],
        "Description": NotRequired[str],
        "Tags": NotRequired[List[TagTypeDef]],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "NextToken": str,
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

RuleGroupResponseTypeDef = TypedDict(
    "RuleGroupResponseTypeDef",
    {
        "RuleGroupArn": str,
        "RuleGroupName": str,
        "RuleGroupId": str,
        "Description": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
        "Capacity": NotRequired[int],
        "RuleGroupStatus": NotRequired[ResourceStatusType],
        "Tags": NotRequired[List[TagTypeDef]],
        "ConsumedCapacity": NotRequired[int],
        "NumberOfAssociations": NotRequired[int],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "SourceMetadata": NotRequired[SourceMetadataTypeDef],
        "SnsTopic": NotRequired[str],
        "LastModifiedTime": NotRequired[datetime],
        "AnalysisResults": NotRequired[List[AnalysisResultTypeDef]],
    },
)

DescribeRuleGroupMetadataResponseTypeDef = TypedDict(
    "DescribeRuleGroupMetadataResponseTypeDef",
    {
        "RuleGroupArn": str,
        "RuleGroupName": str,
        "Description": str,
        "Type": RuleGroupTypeType,
        "Capacity": int,
        "StatefulRuleOptions": StatefulRuleOptionsTypeDef,
        "LastModifiedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PublishMetricActionTypeDef = TypedDict(
    "PublishMetricActionTypeDef",
    {
        "Dimensions": Sequence[DimensionTypeDef],
    },
)

ListFirewallsResponseTypeDef = TypedDict(
    "ListFirewallsResponseTypeDef",
    {
        "NextToken": str,
        "Firewalls": List[FirewallMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFirewallPoliciesResponseTypeDef = TypedDict(
    "ListFirewallPoliciesResponseTypeDef",
    {
        "NextToken": str,
        "FirewallPolicies": List[FirewallPolicyMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReferenceSetsTypeDef = TypedDict(
    "ReferenceSetsTypeDef",
    {
        "IPSetReferences": NotRequired[Mapping[str, IPSetReferenceTypeDef]],
    },
)

PolicyVariablesTypeDef = TypedDict(
    "PolicyVariablesTypeDef",
    {
        "RuleVariables": NotRequired[Mapping[str, IPSetTypeDef]],
    },
)

ListFirewallPoliciesRequestListFirewallPoliciesPaginateTypeDef = TypedDict(
    "ListFirewallPoliciesRequestListFirewallPoliciesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListFirewallsRequestListFirewallsPaginateTypeDef = TypedDict(
    "ListFirewallsRequestListFirewallsPaginateTypeDef",
    {
        "VpcIds": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListRuleGroupsRequestListRuleGroupsPaginateTypeDef = TypedDict(
    "ListRuleGroupsRequestListRuleGroupsPaginateTypeDef",
    {
        "Scope": NotRequired[ResourceManagedStatusType],
        "ManagedType": NotRequired[ResourceManagedTypeType],
        "Type": NotRequired[RuleGroupTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTLSInspectionConfigurationsRequestListTLSInspectionConfigurationsPaginateTypeDef = TypedDict(
    "ListTLSInspectionConfigurationsRequestListTLSInspectionConfigurationsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListRuleGroupsResponseTypeDef = TypedDict(
    "ListRuleGroupsResponseTypeDef",
    {
        "NextToken": str,
        "RuleGroups": List[RuleGroupMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTLSInspectionConfigurationsResponseTypeDef = TypedDict(
    "ListTLSInspectionConfigurationsResponseTypeDef",
    {
        "NextToken": str,
        "TLSInspectionConfigurations": List[TLSInspectionConfigurationMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LoggingConfigurationTypeDef = TypedDict(
    "LoggingConfigurationTypeDef",
    {
        "LogDestinationConfigs": List[LogDestinationConfigTypeDef],
    },
)

ServerCertificateScopeTypeDef = TypedDict(
    "ServerCertificateScopeTypeDef",
    {
        "Sources": NotRequired[Sequence[AddressTypeDef]],
        "Destinations": NotRequired[Sequence[AddressTypeDef]],
        "SourcePorts": NotRequired[Sequence[PortRangeTypeDef]],
        "DestinationPorts": NotRequired[Sequence[PortRangeTypeDef]],
        "Protocols": NotRequired[Sequence[int]],
    },
)

MatchAttributesTypeDef = TypedDict(
    "MatchAttributesTypeDef",
    {
        "Sources": NotRequired[Sequence[AddressTypeDef]],
        "Destinations": NotRequired[Sequence[AddressTypeDef]],
        "SourcePorts": NotRequired[Sequence[PortRangeTypeDef]],
        "DestinationPorts": NotRequired[Sequence[PortRangeTypeDef]],
        "Protocols": NotRequired[Sequence[int]],
        "TCPFlags": NotRequired[Sequence[TCPFlagFieldTypeDef]],
    },
)

SyncStateTypeDef = TypedDict(
    "SyncStateTypeDef",
    {
        "Attachment": NotRequired[AttachmentTypeDef],
        "Config": NotRequired[Dict[str, PerObjectStatusTypeDef]],
    },
)

RuleVariablesTypeDef = TypedDict(
    "RuleVariablesTypeDef",
    {
        "IPSets": NotRequired[Mapping[str, IPSetTypeDef]],
        "PortSets": NotRequired[Mapping[str, PortSetTypeDef]],
    },
)

StatefulRuleTypeDef = TypedDict(
    "StatefulRuleTypeDef",
    {
        "Action": StatefulActionType,
        "Header": HeaderTypeDef,
        "RuleOptions": Sequence[RuleOptionTypeDef],
    },
)

StatefulRuleGroupReferenceTypeDef = TypedDict(
    "StatefulRuleGroupReferenceTypeDef",
    {
        "ResourceArn": str,
        "Priority": NotRequired[int],
        "Override": NotRequired[StatefulRuleGroupOverrideTypeDef],
    },
)

TLSInspectionConfigurationResponseTypeDef = TypedDict(
    "TLSInspectionConfigurationResponseTypeDef",
    {
        "TLSInspectionConfigurationArn": str,
        "TLSInspectionConfigurationName": str,
        "TLSInspectionConfigurationId": str,
        "TLSInspectionConfigurationStatus": NotRequired[ResourceStatusType],
        "Description": NotRequired[str],
        "Tags": NotRequired[List[TagTypeDef]],
        "LastModifiedTime": NotRequired[datetime],
        "NumberOfAssociations": NotRequired[int],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "Certificates": NotRequired[List[TlsCertificateDataTypeDef]],
        "CertificateAuthority": NotRequired[TlsCertificateDataTypeDef],
    },
)

CapacityUsageSummaryTypeDef = TypedDict(
    "CapacityUsageSummaryTypeDef",
    {
        "CIDRs": NotRequired[CIDRSummaryTypeDef],
    },
)

CreateFirewallPolicyResponseTypeDef = TypedDict(
    "CreateFirewallPolicyResponseTypeDef",
    {
        "UpdateToken": str,
        "FirewallPolicyResponse": FirewallPolicyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFirewallPolicyResponseTypeDef = TypedDict(
    "DeleteFirewallPolicyResponseTypeDef",
    {
        "FirewallPolicyResponse": FirewallPolicyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallPolicyResponseTypeDef = TypedDict(
    "UpdateFirewallPolicyResponseTypeDef",
    {
        "UpdateToken": str,
        "FirewallPolicyResponse": FirewallPolicyResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRuleGroupResponseTypeDef = TypedDict(
    "CreateRuleGroupResponseTypeDef",
    {
        "UpdateToken": str,
        "RuleGroupResponse": RuleGroupResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRuleGroupResponseTypeDef = TypedDict(
    "DeleteRuleGroupResponseTypeDef",
    {
        "RuleGroupResponse": RuleGroupResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRuleGroupResponseTypeDef = TypedDict(
    "UpdateRuleGroupResponseTypeDef",
    {
        "UpdateToken": str,
        "RuleGroupResponse": RuleGroupResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ActionDefinitionTypeDef = TypedDict(
    "ActionDefinitionTypeDef",
    {
        "PublishMetricAction": NotRequired[PublishMetricActionTypeDef],
    },
)

DescribeLoggingConfigurationResponseTypeDef = TypedDict(
    "DescribeLoggingConfigurationResponseTypeDef",
    {
        "FirewallArn": str,
        "LoggingConfiguration": LoggingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateLoggingConfigurationRequestRequestTypeDef",
    {
        "FirewallArn": NotRequired[str],
        "FirewallName": NotRequired[str],
        "LoggingConfiguration": NotRequired[LoggingConfigurationTypeDef],
    },
)

UpdateLoggingConfigurationResponseTypeDef = TypedDict(
    "UpdateLoggingConfigurationResponseTypeDef",
    {
        "FirewallArn": str,
        "FirewallName": str,
        "LoggingConfiguration": LoggingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ServerCertificateConfigurationTypeDef = TypedDict(
    "ServerCertificateConfigurationTypeDef",
    {
        "ServerCertificates": NotRequired[Sequence[ServerCertificateTypeDef]],
        "Scopes": NotRequired[Sequence[ServerCertificateScopeTypeDef]],
        "CertificateAuthorityArn": NotRequired[str],
        "CheckCertificateRevocationStatus": NotRequired[
            CheckCertificateRevocationStatusActionsTypeDef
        ],
    },
)

RuleDefinitionTypeDef = TypedDict(
    "RuleDefinitionTypeDef",
    {
        "MatchAttributes": MatchAttributesTypeDef,
        "Actions": Sequence[str],
    },
)

CreateTLSInspectionConfigurationResponseTypeDef = TypedDict(
    "CreateTLSInspectionConfigurationResponseTypeDef",
    {
        "UpdateToken": str,
        "TLSInspectionConfigurationResponse": TLSInspectionConfigurationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTLSInspectionConfigurationResponseTypeDef = TypedDict(
    "DeleteTLSInspectionConfigurationResponseTypeDef",
    {
        "TLSInspectionConfigurationResponse": TLSInspectionConfigurationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTLSInspectionConfigurationResponseTypeDef = TypedDict(
    "UpdateTLSInspectionConfigurationResponseTypeDef",
    {
        "UpdateToken": str,
        "TLSInspectionConfigurationResponse": TLSInspectionConfigurationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FirewallStatusTypeDef = TypedDict(
    "FirewallStatusTypeDef",
    {
        "Status": FirewallStatusValueType,
        "ConfigurationSyncStateSummary": ConfigurationSyncStateType,
        "SyncStates": NotRequired[Dict[str, SyncStateTypeDef]],
        "CapacityUsageSummary": NotRequired[CapacityUsageSummaryTypeDef],
    },
)

CustomActionTypeDef = TypedDict(
    "CustomActionTypeDef",
    {
        "ActionName": str,
        "ActionDefinition": ActionDefinitionTypeDef,
    },
)

TLSInspectionConfigurationTypeDef = TypedDict(
    "TLSInspectionConfigurationTypeDef",
    {
        "ServerCertificateConfigurations": NotRequired[
            Sequence[ServerCertificateConfigurationTypeDef]
        ],
    },
)

StatelessRuleTypeDef = TypedDict(
    "StatelessRuleTypeDef",
    {
        "RuleDefinition": RuleDefinitionTypeDef,
        "Priority": int,
    },
)

CreateFirewallResponseTypeDef = TypedDict(
    "CreateFirewallResponseTypeDef",
    {
        "Firewall": FirewallTypeDef,
        "FirewallStatus": FirewallStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFirewallResponseTypeDef = TypedDict(
    "DeleteFirewallResponseTypeDef",
    {
        "Firewall": FirewallTypeDef,
        "FirewallStatus": FirewallStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFirewallResponseTypeDef = TypedDict(
    "DescribeFirewallResponseTypeDef",
    {
        "UpdateToken": str,
        "Firewall": FirewallTypeDef,
        "FirewallStatus": FirewallStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FirewallPolicyTypeDef = TypedDict(
    "FirewallPolicyTypeDef",
    {
        "StatelessDefaultActions": Sequence[str],
        "StatelessFragmentDefaultActions": Sequence[str],
        "StatelessRuleGroupReferences": NotRequired[Sequence[StatelessRuleGroupReferenceTypeDef]],
        "StatelessCustomActions": NotRequired[Sequence[CustomActionTypeDef]],
        "StatefulRuleGroupReferences": NotRequired[Sequence[StatefulRuleGroupReferenceTypeDef]],
        "StatefulDefaultActions": NotRequired[Sequence[str]],
        "StatefulEngineOptions": NotRequired[StatefulEngineOptionsTypeDef],
        "TLSInspectionConfigurationArn": NotRequired[str],
        "PolicyVariables": NotRequired[PolicyVariablesTypeDef],
    },
)

CreateTLSInspectionConfigurationRequestRequestTypeDef = TypedDict(
    "CreateTLSInspectionConfigurationRequestRequestTypeDef",
    {
        "TLSInspectionConfigurationName": str,
        "TLSInspectionConfiguration": TLSInspectionConfigurationTypeDef,
        "Description": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
    },
)

DescribeTLSInspectionConfigurationResponseTypeDef = TypedDict(
    "DescribeTLSInspectionConfigurationResponseTypeDef",
    {
        "UpdateToken": str,
        "TLSInspectionConfiguration": TLSInspectionConfigurationTypeDef,
        "TLSInspectionConfigurationResponse": TLSInspectionConfigurationResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTLSInspectionConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateTLSInspectionConfigurationRequestRequestTypeDef",
    {
        "TLSInspectionConfiguration": TLSInspectionConfigurationTypeDef,
        "UpdateToken": str,
        "TLSInspectionConfigurationArn": NotRequired[str],
        "TLSInspectionConfigurationName": NotRequired[str],
        "Description": NotRequired[str],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
    },
)

StatelessRulesAndCustomActionsTypeDef = TypedDict(
    "StatelessRulesAndCustomActionsTypeDef",
    {
        "StatelessRules": Sequence[StatelessRuleTypeDef],
        "CustomActions": NotRequired[Sequence[CustomActionTypeDef]],
    },
)

CreateFirewallPolicyRequestRequestTypeDef = TypedDict(
    "CreateFirewallPolicyRequestRequestTypeDef",
    {
        "FirewallPolicyName": str,
        "FirewallPolicy": FirewallPolicyTypeDef,
        "Description": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "DryRun": NotRequired[bool],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
    },
)

DescribeFirewallPolicyResponseTypeDef = TypedDict(
    "DescribeFirewallPolicyResponseTypeDef",
    {
        "UpdateToken": str,
        "FirewallPolicyResponse": FirewallPolicyResponseTypeDef,
        "FirewallPolicy": FirewallPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFirewallPolicyRequestRequestTypeDef = TypedDict(
    "UpdateFirewallPolicyRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "FirewallPolicy": FirewallPolicyTypeDef,
        "FirewallPolicyArn": NotRequired[str],
        "FirewallPolicyName": NotRequired[str],
        "Description": NotRequired[str],
        "DryRun": NotRequired[bool],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
    },
)

RulesSourceTypeDef = TypedDict(
    "RulesSourceTypeDef",
    {
        "RulesString": NotRequired[str],
        "RulesSourceList": NotRequired[RulesSourceListTypeDef],
        "StatefulRules": NotRequired[Sequence[StatefulRuleTypeDef]],
        "StatelessRulesAndCustomActions": NotRequired[StatelessRulesAndCustomActionsTypeDef],
    },
)

RuleGroupTypeDef = TypedDict(
    "RuleGroupTypeDef",
    {
        "RulesSource": RulesSourceTypeDef,
        "RuleVariables": NotRequired[RuleVariablesTypeDef],
        "ReferenceSets": NotRequired[ReferenceSetsTypeDef],
        "StatefulRuleOptions": NotRequired[StatefulRuleOptionsTypeDef],
    },
)

CreateRuleGroupRequestRequestTypeDef = TypedDict(
    "CreateRuleGroupRequestRequestTypeDef",
    {
        "RuleGroupName": str,
        "Type": RuleGroupTypeType,
        "Capacity": int,
        "RuleGroup": NotRequired[RuleGroupTypeDef],
        "Rules": NotRequired[str],
        "Description": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "DryRun": NotRequired[bool],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "SourceMetadata": NotRequired[SourceMetadataTypeDef],
        "AnalyzeRuleGroup": NotRequired[bool],
    },
)

DescribeRuleGroupResponseTypeDef = TypedDict(
    "DescribeRuleGroupResponseTypeDef",
    {
        "UpdateToken": str,
        "RuleGroup": RuleGroupTypeDef,
        "RuleGroupResponse": RuleGroupResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRuleGroupRequestRequestTypeDef = TypedDict(
    "UpdateRuleGroupRequestRequestTypeDef",
    {
        "UpdateToken": str,
        "RuleGroupArn": NotRequired[str],
        "RuleGroupName": NotRequired[str],
        "RuleGroup": NotRequired[RuleGroupTypeDef],
        "Rules": NotRequired[str],
        "Type": NotRequired[RuleGroupTypeType],
        "Description": NotRequired[str],
        "DryRun": NotRequired[bool],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "SourceMetadata": NotRequired[SourceMetadataTypeDef],
        "AnalyzeRuleGroup": NotRequired[bool],
    },
)
