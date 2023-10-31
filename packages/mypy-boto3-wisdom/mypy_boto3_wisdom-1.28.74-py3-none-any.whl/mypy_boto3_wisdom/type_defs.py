"""
Type annotations for wisdom service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wisdom/type_defs/)

Usage::

    ```python
    from mypy_boto3_wisdom.type_defs import AppIntegrationsConfigurationPaginatorTypeDef

    data: AppIntegrationsConfigurationPaginatorTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AssistantStatusType,
    ContentStatusType,
    KnowledgeBaseStatusType,
    KnowledgeBaseTypeType,
    RecommendationSourceTypeType,
    RelevanceLevelType,
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
    "AppIntegrationsConfigurationPaginatorTypeDef",
    "AppIntegrationsConfigurationTypeDef",
    "AssistantAssociationInputDataTypeDef",
    "KnowledgeBaseAssociationDataTypeDef",
    "AssistantIntegrationConfigurationTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "ContentDataTypeDef",
    "ContentReferenceTypeDef",
    "ContentSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "CreateContentRequestRequestTypeDef",
    "RenderingConfigurationTypeDef",
    "CreateSessionRequestRequestTypeDef",
    "DeleteAssistantAssociationRequestRequestTypeDef",
    "DeleteAssistantRequestRequestTypeDef",
    "DeleteContentRequestRequestTypeDef",
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    "HighlightTypeDef",
    "FilterTypeDef",
    "GetAssistantAssociationRequestRequestTypeDef",
    "GetAssistantRequestRequestTypeDef",
    "GetContentRequestRequestTypeDef",
    "GetContentSummaryRequestRequestTypeDef",
    "GetKnowledgeBaseRequestRequestTypeDef",
    "GetRecommendationsRequestRequestTypeDef",
    "GetSessionRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListAssistantAssociationsRequestRequestTypeDef",
    "ListAssistantsRequestRequestTypeDef",
    "ListContentsRequestRequestTypeDef",
    "ListKnowledgeBasesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "NotifyRecommendationsReceivedErrorTypeDef",
    "NotifyRecommendationsReceivedRequestRequestTypeDef",
    "QueryAssistantRequestRequestTypeDef",
    "QueryRecommendationTriggerDataTypeDef",
    "RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "SessionSummaryTypeDef",
    "SessionIntegrationConfigurationTypeDef",
    "StartContentUploadRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateContentRequestRequestTypeDef",
    "UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "SourceConfigurationPaginatorTypeDef",
    "SourceConfigurationTypeDef",
    "CreateAssistantAssociationRequestRequestTypeDef",
    "AssistantAssociationOutputDataTypeDef",
    "AssistantDataTypeDef",
    "AssistantSummaryTypeDef",
    "CreateAssistantRequestRequestTypeDef",
    "CreateContentResponseTypeDef",
    "GetContentResponseTypeDef",
    "GetContentSummaryResponseTypeDef",
    "ListContentsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SearchContentResponseTypeDef",
    "StartContentUploadResponseTypeDef",
    "UpdateContentResponseTypeDef",
    "DocumentTextTypeDef",
    "SearchExpressionTypeDef",
    "ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef",
    "ListAssistantsRequestListAssistantsPaginateTypeDef",
    "ListContentsRequestListContentsPaginateTypeDef",
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    "QueryAssistantRequestQueryAssistantPaginateTypeDef",
    "NotifyRecommendationsReceivedResponseTypeDef",
    "RecommendationTriggerDataTypeDef",
    "SearchSessionsResponseTypeDef",
    "SessionDataTypeDef",
    "KnowledgeBaseSummaryPaginatorTypeDef",
    "CreateKnowledgeBaseRequestRequestTypeDef",
    "KnowledgeBaseDataTypeDef",
    "KnowledgeBaseSummaryTypeDef",
    "AssistantAssociationDataTypeDef",
    "AssistantAssociationSummaryTypeDef",
    "CreateAssistantResponseTypeDef",
    "GetAssistantResponseTypeDef",
    "ListAssistantsResponseTypeDef",
    "DocumentTypeDef",
    "SearchContentRequestRequestTypeDef",
    "SearchContentRequestSearchContentPaginateTypeDef",
    "SearchSessionsRequestRequestTypeDef",
    "SearchSessionsRequestSearchSessionsPaginateTypeDef",
    "RecommendationTriggerTypeDef",
    "CreateSessionResponseTypeDef",
    "GetSessionResponseTypeDef",
    "ListKnowledgeBasesResponsePaginatorTypeDef",
    "CreateKnowledgeBaseResponseTypeDef",
    "GetKnowledgeBaseResponseTypeDef",
    "UpdateKnowledgeBaseTemplateUriResponseTypeDef",
    "ListKnowledgeBasesResponseTypeDef",
    "CreateAssistantAssociationResponseTypeDef",
    "GetAssistantAssociationResponseTypeDef",
    "ListAssistantAssociationsResponseTypeDef",
    "RecommendationDataTypeDef",
    "ResultDataTypeDef",
    "GetRecommendationsResponseTypeDef",
    "QueryAssistantResponseTypeDef",
)

AppIntegrationsConfigurationPaginatorTypeDef = TypedDict(
    "AppIntegrationsConfigurationPaginatorTypeDef",
    {
        "appIntegrationArn": str,
        "objectFields": NotRequired[List[str]],
    },
)

AppIntegrationsConfigurationTypeDef = TypedDict(
    "AppIntegrationsConfigurationTypeDef",
    {
        "appIntegrationArn": str,
        "objectFields": NotRequired[Sequence[str]],
    },
)

AssistantAssociationInputDataTypeDef = TypedDict(
    "AssistantAssociationInputDataTypeDef",
    {
        "knowledgeBaseId": NotRequired[str],
    },
)

KnowledgeBaseAssociationDataTypeDef = TypedDict(
    "KnowledgeBaseAssociationDataTypeDef",
    {
        "knowledgeBaseArn": NotRequired[str],
        "knowledgeBaseId": NotRequired[str],
    },
)

AssistantIntegrationConfigurationTypeDef = TypedDict(
    "AssistantIntegrationConfigurationTypeDef",
    {
        "topicIntegrationArn": NotRequired[str],
    },
)

ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef",
    {
        "kmsKeyId": NotRequired[str],
    },
)

ContentDataTypeDef = TypedDict(
    "ContentDataTypeDef",
    {
        "contentArn": str,
        "contentId": str,
        "contentType": str,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "metadata": Dict[str, str],
        "name": str,
        "revisionId": str,
        "status": ContentStatusType,
        "title": str,
        "url": str,
        "urlExpiry": datetime,
        "linkOutUri": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)

ContentReferenceTypeDef = TypedDict(
    "ContentReferenceTypeDef",
    {
        "contentArn": NotRequired[str],
        "contentId": NotRequired[str],
        "knowledgeBaseArn": NotRequired[str],
        "knowledgeBaseId": NotRequired[str],
    },
)

ContentSummaryTypeDef = TypedDict(
    "ContentSummaryTypeDef",
    {
        "contentArn": str,
        "contentId": str,
        "contentType": str,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "metadata": Dict[str, str],
        "name": str,
        "revisionId": str,
        "status": ContentStatusType,
        "title": str,
        "tags": NotRequired[Dict[str, str]],
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

CreateContentRequestRequestTypeDef = TypedDict(
    "CreateContentRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "name": str,
        "uploadId": str,
        "clientToken": NotRequired[str],
        "metadata": NotRequired[Mapping[str, str]],
        "overrideLinkOutUri": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "title": NotRequired[str],
    },
)

RenderingConfigurationTypeDef = TypedDict(
    "RenderingConfigurationTypeDef",
    {
        "templateUri": NotRequired[str],
    },
)

CreateSessionRequestRequestTypeDef = TypedDict(
    "CreateSessionRequestRequestTypeDef",
    {
        "assistantId": str,
        "name": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

DeleteAssistantAssociationRequestRequestTypeDef = TypedDict(
    "DeleteAssistantAssociationRequestRequestTypeDef",
    {
        "assistantAssociationId": str,
        "assistantId": str,
    },
)

DeleteAssistantRequestRequestTypeDef = TypedDict(
    "DeleteAssistantRequestRequestTypeDef",
    {
        "assistantId": str,
    },
)

DeleteContentRequestRequestTypeDef = TypedDict(
    "DeleteContentRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
    },
)

DeleteKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)

HighlightTypeDef = TypedDict(
    "HighlightTypeDef",
    {
        "beginOffsetInclusive": NotRequired[int],
        "endOffsetExclusive": NotRequired[int],
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "field": Literal["NAME"],
        "operator": Literal["EQUALS"],
        "value": str,
    },
)

GetAssistantAssociationRequestRequestTypeDef = TypedDict(
    "GetAssistantAssociationRequestRequestTypeDef",
    {
        "assistantAssociationId": str,
        "assistantId": str,
    },
)

GetAssistantRequestRequestTypeDef = TypedDict(
    "GetAssistantRequestRequestTypeDef",
    {
        "assistantId": str,
    },
)

GetContentRequestRequestTypeDef = TypedDict(
    "GetContentRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
    },
)

GetContentSummaryRequestRequestTypeDef = TypedDict(
    "GetContentSummaryRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
    },
)

GetKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "GetKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)

GetRecommendationsRequestRequestTypeDef = TypedDict(
    "GetRecommendationsRequestRequestTypeDef",
    {
        "assistantId": str,
        "sessionId": str,
        "maxResults": NotRequired[int],
        "waitTimeSeconds": NotRequired[int],
    },
)

GetSessionRequestRequestTypeDef = TypedDict(
    "GetSessionRequestRequestTypeDef",
    {
        "assistantId": str,
        "sessionId": str,
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

ListAssistantAssociationsRequestRequestTypeDef = TypedDict(
    "ListAssistantAssociationsRequestRequestTypeDef",
    {
        "assistantId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListAssistantsRequestRequestTypeDef = TypedDict(
    "ListAssistantsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListContentsRequestRequestTypeDef = TypedDict(
    "ListContentsRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListKnowledgeBasesRequestRequestTypeDef = TypedDict(
    "ListKnowledgeBasesRequestRequestTypeDef",
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

NotifyRecommendationsReceivedErrorTypeDef = TypedDict(
    "NotifyRecommendationsReceivedErrorTypeDef",
    {
        "message": NotRequired[str],
        "recommendationId": NotRequired[str],
    },
)

NotifyRecommendationsReceivedRequestRequestTypeDef = TypedDict(
    "NotifyRecommendationsReceivedRequestRequestTypeDef",
    {
        "assistantId": str,
        "recommendationIds": Sequence[str],
        "sessionId": str,
    },
)

QueryAssistantRequestRequestTypeDef = TypedDict(
    "QueryAssistantRequestRequestTypeDef",
    {
        "assistantId": str,
        "queryText": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

QueryRecommendationTriggerDataTypeDef = TypedDict(
    "QueryRecommendationTriggerDataTypeDef",
    {
        "text": NotRequired[str],
    },
)

RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef = TypedDict(
    "RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)

SessionSummaryTypeDef = TypedDict(
    "SessionSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "sessionArn": str,
        "sessionId": str,
    },
)

SessionIntegrationConfigurationTypeDef = TypedDict(
    "SessionIntegrationConfigurationTypeDef",
    {
        "topicIntegrationArn": NotRequired[str],
    },
)

StartContentUploadRequestRequestTypeDef = TypedDict(
    "StartContentUploadRequestRequestTypeDef",
    {
        "contentType": str,
        "knowledgeBaseId": str,
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

UpdateContentRequestRequestTypeDef = TypedDict(
    "UpdateContentRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
        "metadata": NotRequired[Mapping[str, str]],
        "overrideLinkOutUri": NotRequired[str],
        "removeOverrideLinkOutUri": NotRequired[bool],
        "revisionId": NotRequired[str],
        "title": NotRequired[str],
        "uploadId": NotRequired[str],
    },
)

UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef = TypedDict(
    "UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "templateUri": str,
    },
)

SourceConfigurationPaginatorTypeDef = TypedDict(
    "SourceConfigurationPaginatorTypeDef",
    {
        "appIntegrations": NotRequired[AppIntegrationsConfigurationPaginatorTypeDef],
    },
)

SourceConfigurationTypeDef = TypedDict(
    "SourceConfigurationTypeDef",
    {
        "appIntegrations": NotRequired[AppIntegrationsConfigurationTypeDef],
    },
)

CreateAssistantAssociationRequestRequestTypeDef = TypedDict(
    "CreateAssistantAssociationRequestRequestTypeDef",
    {
        "assistantId": str,
        "association": AssistantAssociationInputDataTypeDef,
        "associationType": Literal["KNOWLEDGE_BASE"],
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

AssistantAssociationOutputDataTypeDef = TypedDict(
    "AssistantAssociationOutputDataTypeDef",
    {
        "knowledgeBaseAssociation": NotRequired[KnowledgeBaseAssociationDataTypeDef],
    },
)

AssistantDataTypeDef = TypedDict(
    "AssistantDataTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)

AssistantSummaryTypeDef = TypedDict(
    "AssistantSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)

CreateAssistantRequestRequestTypeDef = TypedDict(
    "CreateAssistantRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["AGENT"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)

CreateContentResponseTypeDef = TypedDict(
    "CreateContentResponseTypeDef",
    {
        "content": ContentDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContentResponseTypeDef = TypedDict(
    "GetContentResponseTypeDef",
    {
        "content": ContentDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContentSummaryResponseTypeDef = TypedDict(
    "GetContentSummaryResponseTypeDef",
    {
        "contentSummary": ContentSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListContentsResponseTypeDef = TypedDict(
    "ListContentsResponseTypeDef",
    {
        "contentSummaries": List[ContentSummaryTypeDef],
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

SearchContentResponseTypeDef = TypedDict(
    "SearchContentResponseTypeDef",
    {
        "contentSummaries": List[ContentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartContentUploadResponseTypeDef = TypedDict(
    "StartContentUploadResponseTypeDef",
    {
        "headersToInclude": Dict[str, str],
        "uploadId": str,
        "url": str,
        "urlExpiry": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateContentResponseTypeDef = TypedDict(
    "UpdateContentResponseTypeDef",
    {
        "content": ContentDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DocumentTextTypeDef = TypedDict(
    "DocumentTextTypeDef",
    {
        "highlights": NotRequired[List[HighlightTypeDef]],
        "text": NotRequired[str],
    },
)

SearchExpressionTypeDef = TypedDict(
    "SearchExpressionTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
    },
)

ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef = TypedDict(
    "ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef",
    {
        "assistantId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAssistantsRequestListAssistantsPaginateTypeDef = TypedDict(
    "ListAssistantsRequestListAssistantsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListContentsRequestListContentsPaginateTypeDef = TypedDict(
    "ListContentsRequestListContentsPaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef = TypedDict(
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

QueryAssistantRequestQueryAssistantPaginateTypeDef = TypedDict(
    "QueryAssistantRequestQueryAssistantPaginateTypeDef",
    {
        "assistantId": str,
        "queryText": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

NotifyRecommendationsReceivedResponseTypeDef = TypedDict(
    "NotifyRecommendationsReceivedResponseTypeDef",
    {
        "errors": List[NotifyRecommendationsReceivedErrorTypeDef],
        "recommendationIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RecommendationTriggerDataTypeDef = TypedDict(
    "RecommendationTriggerDataTypeDef",
    {
        "query": NotRequired[QueryRecommendationTriggerDataTypeDef],
    },
)

SearchSessionsResponseTypeDef = TypedDict(
    "SearchSessionsResponseTypeDef",
    {
        "nextToken": str,
        "sessionSummaries": List[SessionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SessionDataTypeDef = TypedDict(
    "SessionDataTypeDef",
    {
        "name": str,
        "sessionArn": str,
        "sessionId": str,
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[SessionIntegrationConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)

KnowledgeBaseSummaryPaginatorTypeDef = TypedDict(
    "KnowledgeBaseSummaryPaginatorTypeDef",
    {
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "knowledgeBaseType": KnowledgeBaseTypeType,
        "name": str,
        "status": KnowledgeBaseStatusType,
        "description": NotRequired[str],
        "renderingConfiguration": NotRequired[RenderingConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "sourceConfiguration": NotRequired[SourceConfigurationPaginatorTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)

CreateKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "CreateKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseType": KnowledgeBaseTypeType,
        "name": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "renderingConfiguration": NotRequired[RenderingConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "sourceConfiguration": NotRequired[SourceConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)

KnowledgeBaseDataTypeDef = TypedDict(
    "KnowledgeBaseDataTypeDef",
    {
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "knowledgeBaseType": KnowledgeBaseTypeType,
        "name": str,
        "status": KnowledgeBaseStatusType,
        "description": NotRequired[str],
        "lastContentModificationTime": NotRequired[datetime],
        "renderingConfiguration": NotRequired[RenderingConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "sourceConfiguration": NotRequired[SourceConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)

KnowledgeBaseSummaryTypeDef = TypedDict(
    "KnowledgeBaseSummaryTypeDef",
    {
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "knowledgeBaseType": KnowledgeBaseTypeType,
        "name": str,
        "status": KnowledgeBaseStatusType,
        "description": NotRequired[str],
        "renderingConfiguration": NotRequired[RenderingConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "sourceConfiguration": NotRequired[SourceConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)

AssistantAssociationDataTypeDef = TypedDict(
    "AssistantAssociationDataTypeDef",
    {
        "assistantArn": str,
        "assistantAssociationArn": str,
        "assistantAssociationId": str,
        "assistantId": str,
        "associationData": AssistantAssociationOutputDataTypeDef,
        "associationType": Literal["KNOWLEDGE_BASE"],
        "tags": NotRequired[Dict[str, str]],
    },
)

AssistantAssociationSummaryTypeDef = TypedDict(
    "AssistantAssociationSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantAssociationArn": str,
        "assistantAssociationId": str,
        "assistantId": str,
        "associationData": AssistantAssociationOutputDataTypeDef,
        "associationType": Literal["KNOWLEDGE_BASE"],
        "tags": NotRequired[Dict[str, str]],
    },
)

CreateAssistantResponseTypeDef = TypedDict(
    "CreateAssistantResponseTypeDef",
    {
        "assistant": AssistantDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssistantResponseTypeDef = TypedDict(
    "GetAssistantResponseTypeDef",
    {
        "assistant": AssistantDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssistantsResponseTypeDef = TypedDict(
    "ListAssistantsResponseTypeDef",
    {
        "assistantSummaries": List[AssistantSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DocumentTypeDef = TypedDict(
    "DocumentTypeDef",
    {
        "contentReference": ContentReferenceTypeDef,
        "excerpt": NotRequired[DocumentTextTypeDef],
        "title": NotRequired[DocumentTextTypeDef],
    },
)

SearchContentRequestRequestTypeDef = TypedDict(
    "SearchContentRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "searchExpression": SearchExpressionTypeDef,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

SearchContentRequestSearchContentPaginateTypeDef = TypedDict(
    "SearchContentRequestSearchContentPaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "searchExpression": SearchExpressionTypeDef,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

SearchSessionsRequestRequestTypeDef = TypedDict(
    "SearchSessionsRequestRequestTypeDef",
    {
        "assistantId": str,
        "searchExpression": SearchExpressionTypeDef,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

SearchSessionsRequestSearchSessionsPaginateTypeDef = TypedDict(
    "SearchSessionsRequestSearchSessionsPaginateTypeDef",
    {
        "assistantId": str,
        "searchExpression": SearchExpressionTypeDef,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

RecommendationTriggerTypeDef = TypedDict(
    "RecommendationTriggerTypeDef",
    {
        "data": RecommendationTriggerDataTypeDef,
        "id": str,
        "recommendationIds": List[str],
        "source": RecommendationSourceTypeType,
        "type": Literal["QUERY"],
    },
)

CreateSessionResponseTypeDef = TypedDict(
    "CreateSessionResponseTypeDef",
    {
        "session": SessionDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSessionResponseTypeDef = TypedDict(
    "GetSessionResponseTypeDef",
    {
        "session": SessionDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKnowledgeBasesResponsePaginatorTypeDef = TypedDict(
    "ListKnowledgeBasesResponsePaginatorTypeDef",
    {
        "knowledgeBaseSummaries": List[KnowledgeBaseSummaryPaginatorTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKnowledgeBaseResponseTypeDef = TypedDict(
    "CreateKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKnowledgeBaseResponseTypeDef = TypedDict(
    "GetKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateKnowledgeBaseTemplateUriResponseTypeDef = TypedDict(
    "UpdateKnowledgeBaseTemplateUriResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKnowledgeBasesResponseTypeDef = TypedDict(
    "ListKnowledgeBasesResponseTypeDef",
    {
        "knowledgeBaseSummaries": List[KnowledgeBaseSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAssistantAssociationResponseTypeDef = TypedDict(
    "CreateAssistantAssociationResponseTypeDef",
    {
        "assistantAssociation": AssistantAssociationDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssistantAssociationResponseTypeDef = TypedDict(
    "GetAssistantAssociationResponseTypeDef",
    {
        "assistantAssociation": AssistantAssociationDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssistantAssociationsResponseTypeDef = TypedDict(
    "ListAssistantAssociationsResponseTypeDef",
    {
        "assistantAssociationSummaries": List[AssistantAssociationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RecommendationDataTypeDef = TypedDict(
    "RecommendationDataTypeDef",
    {
        "document": DocumentTypeDef,
        "recommendationId": str,
        "relevanceLevel": NotRequired[RelevanceLevelType],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[Literal["KNOWLEDGE_CONTENT"]],
    },
)

ResultDataTypeDef = TypedDict(
    "ResultDataTypeDef",
    {
        "document": DocumentTypeDef,
        "resultId": str,
        "relevanceScore": NotRequired[float],
    },
)

GetRecommendationsResponseTypeDef = TypedDict(
    "GetRecommendationsResponseTypeDef",
    {
        "recommendations": List[RecommendationDataTypeDef],
        "triggers": List[RecommendationTriggerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

QueryAssistantResponseTypeDef = TypedDict(
    "QueryAssistantResponseTypeDef",
    {
        "nextToken": str,
        "results": List[ResultDataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
