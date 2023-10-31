"""
Type annotations for resiliencehub service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehub/type_defs/)

Usage::

    ```python
    from mypy_boto3_resiliencehub.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AlarmTypeType,
    AppAssessmentScheduleTypeType,
    AppComplianceStatusTypeType,
    AppDriftStatusTypeType,
    AppStatusTypeType,
    AssessmentInvokerType,
    AssessmentStatusType,
    ComplianceStatusType,
    ConfigRecommendationOptimizationTypeType,
    CostFrequencyType,
    DataLocationConstraintType,
    DisruptionTypeType,
    DriftStatusType,
    EstimatedCostTierType,
    EventTypeType,
    ExcludeRecommendationReasonType,
    HaArchitectureType,
    PermissionModelTypeType,
    PhysicalIdentifierTypeType,
    RecommendationComplianceStatusType,
    RecommendationTemplateStatusType,
    RenderRecommendationTypeType,
    ResiliencyPolicyTierType,
    ResourceImportStatusTypeType,
    ResourceImportStrategyTypeType,
    ResourceMappingTypeType,
    ResourceResolutionStatusTypeType,
    ResourceSourceTypeType,
    TemplateFormatType,
    TestRiskType,
    TestTypeType,
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
    "ResponseMetadataTypeDef",
    "RecommendationItemTypeDef",
    "CostTypeDef",
    "DisruptionComplianceTypeDef",
    "ResiliencyScoreTypeDef",
    "AppComponentTypeDef",
    "EksSourceClusterNamespaceTypeDef",
    "TerraformSourceTypeDef",
    "AppSummaryTypeDef",
    "EventSubscriptionTypeDef",
    "PermissionModelTypeDef",
    "AppVersionSummaryTypeDef",
    "BatchUpdateRecommendationStatusFailedEntryTypeDef",
    "UpdateRecommendationStatusItemTypeDef",
    "RecommendationDisruptionComplianceTypeDef",
    "CreateAppVersionAppComponentRequestRequestTypeDef",
    "LogicalResourceIdTypeDef",
    "CreateRecommendationTemplateRequestRequestTypeDef",
    "FailurePolicyTypeDef",
    "DeleteAppAssessmentRequestRequestTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteAppVersionAppComponentRequestRequestTypeDef",
    "DeleteRecommendationTemplateRequestRequestTypeDef",
    "DeleteResiliencyPolicyRequestRequestTypeDef",
    "DescribeAppAssessmentRequestRequestTypeDef",
    "DescribeAppRequestRequestTypeDef",
    "DescribeAppVersionAppComponentRequestRequestTypeDef",
    "DescribeAppVersionRequestRequestTypeDef",
    "DescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef",
    "DescribeAppVersionTemplateRequestRequestTypeDef",
    "DescribeDraftAppVersionResourcesImportStatusRequestRequestTypeDef",
    "DescribeResiliencyPolicyRequestRequestTypeDef",
    "EksSourceTypeDef",
    "ListAlarmRecommendationsRequestRequestTypeDef",
    "ListAppAssessmentComplianceDriftsRequestRequestTypeDef",
    "ListAppAssessmentsRequestRequestTypeDef",
    "ListAppComponentCompliancesRequestRequestTypeDef",
    "ListAppComponentRecommendationsRequestRequestTypeDef",
    "ListAppInputSourcesRequestRequestTypeDef",
    "ListAppVersionAppComponentsRequestRequestTypeDef",
    "ListAppVersionResourceMappingsRequestRequestTypeDef",
    "ListAppVersionResourcesRequestRequestTypeDef",
    "TimestampTypeDef",
    "ListRecommendationTemplatesRequestRequestTypeDef",
    "ListResiliencyPoliciesRequestRequestTypeDef",
    "ListSopRecommendationsRequestRequestTypeDef",
    "ListSuggestedResiliencyPoliciesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTestRecommendationsRequestRequestTypeDef",
    "ListUnsupportedAppVersionResourcesRequestRequestTypeDef",
    "PhysicalResourceIdTypeDef",
    "PublishAppVersionRequestRequestTypeDef",
    "PutDraftAppVersionTemplateRequestRequestTypeDef",
    "S3LocationTypeDef",
    "RemoveDraftAppVersionResourceMappingsRequestRequestTypeDef",
    "ResolveAppVersionResourcesRequestRequestTypeDef",
    "ResourceErrorTypeDef",
    "StartAppAssessmentRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAppVersionAppComponentRequestRequestTypeDef",
    "UpdateAppVersionRequestRequestTypeDef",
    "DeleteAppAssessmentResponseTypeDef",
    "DeleteAppResponseTypeDef",
    "DeleteRecommendationTemplateResponseTypeDef",
    "DeleteResiliencyPolicyResponseTypeDef",
    "DescribeAppVersionResourcesResolutionStatusResponseTypeDef",
    "DescribeAppVersionResponseTypeDef",
    "DescribeAppVersionTemplateResponseTypeDef",
    "DescribeDraftAppVersionResourcesImportStatusResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PublishAppVersionResponseTypeDef",
    "PutDraftAppVersionTemplateResponseTypeDef",
    "RemoveDraftAppVersionResourceMappingsResponseTypeDef",
    "ResolveAppVersionResourcesResponseTypeDef",
    "UpdateAppVersionResponseTypeDef",
    "AlarmRecommendationTypeDef",
    "SopRecommendationTypeDef",
    "TestRecommendationTypeDef",
    "AppAssessmentSummaryTypeDef",
    "ComplianceDriftTypeDef",
    "AppComponentComplianceTypeDef",
    "CreateAppVersionAppComponentResponseTypeDef",
    "DeleteAppVersionAppComponentResponseTypeDef",
    "DescribeAppVersionAppComponentResponseTypeDef",
    "ListAppVersionAppComponentsResponseTypeDef",
    "UpdateAppVersionAppComponentResponseTypeDef",
    "AppInputSourceTypeDef",
    "DeleteAppInputSourceRequestRequestTypeDef",
    "ListAppsResponseTypeDef",
    "AppTypeDef",
    "CreateAppRequestRequestTypeDef",
    "UpdateAppRequestRequestTypeDef",
    "ListAppVersionsResponseTypeDef",
    "BatchUpdateRecommendationStatusSuccessfulEntryTypeDef",
    "UpdateRecommendationStatusRequestEntryTypeDef",
    "ConfigRecommendationTypeDef",
    "CreateAppVersionResourceRequestRequestTypeDef",
    "DeleteAppVersionResourceRequestRequestTypeDef",
    "DescribeAppVersionResourceRequestRequestTypeDef",
    "UpdateAppVersionResourceRequestRequestTypeDef",
    "CreateResiliencyPolicyRequestRequestTypeDef",
    "ResiliencyPolicyTypeDef",
    "UpdateResiliencyPolicyRequestRequestTypeDef",
    "ImportResourcesToDraftAppVersionRequestRequestTypeDef",
    "ImportResourcesToDraftAppVersionResponseTypeDef",
    "ListAppVersionsRequestRequestTypeDef",
    "ListAppsRequestRequestTypeDef",
    "PhysicalResourceTypeDef",
    "ResourceMappingTypeDef",
    "UnsupportedResourceTypeDef",
    "RecommendationTemplateTypeDef",
    "ResourceErrorsDetailsTypeDef",
    "ListAlarmRecommendationsResponseTypeDef",
    "ListSopRecommendationsResponseTypeDef",
    "ListTestRecommendationsResponseTypeDef",
    "ListAppAssessmentsResponseTypeDef",
    "ListAppAssessmentComplianceDriftsResponseTypeDef",
    "ListAppComponentCompliancesResponseTypeDef",
    "DeleteAppInputSourceResponseTypeDef",
    "ListAppInputSourcesResponseTypeDef",
    "CreateAppResponseTypeDef",
    "DescribeAppResponseTypeDef",
    "UpdateAppResponseTypeDef",
    "BatchUpdateRecommendationStatusResponseTypeDef",
    "BatchUpdateRecommendationStatusRequestRequestTypeDef",
    "ComponentRecommendationTypeDef",
    "CreateResiliencyPolicyResponseTypeDef",
    "DescribeResiliencyPolicyResponseTypeDef",
    "ListResiliencyPoliciesResponseTypeDef",
    "ListSuggestedResiliencyPoliciesResponseTypeDef",
    "UpdateResiliencyPolicyResponseTypeDef",
    "CreateAppVersionResourceResponseTypeDef",
    "DeleteAppVersionResourceResponseTypeDef",
    "DescribeAppVersionResourceResponseTypeDef",
    "ListAppVersionResourcesResponseTypeDef",
    "UpdateAppVersionResourceResponseTypeDef",
    "AddDraftAppVersionResourceMappingsRequestRequestTypeDef",
    "AddDraftAppVersionResourceMappingsResponseTypeDef",
    "ListAppVersionResourceMappingsResponseTypeDef",
    "ListUnsupportedAppVersionResourcesResponseTypeDef",
    "CreateRecommendationTemplateResponseTypeDef",
    "ListRecommendationTemplatesResponseTypeDef",
    "AppAssessmentTypeDef",
    "ListAppComponentRecommendationsResponseTypeDef",
    "DescribeAppAssessmentResponseTypeDef",
    "StartAppAssessmentResponseTypeDef",
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

RecommendationItemTypeDef = TypedDict(
    "RecommendationItemTypeDef",
    {
        "alreadyImplemented": NotRequired[bool],
        "excludeReason": NotRequired[ExcludeRecommendationReasonType],
        "excluded": NotRequired[bool],
        "resourceId": NotRequired[str],
        "targetAccountId": NotRequired[str],
        "targetRegion": NotRequired[str],
    },
)

CostTypeDef = TypedDict(
    "CostTypeDef",
    {
        "amount": float,
        "currency": str,
        "frequency": CostFrequencyType,
    },
)

DisruptionComplianceTypeDef = TypedDict(
    "DisruptionComplianceTypeDef",
    {
        "complianceStatus": ComplianceStatusType,
        "achievableRpoInSecs": NotRequired[int],
        "achievableRtoInSecs": NotRequired[int],
        "currentRpoInSecs": NotRequired[int],
        "currentRtoInSecs": NotRequired[int],
        "message": NotRequired[str],
        "rpoDescription": NotRequired[str],
        "rpoReferenceId": NotRequired[str],
        "rtoDescription": NotRequired[str],
        "rtoReferenceId": NotRequired[str],
    },
)

ResiliencyScoreTypeDef = TypedDict(
    "ResiliencyScoreTypeDef",
    {
        "disruptionScore": Dict[DisruptionTypeType, float],
        "score": float,
    },
)

AppComponentTypeDef = TypedDict(
    "AppComponentTypeDef",
    {
        "name": str,
        "type": str,
        "additionalInfo": NotRequired[Dict[str, List[str]]],
        "id": NotRequired[str],
    },
)

EksSourceClusterNamespaceTypeDef = TypedDict(
    "EksSourceClusterNamespaceTypeDef",
    {
        "eksClusterArn": str,
        "namespace": str,
    },
)

TerraformSourceTypeDef = TypedDict(
    "TerraformSourceTypeDef",
    {
        "s3StateFileUrl": str,
    },
)

AppSummaryTypeDef = TypedDict(
    "AppSummaryTypeDef",
    {
        "appArn": str,
        "creationTime": datetime,
        "name": str,
        "assessmentSchedule": NotRequired[AppAssessmentScheduleTypeType],
        "complianceStatus": NotRequired[AppComplianceStatusTypeType],
        "description": NotRequired[str],
        "driftStatus": NotRequired[AppDriftStatusTypeType],
        "lastAppComplianceEvaluationTime": NotRequired[datetime],
        "resiliencyScore": NotRequired[float],
        "rpoInSecs": NotRequired[int],
        "rtoInSecs": NotRequired[int],
        "status": NotRequired[AppStatusTypeType],
    },
)

EventSubscriptionTypeDef = TypedDict(
    "EventSubscriptionTypeDef",
    {
        "eventType": EventTypeType,
        "name": str,
        "snsTopicArn": NotRequired[str],
    },
)

PermissionModelTypeDef = TypedDict(
    "PermissionModelTypeDef",
    {
        "type": PermissionModelTypeType,
        "crossAccountRoleArns": NotRequired[Sequence[str]],
        "invokerRoleName": NotRequired[str],
    },
)

AppVersionSummaryTypeDef = TypedDict(
    "AppVersionSummaryTypeDef",
    {
        "appVersion": str,
        "creationTime": NotRequired[datetime],
        "identifier": NotRequired[int],
        "versionName": NotRequired[str],
    },
)

BatchUpdateRecommendationStatusFailedEntryTypeDef = TypedDict(
    "BatchUpdateRecommendationStatusFailedEntryTypeDef",
    {
        "entryId": str,
        "errorMessage": str,
    },
)

UpdateRecommendationStatusItemTypeDef = TypedDict(
    "UpdateRecommendationStatusItemTypeDef",
    {
        "resourceId": NotRequired[str],
        "targetAccountId": NotRequired[str],
        "targetRegion": NotRequired[str],
    },
)

RecommendationDisruptionComplianceTypeDef = TypedDict(
    "RecommendationDisruptionComplianceTypeDef",
    {
        "expectedComplianceStatus": ComplianceStatusType,
        "expectedRpoDescription": NotRequired[str],
        "expectedRpoInSecs": NotRequired[int],
        "expectedRtoDescription": NotRequired[str],
        "expectedRtoInSecs": NotRequired[int],
    },
)

CreateAppVersionAppComponentRequestRequestTypeDef = TypedDict(
    "CreateAppVersionAppComponentRequestRequestTypeDef",
    {
        "appArn": str,
        "name": str,
        "type": str,
        "additionalInfo": NotRequired[Mapping[str, Sequence[str]]],
        "clientToken": NotRequired[str],
        "id": NotRequired[str],
    },
)

LogicalResourceIdTypeDef = TypedDict(
    "LogicalResourceIdTypeDef",
    {
        "identifier": str,
        "eksSourceName": NotRequired[str],
        "logicalStackName": NotRequired[str],
        "resourceGroupName": NotRequired[str],
        "terraformSourceName": NotRequired[str],
    },
)

CreateRecommendationTemplateRequestRequestTypeDef = TypedDict(
    "CreateRecommendationTemplateRequestRequestTypeDef",
    {
        "assessmentArn": str,
        "name": str,
        "bucketName": NotRequired[str],
        "clientToken": NotRequired[str],
        "format": NotRequired[TemplateFormatType],
        "recommendationIds": NotRequired[Sequence[str]],
        "recommendationTypes": NotRequired[Sequence[RenderRecommendationTypeType]],
        "tags": NotRequired[Mapping[str, str]],
    },
)

FailurePolicyTypeDef = TypedDict(
    "FailurePolicyTypeDef",
    {
        "rpoInSecs": int,
        "rtoInSecs": int,
    },
)

DeleteAppAssessmentRequestRequestTypeDef = TypedDict(
    "DeleteAppAssessmentRequestRequestTypeDef",
    {
        "assessmentArn": str,
        "clientToken": NotRequired[str],
    },
)

DeleteAppRequestRequestTypeDef = TypedDict(
    "DeleteAppRequestRequestTypeDef",
    {
        "appArn": str,
        "clientToken": NotRequired[str],
        "forceDelete": NotRequired[bool],
    },
)

DeleteAppVersionAppComponentRequestRequestTypeDef = TypedDict(
    "DeleteAppVersionAppComponentRequestRequestTypeDef",
    {
        "appArn": str,
        "id": str,
        "clientToken": NotRequired[str],
    },
)

DeleteRecommendationTemplateRequestRequestTypeDef = TypedDict(
    "DeleteRecommendationTemplateRequestRequestTypeDef",
    {
        "recommendationTemplateArn": str,
        "clientToken": NotRequired[str],
    },
)

DeleteResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "DeleteResiliencyPolicyRequestRequestTypeDef",
    {
        "policyArn": str,
        "clientToken": NotRequired[str],
    },
)

DescribeAppAssessmentRequestRequestTypeDef = TypedDict(
    "DescribeAppAssessmentRequestRequestTypeDef",
    {
        "assessmentArn": str,
    },
)

DescribeAppRequestRequestTypeDef = TypedDict(
    "DescribeAppRequestRequestTypeDef",
    {
        "appArn": str,
    },
)

DescribeAppVersionAppComponentRequestRequestTypeDef = TypedDict(
    "DescribeAppVersionAppComponentRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "id": str,
    },
)

DescribeAppVersionRequestRequestTypeDef = TypedDict(
    "DescribeAppVersionRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
    },
)

DescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef = TypedDict(
    "DescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "resolutionId": NotRequired[str],
    },
)

DescribeAppVersionTemplateRequestRequestTypeDef = TypedDict(
    "DescribeAppVersionTemplateRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
    },
)

DescribeDraftAppVersionResourcesImportStatusRequestRequestTypeDef = TypedDict(
    "DescribeDraftAppVersionResourcesImportStatusRequestRequestTypeDef",
    {
        "appArn": str,
    },
)

DescribeResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "DescribeResiliencyPolicyRequestRequestTypeDef",
    {
        "policyArn": str,
    },
)

EksSourceTypeDef = TypedDict(
    "EksSourceTypeDef",
    {
        "eksClusterArn": str,
        "namespaces": Sequence[str],
    },
)

ListAlarmRecommendationsRequestRequestTypeDef = TypedDict(
    "ListAlarmRecommendationsRequestRequestTypeDef",
    {
        "assessmentArn": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListAppAssessmentComplianceDriftsRequestRequestTypeDef = TypedDict(
    "ListAppAssessmentComplianceDriftsRequestRequestTypeDef",
    {
        "assessmentArn": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListAppAssessmentsRequestRequestTypeDef = TypedDict(
    "ListAppAssessmentsRequestRequestTypeDef",
    {
        "appArn": NotRequired[str],
        "assessmentName": NotRequired[str],
        "assessmentStatus": NotRequired[Sequence[AssessmentStatusType]],
        "complianceStatus": NotRequired[ComplianceStatusType],
        "invoker": NotRequired[AssessmentInvokerType],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "reverseOrder": NotRequired[bool],
    },
)

ListAppComponentCompliancesRequestRequestTypeDef = TypedDict(
    "ListAppComponentCompliancesRequestRequestTypeDef",
    {
        "assessmentArn": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListAppComponentRecommendationsRequestRequestTypeDef = TypedDict(
    "ListAppComponentRecommendationsRequestRequestTypeDef",
    {
        "assessmentArn": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListAppInputSourcesRequestRequestTypeDef = TypedDict(
    "ListAppInputSourcesRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListAppVersionAppComponentsRequestRequestTypeDef = TypedDict(
    "ListAppVersionAppComponentsRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListAppVersionResourceMappingsRequestRequestTypeDef = TypedDict(
    "ListAppVersionResourceMappingsRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListAppVersionResourcesRequestRequestTypeDef = TypedDict(
    "ListAppVersionResourcesRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "resolutionId": NotRequired[str],
    },
)

TimestampTypeDef = Union[datetime, str]
ListRecommendationTemplatesRequestRequestTypeDef = TypedDict(
    "ListRecommendationTemplatesRequestRequestTypeDef",
    {
        "assessmentArn": str,
        "maxResults": NotRequired[int],
        "name": NotRequired[str],
        "nextToken": NotRequired[str],
        "recommendationTemplateArn": NotRequired[str],
        "reverseOrder": NotRequired[bool],
        "status": NotRequired[Sequence[RecommendationTemplateStatusType]],
    },
)

ListResiliencyPoliciesRequestRequestTypeDef = TypedDict(
    "ListResiliencyPoliciesRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "policyName": NotRequired[str],
    },
)

ListSopRecommendationsRequestRequestTypeDef = TypedDict(
    "ListSopRecommendationsRequestRequestTypeDef",
    {
        "assessmentArn": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListSuggestedResiliencyPoliciesRequestRequestTypeDef = TypedDict(
    "ListSuggestedResiliencyPoliciesRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTestRecommendationsRequestRequestTypeDef = TypedDict(
    "ListTestRecommendationsRequestRequestTypeDef",
    {
        "assessmentArn": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListUnsupportedAppVersionResourcesRequestRequestTypeDef = TypedDict(
    "ListUnsupportedAppVersionResourcesRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "resolutionId": NotRequired[str],
    },
)

PhysicalResourceIdTypeDef = TypedDict(
    "PhysicalResourceIdTypeDef",
    {
        "identifier": str,
        "type": PhysicalIdentifierTypeType,
        "awsAccountId": NotRequired[str],
        "awsRegion": NotRequired[str],
    },
)

PublishAppVersionRequestRequestTypeDef = TypedDict(
    "PublishAppVersionRequestRequestTypeDef",
    {
        "appArn": str,
        "versionName": NotRequired[str],
    },
)

PutDraftAppVersionTemplateRequestRequestTypeDef = TypedDict(
    "PutDraftAppVersionTemplateRequestRequestTypeDef",
    {
        "appArn": str,
        "appTemplateBody": str,
    },
)

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "bucket": NotRequired[str],
        "prefix": NotRequired[str],
    },
)

RemoveDraftAppVersionResourceMappingsRequestRequestTypeDef = TypedDict(
    "RemoveDraftAppVersionResourceMappingsRequestRequestTypeDef",
    {
        "appArn": str,
        "appRegistryAppNames": NotRequired[Sequence[str]],
        "eksSourceNames": NotRequired[Sequence[str]],
        "logicalStackNames": NotRequired[Sequence[str]],
        "resourceGroupNames": NotRequired[Sequence[str]],
        "resourceNames": NotRequired[Sequence[str]],
        "terraformSourceNames": NotRequired[Sequence[str]],
    },
)

ResolveAppVersionResourcesRequestRequestTypeDef = TypedDict(
    "ResolveAppVersionResourcesRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
    },
)

ResourceErrorTypeDef = TypedDict(
    "ResourceErrorTypeDef",
    {
        "logicalResourceId": NotRequired[str],
        "physicalResourceId": NotRequired[str],
        "reason": NotRequired[str],
    },
)

StartAppAssessmentRequestRequestTypeDef = TypedDict(
    "StartAppAssessmentRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "assessmentName": str,
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
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

UpdateAppVersionAppComponentRequestRequestTypeDef = TypedDict(
    "UpdateAppVersionAppComponentRequestRequestTypeDef",
    {
        "appArn": str,
        "id": str,
        "additionalInfo": NotRequired[Mapping[str, Sequence[str]]],
        "name": NotRequired[str],
        "type": NotRequired[str],
    },
)

UpdateAppVersionRequestRequestTypeDef = TypedDict(
    "UpdateAppVersionRequestRequestTypeDef",
    {
        "appArn": str,
        "additionalInfo": NotRequired[Mapping[str, Sequence[str]]],
    },
)

DeleteAppAssessmentResponseTypeDef = TypedDict(
    "DeleteAppAssessmentResponseTypeDef",
    {
        "assessmentArn": str,
        "assessmentStatus": AssessmentStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAppResponseTypeDef = TypedDict(
    "DeleteAppResponseTypeDef",
    {
        "appArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRecommendationTemplateResponseTypeDef = TypedDict(
    "DeleteRecommendationTemplateResponseTypeDef",
    {
        "recommendationTemplateArn": str,
        "status": RecommendationTemplateStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteResiliencyPolicyResponseTypeDef = TypedDict(
    "DeleteResiliencyPolicyResponseTypeDef",
    {
        "policyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppVersionResourcesResolutionStatusResponseTypeDef = TypedDict(
    "DescribeAppVersionResourcesResolutionStatusResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "errorMessage": str,
        "resolutionId": str,
        "status": ResourceResolutionStatusTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppVersionResponseTypeDef = TypedDict(
    "DescribeAppVersionResponseTypeDef",
    {
        "additionalInfo": Dict[str, List[str]],
        "appArn": str,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppVersionTemplateResponseTypeDef = TypedDict(
    "DescribeAppVersionTemplateResponseTypeDef",
    {
        "appArn": str,
        "appTemplateBody": str,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDraftAppVersionResourcesImportStatusResponseTypeDef = TypedDict(
    "DescribeDraftAppVersionResourcesImportStatusResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "errorMessage": str,
        "status": ResourceImportStatusTypeType,
        "statusChangeTime": datetime,
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

PublishAppVersionResponseTypeDef = TypedDict(
    "PublishAppVersionResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "identifier": int,
        "versionName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDraftAppVersionTemplateResponseTypeDef = TypedDict(
    "PutDraftAppVersionTemplateResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveDraftAppVersionResourceMappingsResponseTypeDef = TypedDict(
    "RemoveDraftAppVersionResourceMappingsResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResolveAppVersionResourcesResponseTypeDef = TypedDict(
    "ResolveAppVersionResourcesResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "resolutionId": str,
        "status": ResourceResolutionStatusTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppVersionResponseTypeDef = TypedDict(
    "UpdateAppVersionResponseTypeDef",
    {
        "additionalInfo": Dict[str, List[str]],
        "appArn": str,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AlarmRecommendationTypeDef = TypedDict(
    "AlarmRecommendationTypeDef",
    {
        "name": str,
        "recommendationId": str,
        "referenceId": str,
        "type": AlarmTypeType,
        "appComponentName": NotRequired[str],
        "appComponentNames": NotRequired[List[str]],
        "description": NotRequired[str],
        "items": NotRequired[List[RecommendationItemTypeDef]],
        "prerequisite": NotRequired[str],
    },
)

SopRecommendationTypeDef = TypedDict(
    "SopRecommendationTypeDef",
    {
        "recommendationId": str,
        "referenceId": str,
        "serviceType": Literal["SSM"],
        "appComponentName": NotRequired[str],
        "description": NotRequired[str],
        "items": NotRequired[List[RecommendationItemTypeDef]],
        "name": NotRequired[str],
        "prerequisite": NotRequired[str],
    },
)

TestRecommendationTypeDef = TypedDict(
    "TestRecommendationTypeDef",
    {
        "referenceId": str,
        "appComponentName": NotRequired[str],
        "dependsOnAlarms": NotRequired[List[str]],
        "description": NotRequired[str],
        "intent": NotRequired[str],
        "items": NotRequired[List[RecommendationItemTypeDef]],
        "name": NotRequired[str],
        "prerequisite": NotRequired[str],
        "recommendationId": NotRequired[str],
        "risk": NotRequired[TestRiskType],
        "type": NotRequired[TestTypeType],
    },
)

AppAssessmentSummaryTypeDef = TypedDict(
    "AppAssessmentSummaryTypeDef",
    {
        "assessmentArn": str,
        "assessmentStatus": AssessmentStatusType,
        "appArn": NotRequired[str],
        "appVersion": NotRequired[str],
        "assessmentName": NotRequired[str],
        "complianceStatus": NotRequired[ComplianceStatusType],
        "cost": NotRequired[CostTypeDef],
        "driftStatus": NotRequired[DriftStatusType],
        "endTime": NotRequired[datetime],
        "invoker": NotRequired[AssessmentInvokerType],
        "message": NotRequired[str],
        "resiliencyScore": NotRequired[float],
        "startTime": NotRequired[datetime],
        "versionName": NotRequired[str],
    },
)

ComplianceDriftTypeDef = TypedDict(
    "ComplianceDriftTypeDef",
    {
        "actualReferenceId": NotRequired[str],
        "actualValue": NotRequired[Dict[DisruptionTypeType, DisruptionComplianceTypeDef]],
        "appId": NotRequired[str],
        "appVersion": NotRequired[str],
        "diffType": NotRequired[Literal["NotEqual"]],
        "driftType": NotRequired[Literal["ApplicationCompliance"]],
        "entityId": NotRequired[str],
        "entityType": NotRequired[str],
        "expectedReferenceId": NotRequired[str],
        "expectedValue": NotRequired[Dict[DisruptionTypeType, DisruptionComplianceTypeDef]],
    },
)

AppComponentComplianceTypeDef = TypedDict(
    "AppComponentComplianceTypeDef",
    {
        "appComponentName": NotRequired[str],
        "compliance": NotRequired[Dict[DisruptionTypeType, DisruptionComplianceTypeDef]],
        "cost": NotRequired[CostTypeDef],
        "message": NotRequired[str],
        "resiliencyScore": NotRequired[ResiliencyScoreTypeDef],
        "status": NotRequired[ComplianceStatusType],
    },
)

CreateAppVersionAppComponentResponseTypeDef = TypedDict(
    "CreateAppVersionAppComponentResponseTypeDef",
    {
        "appArn": str,
        "appComponent": AppComponentTypeDef,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAppVersionAppComponentResponseTypeDef = TypedDict(
    "DeleteAppVersionAppComponentResponseTypeDef",
    {
        "appArn": str,
        "appComponent": AppComponentTypeDef,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppVersionAppComponentResponseTypeDef = TypedDict(
    "DescribeAppVersionAppComponentResponseTypeDef",
    {
        "appArn": str,
        "appComponent": AppComponentTypeDef,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppVersionAppComponentsResponseTypeDef = TypedDict(
    "ListAppVersionAppComponentsResponseTypeDef",
    {
        "appArn": str,
        "appComponents": List[AppComponentTypeDef],
        "appVersion": str,
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppVersionAppComponentResponseTypeDef = TypedDict(
    "UpdateAppVersionAppComponentResponseTypeDef",
    {
        "appArn": str,
        "appComponent": AppComponentTypeDef,
        "appVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AppInputSourceTypeDef = TypedDict(
    "AppInputSourceTypeDef",
    {
        "importType": ResourceMappingTypeType,
        "eksSourceClusterNamespace": NotRequired[EksSourceClusterNamespaceTypeDef],
        "resourceCount": NotRequired[int],
        "sourceArn": NotRequired[str],
        "sourceName": NotRequired[str],
        "terraformSource": NotRequired[TerraformSourceTypeDef],
    },
)

DeleteAppInputSourceRequestRequestTypeDef = TypedDict(
    "DeleteAppInputSourceRequestRequestTypeDef",
    {
        "appArn": str,
        "clientToken": NotRequired[str],
        "eksSourceClusterNamespace": NotRequired[EksSourceClusterNamespaceTypeDef],
        "sourceArn": NotRequired[str],
        "terraformSource": NotRequired[TerraformSourceTypeDef],
    },
)

ListAppsResponseTypeDef = TypedDict(
    "ListAppsResponseTypeDef",
    {
        "appSummaries": List[AppSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AppTypeDef = TypedDict(
    "AppTypeDef",
    {
        "appArn": str,
        "creationTime": datetime,
        "name": str,
        "assessmentSchedule": NotRequired[AppAssessmentScheduleTypeType],
        "complianceStatus": NotRequired[AppComplianceStatusTypeType],
        "description": NotRequired[str],
        "driftStatus": NotRequired[AppDriftStatusTypeType],
        "eventSubscriptions": NotRequired[List[EventSubscriptionTypeDef]],
        "lastAppComplianceEvaluationTime": NotRequired[datetime],
        "lastDriftEvaluationTime": NotRequired[datetime],
        "lastResiliencyScoreEvaluationTime": NotRequired[datetime],
        "permissionModel": NotRequired[PermissionModelTypeDef],
        "policyArn": NotRequired[str],
        "resiliencyScore": NotRequired[float],
        "rpoInSecs": NotRequired[int],
        "rtoInSecs": NotRequired[int],
        "status": NotRequired[AppStatusTypeType],
        "tags": NotRequired[Dict[str, str]],
    },
)

CreateAppRequestRequestTypeDef = TypedDict(
    "CreateAppRequestRequestTypeDef",
    {
        "name": str,
        "assessmentSchedule": NotRequired[AppAssessmentScheduleTypeType],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "eventSubscriptions": NotRequired[Sequence[EventSubscriptionTypeDef]],
        "permissionModel": NotRequired[PermissionModelTypeDef],
        "policyArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

UpdateAppRequestRequestTypeDef = TypedDict(
    "UpdateAppRequestRequestTypeDef",
    {
        "appArn": str,
        "assessmentSchedule": NotRequired[AppAssessmentScheduleTypeType],
        "clearResiliencyPolicyArn": NotRequired[bool],
        "description": NotRequired[str],
        "eventSubscriptions": NotRequired[Sequence[EventSubscriptionTypeDef]],
        "permissionModel": NotRequired[PermissionModelTypeDef],
        "policyArn": NotRequired[str],
    },
)

ListAppVersionsResponseTypeDef = TypedDict(
    "ListAppVersionsResponseTypeDef",
    {
        "appVersions": List[AppVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateRecommendationStatusSuccessfulEntryTypeDef = TypedDict(
    "BatchUpdateRecommendationStatusSuccessfulEntryTypeDef",
    {
        "entryId": str,
        "excluded": bool,
        "item": UpdateRecommendationStatusItemTypeDef,
        "referenceId": str,
        "excludeReason": NotRequired[ExcludeRecommendationReasonType],
    },
)

UpdateRecommendationStatusRequestEntryTypeDef = TypedDict(
    "UpdateRecommendationStatusRequestEntryTypeDef",
    {
        "entryId": str,
        "excluded": bool,
        "item": UpdateRecommendationStatusItemTypeDef,
        "referenceId": str,
        "excludeReason": NotRequired[ExcludeRecommendationReasonType],
    },
)

ConfigRecommendationTypeDef = TypedDict(
    "ConfigRecommendationTypeDef",
    {
        "name": str,
        "optimizationType": ConfigRecommendationOptimizationTypeType,
        "referenceId": str,
        "appComponentName": NotRequired[str],
        "compliance": NotRequired[Dict[DisruptionTypeType, DisruptionComplianceTypeDef]],
        "cost": NotRequired[CostTypeDef],
        "description": NotRequired[str],
        "haArchitecture": NotRequired[HaArchitectureType],
        "recommendationCompliance": NotRequired[
            Dict[DisruptionTypeType, RecommendationDisruptionComplianceTypeDef]
        ],
        "suggestedChanges": NotRequired[List[str]],
    },
)

CreateAppVersionResourceRequestRequestTypeDef = TypedDict(
    "CreateAppVersionResourceRequestRequestTypeDef",
    {
        "appArn": str,
        "appComponents": Sequence[str],
        "logicalResourceId": LogicalResourceIdTypeDef,
        "physicalResourceId": str,
        "resourceType": str,
        "additionalInfo": NotRequired[Mapping[str, Sequence[str]]],
        "awsAccountId": NotRequired[str],
        "awsRegion": NotRequired[str],
        "clientToken": NotRequired[str],
        "resourceName": NotRequired[str],
    },
)

DeleteAppVersionResourceRequestRequestTypeDef = TypedDict(
    "DeleteAppVersionResourceRequestRequestTypeDef",
    {
        "appArn": str,
        "awsAccountId": NotRequired[str],
        "awsRegion": NotRequired[str],
        "clientToken": NotRequired[str],
        "logicalResourceId": NotRequired[LogicalResourceIdTypeDef],
        "physicalResourceId": NotRequired[str],
        "resourceName": NotRequired[str],
    },
)

DescribeAppVersionResourceRequestRequestTypeDef = TypedDict(
    "DescribeAppVersionResourceRequestRequestTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "awsAccountId": NotRequired[str],
        "awsRegion": NotRequired[str],
        "logicalResourceId": NotRequired[LogicalResourceIdTypeDef],
        "physicalResourceId": NotRequired[str],
        "resourceName": NotRequired[str],
    },
)

UpdateAppVersionResourceRequestRequestTypeDef = TypedDict(
    "UpdateAppVersionResourceRequestRequestTypeDef",
    {
        "appArn": str,
        "additionalInfo": NotRequired[Mapping[str, Sequence[str]]],
        "appComponents": NotRequired[Sequence[str]],
        "awsAccountId": NotRequired[str],
        "awsRegion": NotRequired[str],
        "excluded": NotRequired[bool],
        "logicalResourceId": NotRequired[LogicalResourceIdTypeDef],
        "physicalResourceId": NotRequired[str],
        "resourceName": NotRequired[str],
        "resourceType": NotRequired[str],
    },
)

CreateResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "CreateResiliencyPolicyRequestRequestTypeDef",
    {
        "policy": Mapping[DisruptionTypeType, FailurePolicyTypeDef],
        "policyName": str,
        "tier": ResiliencyPolicyTierType,
        "clientToken": NotRequired[str],
        "dataLocationConstraint": NotRequired[DataLocationConstraintType],
        "policyDescription": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

ResiliencyPolicyTypeDef = TypedDict(
    "ResiliencyPolicyTypeDef",
    {
        "creationTime": NotRequired[datetime],
        "dataLocationConstraint": NotRequired[DataLocationConstraintType],
        "estimatedCostTier": NotRequired[EstimatedCostTierType],
        "policy": NotRequired[Dict[DisruptionTypeType, FailurePolicyTypeDef]],
        "policyArn": NotRequired[str],
        "policyDescription": NotRequired[str],
        "policyName": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "tier": NotRequired[ResiliencyPolicyTierType],
    },
)

UpdateResiliencyPolicyRequestRequestTypeDef = TypedDict(
    "UpdateResiliencyPolicyRequestRequestTypeDef",
    {
        "policyArn": str,
        "dataLocationConstraint": NotRequired[DataLocationConstraintType],
        "policy": NotRequired[Mapping[DisruptionTypeType, FailurePolicyTypeDef]],
        "policyDescription": NotRequired[str],
        "policyName": NotRequired[str],
        "tier": NotRequired[ResiliencyPolicyTierType],
    },
)

ImportResourcesToDraftAppVersionRequestRequestTypeDef = TypedDict(
    "ImportResourcesToDraftAppVersionRequestRequestTypeDef",
    {
        "appArn": str,
        "eksSources": NotRequired[Sequence[EksSourceTypeDef]],
        "importStrategy": NotRequired[ResourceImportStrategyTypeType],
        "sourceArns": NotRequired[Sequence[str]],
        "terraformSources": NotRequired[Sequence[TerraformSourceTypeDef]],
    },
)

ImportResourcesToDraftAppVersionResponseTypeDef = TypedDict(
    "ImportResourcesToDraftAppVersionResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "eksSources": List[EksSourceTypeDef],
        "sourceArns": List[str],
        "status": ResourceImportStatusTypeType,
        "terraformSources": List[TerraformSourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppVersionsRequestRequestTypeDef = TypedDict(
    "ListAppVersionsRequestRequestTypeDef",
    {
        "appArn": str,
        "endTime": NotRequired[TimestampTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "startTime": NotRequired[TimestampTypeDef],
    },
)

ListAppsRequestRequestTypeDef = TypedDict(
    "ListAppsRequestRequestTypeDef",
    {
        "appArn": NotRequired[str],
        "fromLastAssessmentTime": NotRequired[TimestampTypeDef],
        "maxResults": NotRequired[int],
        "name": NotRequired[str],
        "nextToken": NotRequired[str],
        "reverseOrder": NotRequired[bool],
        "toLastAssessmentTime": NotRequired[TimestampTypeDef],
    },
)

PhysicalResourceTypeDef = TypedDict(
    "PhysicalResourceTypeDef",
    {
        "logicalResourceId": LogicalResourceIdTypeDef,
        "physicalResourceId": PhysicalResourceIdTypeDef,
        "resourceType": str,
        "additionalInfo": NotRequired[Dict[str, List[str]]],
        "appComponents": NotRequired[List[AppComponentTypeDef]],
        "excluded": NotRequired[bool],
        "parentResourceName": NotRequired[str],
        "resourceName": NotRequired[str],
        "sourceType": NotRequired[ResourceSourceTypeType],
    },
)

ResourceMappingTypeDef = TypedDict(
    "ResourceMappingTypeDef",
    {
        "mappingType": ResourceMappingTypeType,
        "physicalResourceId": PhysicalResourceIdTypeDef,
        "appRegistryAppName": NotRequired[str],
        "eksSourceName": NotRequired[str],
        "logicalStackName": NotRequired[str],
        "resourceGroupName": NotRequired[str],
        "resourceName": NotRequired[str],
        "terraformSourceName": NotRequired[str],
    },
)

UnsupportedResourceTypeDef = TypedDict(
    "UnsupportedResourceTypeDef",
    {
        "logicalResourceId": LogicalResourceIdTypeDef,
        "physicalResourceId": PhysicalResourceIdTypeDef,
        "resourceType": str,
        "unsupportedResourceStatus": NotRequired[str],
    },
)

RecommendationTemplateTypeDef = TypedDict(
    "RecommendationTemplateTypeDef",
    {
        "assessmentArn": str,
        "format": TemplateFormatType,
        "name": str,
        "recommendationTemplateArn": str,
        "recommendationTypes": List[RenderRecommendationTypeType],
        "status": RecommendationTemplateStatusType,
        "appArn": NotRequired[str],
        "endTime": NotRequired[datetime],
        "message": NotRequired[str],
        "needsReplacements": NotRequired[bool],
        "recommendationIds": NotRequired[List[str]],
        "startTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
        "templatesLocation": NotRequired[S3LocationTypeDef],
    },
)

ResourceErrorsDetailsTypeDef = TypedDict(
    "ResourceErrorsDetailsTypeDef",
    {
        "hasMoreErrors": NotRequired[bool],
        "resourceErrors": NotRequired[List[ResourceErrorTypeDef]],
    },
)

ListAlarmRecommendationsResponseTypeDef = TypedDict(
    "ListAlarmRecommendationsResponseTypeDef",
    {
        "alarmRecommendations": List[AlarmRecommendationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSopRecommendationsResponseTypeDef = TypedDict(
    "ListSopRecommendationsResponseTypeDef",
    {
        "nextToken": str,
        "sopRecommendations": List[SopRecommendationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTestRecommendationsResponseTypeDef = TypedDict(
    "ListTestRecommendationsResponseTypeDef",
    {
        "nextToken": str,
        "testRecommendations": List[TestRecommendationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppAssessmentsResponseTypeDef = TypedDict(
    "ListAppAssessmentsResponseTypeDef",
    {
        "assessmentSummaries": List[AppAssessmentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppAssessmentComplianceDriftsResponseTypeDef = TypedDict(
    "ListAppAssessmentComplianceDriftsResponseTypeDef",
    {
        "complianceDrifts": List[ComplianceDriftTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppComponentCompliancesResponseTypeDef = TypedDict(
    "ListAppComponentCompliancesResponseTypeDef",
    {
        "componentCompliances": List[AppComponentComplianceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAppInputSourceResponseTypeDef = TypedDict(
    "DeleteAppInputSourceResponseTypeDef",
    {
        "appArn": str,
        "appInputSource": AppInputSourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppInputSourcesResponseTypeDef = TypedDict(
    "ListAppInputSourcesResponseTypeDef",
    {
        "appInputSources": List[AppInputSourceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppResponseTypeDef = TypedDict(
    "CreateAppResponseTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppResponseTypeDef = TypedDict(
    "DescribeAppResponseTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppResponseTypeDef = TypedDict(
    "UpdateAppResponseTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateRecommendationStatusResponseTypeDef = TypedDict(
    "BatchUpdateRecommendationStatusResponseTypeDef",
    {
        "appArn": str,
        "failedEntries": List[BatchUpdateRecommendationStatusFailedEntryTypeDef],
        "successfulEntries": List[BatchUpdateRecommendationStatusSuccessfulEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateRecommendationStatusRequestRequestTypeDef = TypedDict(
    "BatchUpdateRecommendationStatusRequestRequestTypeDef",
    {
        "appArn": str,
        "requestEntries": Sequence[UpdateRecommendationStatusRequestEntryTypeDef],
    },
)

ComponentRecommendationTypeDef = TypedDict(
    "ComponentRecommendationTypeDef",
    {
        "appComponentName": str,
        "configRecommendations": List[ConfigRecommendationTypeDef],
        "recommendationStatus": RecommendationComplianceStatusType,
    },
)

CreateResiliencyPolicyResponseTypeDef = TypedDict(
    "CreateResiliencyPolicyResponseTypeDef",
    {
        "policy": ResiliencyPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeResiliencyPolicyResponseTypeDef = TypedDict(
    "DescribeResiliencyPolicyResponseTypeDef",
    {
        "policy": ResiliencyPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListResiliencyPoliciesResponseTypeDef = TypedDict(
    "ListResiliencyPoliciesResponseTypeDef",
    {
        "nextToken": str,
        "resiliencyPolicies": List[ResiliencyPolicyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSuggestedResiliencyPoliciesResponseTypeDef = TypedDict(
    "ListSuggestedResiliencyPoliciesResponseTypeDef",
    {
        "nextToken": str,
        "resiliencyPolicies": List[ResiliencyPolicyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateResiliencyPolicyResponseTypeDef = TypedDict(
    "UpdateResiliencyPolicyResponseTypeDef",
    {
        "policy": ResiliencyPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppVersionResourceResponseTypeDef = TypedDict(
    "CreateAppVersionResourceResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "physicalResource": PhysicalResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAppVersionResourceResponseTypeDef = TypedDict(
    "DeleteAppVersionResourceResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "physicalResource": PhysicalResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppVersionResourceResponseTypeDef = TypedDict(
    "DescribeAppVersionResourceResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "physicalResource": PhysicalResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppVersionResourcesResponseTypeDef = TypedDict(
    "ListAppVersionResourcesResponseTypeDef",
    {
        "nextToken": str,
        "physicalResources": List[PhysicalResourceTypeDef],
        "resolutionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppVersionResourceResponseTypeDef = TypedDict(
    "UpdateAppVersionResourceResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "physicalResource": PhysicalResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddDraftAppVersionResourceMappingsRequestRequestTypeDef = TypedDict(
    "AddDraftAppVersionResourceMappingsRequestRequestTypeDef",
    {
        "appArn": str,
        "resourceMappings": Sequence[ResourceMappingTypeDef],
    },
)

AddDraftAppVersionResourceMappingsResponseTypeDef = TypedDict(
    "AddDraftAppVersionResourceMappingsResponseTypeDef",
    {
        "appArn": str,
        "appVersion": str,
        "resourceMappings": List[ResourceMappingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppVersionResourceMappingsResponseTypeDef = TypedDict(
    "ListAppVersionResourceMappingsResponseTypeDef",
    {
        "nextToken": str,
        "resourceMappings": List[ResourceMappingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUnsupportedAppVersionResourcesResponseTypeDef = TypedDict(
    "ListUnsupportedAppVersionResourcesResponseTypeDef",
    {
        "nextToken": str,
        "resolutionId": str,
        "unsupportedResources": List[UnsupportedResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRecommendationTemplateResponseTypeDef = TypedDict(
    "CreateRecommendationTemplateResponseTypeDef",
    {
        "recommendationTemplate": RecommendationTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRecommendationTemplatesResponseTypeDef = TypedDict(
    "ListRecommendationTemplatesResponseTypeDef",
    {
        "nextToken": str,
        "recommendationTemplates": List[RecommendationTemplateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AppAssessmentTypeDef = TypedDict(
    "AppAssessmentTypeDef",
    {
        "assessmentArn": str,
        "assessmentStatus": AssessmentStatusType,
        "invoker": AssessmentInvokerType,
        "appArn": NotRequired[str],
        "appVersion": NotRequired[str],
        "assessmentName": NotRequired[str],
        "compliance": NotRequired[Dict[DisruptionTypeType, DisruptionComplianceTypeDef]],
        "complianceStatus": NotRequired[ComplianceStatusType],
        "cost": NotRequired[CostTypeDef],
        "driftStatus": NotRequired[DriftStatusType],
        "endTime": NotRequired[datetime],
        "message": NotRequired[str],
        "policy": NotRequired[ResiliencyPolicyTypeDef],
        "resiliencyScore": NotRequired[ResiliencyScoreTypeDef],
        "resourceErrorsDetails": NotRequired[ResourceErrorsDetailsTypeDef],
        "startTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
        "versionName": NotRequired[str],
    },
)

ListAppComponentRecommendationsResponseTypeDef = TypedDict(
    "ListAppComponentRecommendationsResponseTypeDef",
    {
        "componentRecommendations": List[ComponentRecommendationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAppAssessmentResponseTypeDef = TypedDict(
    "DescribeAppAssessmentResponseTypeDef",
    {
        "assessment": AppAssessmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAppAssessmentResponseTypeDef = TypedDict(
    "StartAppAssessmentResponseTypeDef",
    {
        "assessment": AppAssessmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
