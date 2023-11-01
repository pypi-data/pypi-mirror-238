"""
Type annotations for application-insights service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_insights/type_defs/)

Usage::

    ```python
    from mypy_boto3_application_insights.type_defs import WorkloadConfigurationTypeDef

    data: WorkloadConfigurationTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    CloudWatchEventSourceType,
    ConfigurationEventResourceTypeType,
    ConfigurationEventStatusType,
    DiscoveryTypeType,
    FeedbackValueType,
    LogFilterType,
    OsTypeType,
    RecommendationTypeType,
    ResolutionMethodType,
    SeverityLevelType,
    StatusType,
    TierType,
    VisibilityType,
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
    "WorkloadConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "ApplicationComponentTypeDef",
    "ApplicationInfoTypeDef",
    "ConfigurationEventTypeDef",
    "TagTypeDef",
    "CreateComponentRequestRequestTypeDef",
    "CreateLogPatternRequestRequestTypeDef",
    "LogPatternTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteComponentRequestRequestTypeDef",
    "DeleteLogPatternRequestRequestTypeDef",
    "DescribeApplicationRequestRequestTypeDef",
    "DescribeComponentConfigurationRecommendationRequestRequestTypeDef",
    "DescribeComponentConfigurationRequestRequestTypeDef",
    "DescribeComponentRequestRequestTypeDef",
    "DescribeLogPatternRequestRequestTypeDef",
    "DescribeObservationRequestRequestTypeDef",
    "ObservationTypeDef",
    "DescribeProblemObservationsRequestRequestTypeDef",
    "DescribeProblemRequestRequestTypeDef",
    "ProblemTypeDef",
    "DescribeWorkloadRequestRequestTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListComponentsRequestRequestTypeDef",
    "TimestampTypeDef",
    "ListLogPatternSetsRequestRequestTypeDef",
    "ListLogPatternsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWorkloadsRequestRequestTypeDef",
    "WorkloadTypeDef",
    "RemoveWorkloadRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateComponentConfigurationRequestRequestTypeDef",
    "UpdateComponentRequestRequestTypeDef",
    "UpdateLogPatternRequestRequestTypeDef",
    "UpdateProblemRequestRequestTypeDef",
    "AddWorkloadRequestRequestTypeDef",
    "UpdateWorkloadRequestRequestTypeDef",
    "AddWorkloadResponseTypeDef",
    "DescribeComponentConfigurationRecommendationResponseTypeDef",
    "DescribeComponentConfigurationResponseTypeDef",
    "DescribeWorkloadResponseTypeDef",
    "ListLogPatternSetsResponseTypeDef",
    "UpdateWorkloadResponseTypeDef",
    "DescribeComponentResponseTypeDef",
    "ListComponentsResponseTypeDef",
    "CreateApplicationResponseTypeDef",
    "DescribeApplicationResponseTypeDef",
    "ListApplicationsResponseTypeDef",
    "UpdateApplicationResponseTypeDef",
    "ListConfigurationHistoryResponseTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateLogPatternResponseTypeDef",
    "DescribeLogPatternResponseTypeDef",
    "ListLogPatternsResponseTypeDef",
    "UpdateLogPatternResponseTypeDef",
    "DescribeObservationResponseTypeDef",
    "RelatedObservationsTypeDef",
    "DescribeProblemResponseTypeDef",
    "ListProblemsResponseTypeDef",
    "ListConfigurationHistoryRequestRequestTypeDef",
    "ListProblemsRequestRequestTypeDef",
    "ListWorkloadsResponseTypeDef",
    "DescribeProblemObservationsResponseTypeDef",
)

WorkloadConfigurationTypeDef = TypedDict(
    "WorkloadConfigurationTypeDef",
    {
        "WorkloadName": NotRequired[str],
        "Tier": NotRequired[TierType],
        "Configuration": NotRequired[str],
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

ApplicationComponentTypeDef = TypedDict(
    "ApplicationComponentTypeDef",
    {
        "ComponentName": NotRequired[str],
        "ComponentRemarks": NotRequired[str],
        "ResourceType": NotRequired[str],
        "OsType": NotRequired[OsTypeType],
        "Tier": NotRequired[TierType],
        "Monitor": NotRequired[bool],
        "DetectedWorkload": NotRequired[Dict[TierType, Dict[str, str]]],
    },
)

ApplicationInfoTypeDef = TypedDict(
    "ApplicationInfoTypeDef",
    {
        "AccountId": NotRequired[str],
        "ResourceGroupName": NotRequired[str],
        "LifeCycle": NotRequired[str],
        "OpsItemSNSTopicArn": NotRequired[str],
        "OpsCenterEnabled": NotRequired[bool],
        "CWEMonitorEnabled": NotRequired[bool],
        "Remarks": NotRequired[str],
        "AutoConfigEnabled": NotRequired[bool],
        "DiscoveryType": NotRequired[DiscoveryTypeType],
        "AttachMissingPermission": NotRequired[bool],
    },
)

ConfigurationEventTypeDef = TypedDict(
    "ConfigurationEventTypeDef",
    {
        "ResourceGroupName": NotRequired[str],
        "AccountId": NotRequired[str],
        "MonitoredResourceARN": NotRequired[str],
        "EventStatus": NotRequired[ConfigurationEventStatusType],
        "EventResourceType": NotRequired[ConfigurationEventResourceTypeType],
        "EventTime": NotRequired[datetime],
        "EventDetail": NotRequired[str],
        "EventResourceName": NotRequired[str],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

CreateComponentRequestRequestTypeDef = TypedDict(
    "CreateComponentRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "ResourceList": Sequence[str],
    },
)

CreateLogPatternRequestRequestTypeDef = TypedDict(
    "CreateLogPatternRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "PatternSetName": str,
        "PatternName": str,
        "Pattern": str,
        "Rank": int,
    },
)

LogPatternTypeDef = TypedDict(
    "LogPatternTypeDef",
    {
        "PatternSetName": NotRequired[str],
        "PatternName": NotRequired[str],
        "Pattern": NotRequired[str],
        "Rank": NotRequired[int],
    },
)

DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
    },
)

DeleteComponentRequestRequestTypeDef = TypedDict(
    "DeleteComponentRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
    },
)

DeleteLogPatternRequestRequestTypeDef = TypedDict(
    "DeleteLogPatternRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "PatternSetName": str,
        "PatternName": str,
    },
)

DescribeApplicationRequestRequestTypeDef = TypedDict(
    "DescribeApplicationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "AccountId": NotRequired[str],
    },
)

DescribeComponentConfigurationRecommendationRequestRequestTypeDef = TypedDict(
    "DescribeComponentConfigurationRecommendationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "Tier": TierType,
        "WorkloadName": NotRequired[str],
        "RecommendationType": NotRequired[RecommendationTypeType],
    },
)

DescribeComponentConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeComponentConfigurationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "AccountId": NotRequired[str],
    },
)

DescribeComponentRequestRequestTypeDef = TypedDict(
    "DescribeComponentRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "AccountId": NotRequired[str],
    },
)

DescribeLogPatternRequestRequestTypeDef = TypedDict(
    "DescribeLogPatternRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "PatternSetName": str,
        "PatternName": str,
        "AccountId": NotRequired[str],
    },
)

DescribeObservationRequestRequestTypeDef = TypedDict(
    "DescribeObservationRequestRequestTypeDef",
    {
        "ObservationId": str,
        "AccountId": NotRequired[str],
    },
)

ObservationTypeDef = TypedDict(
    "ObservationTypeDef",
    {
        "Id": NotRequired[str],
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "SourceType": NotRequired[str],
        "SourceARN": NotRequired[str],
        "LogGroup": NotRequired[str],
        "LineTime": NotRequired[datetime],
        "LogText": NotRequired[str],
        "LogFilter": NotRequired[LogFilterType],
        "MetricNamespace": NotRequired[str],
        "MetricName": NotRequired[str],
        "Unit": NotRequired[str],
        "Value": NotRequired[float],
        "CloudWatchEventId": NotRequired[str],
        "CloudWatchEventSource": NotRequired[CloudWatchEventSourceType],
        "CloudWatchEventDetailType": NotRequired[str],
        "HealthEventArn": NotRequired[str],
        "HealthService": NotRequired[str],
        "HealthEventTypeCode": NotRequired[str],
        "HealthEventTypeCategory": NotRequired[str],
        "HealthEventDescription": NotRequired[str],
        "CodeDeployDeploymentId": NotRequired[str],
        "CodeDeployDeploymentGroup": NotRequired[str],
        "CodeDeployState": NotRequired[str],
        "CodeDeployApplication": NotRequired[str],
        "CodeDeployInstanceGroupId": NotRequired[str],
        "Ec2State": NotRequired[str],
        "RdsEventCategories": NotRequired[str],
        "RdsEventMessage": NotRequired[str],
        "S3EventName": NotRequired[str],
        "StatesExecutionArn": NotRequired[str],
        "StatesArn": NotRequired[str],
        "StatesStatus": NotRequired[str],
        "StatesInput": NotRequired[str],
        "EbsEvent": NotRequired[str],
        "EbsResult": NotRequired[str],
        "EbsCause": NotRequired[str],
        "EbsRequestId": NotRequired[str],
        "XRayFaultPercent": NotRequired[int],
        "XRayThrottlePercent": NotRequired[int],
        "XRayErrorPercent": NotRequired[int],
        "XRayRequestCount": NotRequired[int],
        "XRayRequestAverageLatency": NotRequired[int],
        "XRayNodeName": NotRequired[str],
        "XRayNodeType": NotRequired[str],
    },
)

DescribeProblemObservationsRequestRequestTypeDef = TypedDict(
    "DescribeProblemObservationsRequestRequestTypeDef",
    {
        "ProblemId": str,
        "AccountId": NotRequired[str],
    },
)

DescribeProblemRequestRequestTypeDef = TypedDict(
    "DescribeProblemRequestRequestTypeDef",
    {
        "ProblemId": str,
        "AccountId": NotRequired[str],
    },
)

ProblemTypeDef = TypedDict(
    "ProblemTypeDef",
    {
        "Id": NotRequired[str],
        "Title": NotRequired[str],
        "Insights": NotRequired[str],
        "Status": NotRequired[StatusType],
        "AffectedResource": NotRequired[str],
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "SeverityLevel": NotRequired[SeverityLevelType],
        "AccountId": NotRequired[str],
        "ResourceGroupName": NotRequired[str],
        "Feedback": NotRequired[Dict[Literal["INSIGHTS_FEEDBACK"], FeedbackValueType]],
        "RecurringCount": NotRequired[int],
        "LastRecurrenceTime": NotRequired[datetime],
        "Visibility": NotRequired[VisibilityType],
        "ResolutionMethod": NotRequired[ResolutionMethodType],
    },
)

DescribeWorkloadRequestRequestTypeDef = TypedDict(
    "DescribeWorkloadRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "WorkloadId": str,
        "AccountId": NotRequired[str],
    },
)

ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "AccountId": NotRequired[str],
    },
)

ListComponentsRequestRequestTypeDef = TypedDict(
    "ListComponentsRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "AccountId": NotRequired[str],
    },
)

TimestampTypeDef = Union[datetime, str]
ListLogPatternSetsRequestRequestTypeDef = TypedDict(
    "ListLogPatternSetsRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "AccountId": NotRequired[str],
    },
)

ListLogPatternsRequestRequestTypeDef = TypedDict(
    "ListLogPatternsRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "PatternSetName": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "AccountId": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

ListWorkloadsRequestRequestTypeDef = TypedDict(
    "ListWorkloadsRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "AccountId": NotRequired[str],
    },
)

WorkloadTypeDef = TypedDict(
    "WorkloadTypeDef",
    {
        "WorkloadId": NotRequired[str],
        "ComponentName": NotRequired[str],
        "WorkloadName": NotRequired[str],
        "Tier": NotRequired[TierType],
        "WorkloadRemarks": NotRequired[str],
    },
)

RemoveWorkloadRequestRequestTypeDef = TypedDict(
    "RemoveWorkloadRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "WorkloadId": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

UpdateApplicationRequestRequestTypeDef = TypedDict(
    "UpdateApplicationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "OpsCenterEnabled": NotRequired[bool],
        "CWEMonitorEnabled": NotRequired[bool],
        "OpsItemSNSTopicArn": NotRequired[str],
        "RemoveSNSTopic": NotRequired[bool],
        "AutoConfigEnabled": NotRequired[bool],
        "AttachMissingPermission": NotRequired[bool],
    },
)

UpdateComponentConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateComponentConfigurationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "Monitor": NotRequired[bool],
        "Tier": NotRequired[TierType],
        "ComponentConfiguration": NotRequired[str],
        "AutoConfigEnabled": NotRequired[bool],
    },
)

UpdateComponentRequestRequestTypeDef = TypedDict(
    "UpdateComponentRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "NewComponentName": NotRequired[str],
        "ResourceList": NotRequired[Sequence[str]],
    },
)

UpdateLogPatternRequestRequestTypeDef = TypedDict(
    "UpdateLogPatternRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "PatternSetName": str,
        "PatternName": str,
        "Pattern": NotRequired[str],
        "Rank": NotRequired[int],
    },
)

UpdateProblemRequestRequestTypeDef = TypedDict(
    "UpdateProblemRequestRequestTypeDef",
    {
        "ProblemId": str,
        "UpdateStatus": NotRequired[Literal["RESOLVED"]],
        "Visibility": NotRequired[VisibilityType],
    },
)

AddWorkloadRequestRequestTypeDef = TypedDict(
    "AddWorkloadRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "WorkloadConfiguration": WorkloadConfigurationTypeDef,
    },
)

UpdateWorkloadRequestRequestTypeDef = TypedDict(
    "UpdateWorkloadRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "WorkloadConfiguration": WorkloadConfigurationTypeDef,
        "WorkloadId": NotRequired[str],
    },
)

AddWorkloadResponseTypeDef = TypedDict(
    "AddWorkloadResponseTypeDef",
    {
        "WorkloadId": str,
        "WorkloadConfiguration": WorkloadConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeComponentConfigurationRecommendationResponseTypeDef = TypedDict(
    "DescribeComponentConfigurationRecommendationResponseTypeDef",
    {
        "ComponentConfiguration": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeComponentConfigurationResponseTypeDef = TypedDict(
    "DescribeComponentConfigurationResponseTypeDef",
    {
        "Monitor": bool,
        "Tier": TierType,
        "ComponentConfiguration": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkloadResponseTypeDef = TypedDict(
    "DescribeWorkloadResponseTypeDef",
    {
        "WorkloadId": str,
        "WorkloadRemarks": str,
        "WorkloadConfiguration": WorkloadConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLogPatternSetsResponseTypeDef = TypedDict(
    "ListLogPatternSetsResponseTypeDef",
    {
        "ResourceGroupName": str,
        "AccountId": str,
        "LogPatternSets": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWorkloadResponseTypeDef = TypedDict(
    "UpdateWorkloadResponseTypeDef",
    {
        "WorkloadId": str,
        "WorkloadConfiguration": WorkloadConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeComponentResponseTypeDef = TypedDict(
    "DescribeComponentResponseTypeDef",
    {
        "ApplicationComponent": ApplicationComponentTypeDef,
        "ResourceList": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListComponentsResponseTypeDef = TypedDict(
    "ListComponentsResponseTypeDef",
    {
        "ApplicationComponentList": List[ApplicationComponentTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "ApplicationInfo": ApplicationInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeApplicationResponseTypeDef = TypedDict(
    "DescribeApplicationResponseTypeDef",
    {
        "ApplicationInfo": ApplicationInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "ApplicationInfoList": List[ApplicationInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApplicationResponseTypeDef = TypedDict(
    "UpdateApplicationResponseTypeDef",
    {
        "ApplicationInfo": ApplicationInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConfigurationHistoryResponseTypeDef = TypedDict(
    "ListConfigurationHistoryResponseTypeDef",
    {
        "EventList": List[ConfigurationEventTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateApplicationRequestRequestTypeDef = TypedDict(
    "CreateApplicationRequestRequestTypeDef",
    {
        "ResourceGroupName": NotRequired[str],
        "OpsCenterEnabled": NotRequired[bool],
        "CWEMonitorEnabled": NotRequired[bool],
        "OpsItemSNSTopicArn": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "AutoConfigEnabled": NotRequired[bool],
        "AutoCreate": NotRequired[bool],
        "GroupingType": NotRequired[Literal["ACCOUNT_BASED"]],
        "AttachMissingPermission": NotRequired[bool],
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
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateLogPatternResponseTypeDef = TypedDict(
    "CreateLogPatternResponseTypeDef",
    {
        "LogPattern": LogPatternTypeDef,
        "ResourceGroupName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLogPatternResponseTypeDef = TypedDict(
    "DescribeLogPatternResponseTypeDef",
    {
        "ResourceGroupName": str,
        "AccountId": str,
        "LogPattern": LogPatternTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLogPatternsResponseTypeDef = TypedDict(
    "ListLogPatternsResponseTypeDef",
    {
        "ResourceGroupName": str,
        "AccountId": str,
        "LogPatterns": List[LogPatternTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateLogPatternResponseTypeDef = TypedDict(
    "UpdateLogPatternResponseTypeDef",
    {
        "ResourceGroupName": str,
        "LogPattern": LogPatternTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeObservationResponseTypeDef = TypedDict(
    "DescribeObservationResponseTypeDef",
    {
        "Observation": ObservationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RelatedObservationsTypeDef = TypedDict(
    "RelatedObservationsTypeDef",
    {
        "ObservationList": NotRequired[List[ObservationTypeDef]],
    },
)

DescribeProblemResponseTypeDef = TypedDict(
    "DescribeProblemResponseTypeDef",
    {
        "Problem": ProblemTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProblemsResponseTypeDef = TypedDict(
    "ListProblemsResponseTypeDef",
    {
        "ProblemList": List[ProblemTypeDef],
        "NextToken": str,
        "ResourceGroupName": str,
        "AccountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConfigurationHistoryRequestRequestTypeDef = TypedDict(
    "ListConfigurationHistoryRequestRequestTypeDef",
    {
        "ResourceGroupName": NotRequired[str],
        "StartTime": NotRequired[TimestampTypeDef],
        "EndTime": NotRequired[TimestampTypeDef],
        "EventStatus": NotRequired[ConfigurationEventStatusType],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "AccountId": NotRequired[str],
    },
)

ListProblemsRequestRequestTypeDef = TypedDict(
    "ListProblemsRequestRequestTypeDef",
    {
        "AccountId": NotRequired[str],
        "ResourceGroupName": NotRequired[str],
        "StartTime": NotRequired[TimestampTypeDef],
        "EndTime": NotRequired[TimestampTypeDef],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "ComponentName": NotRequired[str],
        "Visibility": NotRequired[VisibilityType],
    },
)

ListWorkloadsResponseTypeDef = TypedDict(
    "ListWorkloadsResponseTypeDef",
    {
        "WorkloadList": List[WorkloadTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeProblemObservationsResponseTypeDef = TypedDict(
    "DescribeProblemObservationsResponseTypeDef",
    {
        "RelatedObservations": RelatedObservationsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
