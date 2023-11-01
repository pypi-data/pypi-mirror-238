"""
Type annotations for amplify service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/type_defs/)

Usage::

    ```python
    from mypy_boto3_amplify.type_defs import AutoBranchCreationConfigPaginatorTypeDef

    data: AutoBranchCreationConfigPaginatorTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    DomainStatusType,
    JobStatusType,
    JobTypeType,
    PlatformType,
    RepositoryCloneMethodType,
    StageType,
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
    "AutoBranchCreationConfigPaginatorTypeDef",
    "CustomRuleTypeDef",
    "ProductionBranchTypeDef",
    "AutoBranchCreationConfigTypeDef",
    "ArtifactTypeDef",
    "BackendEnvironmentTypeDef",
    "BackendTypeDef",
    "ResponseMetadataTypeDef",
    "CreateBackendEnvironmentRequestRequestTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "SubDomainSettingTypeDef",
    "CreateWebhookRequestRequestTypeDef",
    "WebhookTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteBackendEnvironmentRequestRequestTypeDef",
    "DeleteBranchRequestRequestTypeDef",
    "DeleteDomainAssociationRequestRequestTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "JobSummaryTypeDef",
    "DeleteWebhookRequestRequestTypeDef",
    "TimestampTypeDef",
    "GetAppRequestRequestTypeDef",
    "GetArtifactUrlRequestRequestTypeDef",
    "GetBackendEnvironmentRequestRequestTypeDef",
    "GetBranchRequestRequestTypeDef",
    "GetDomainAssociationRequestRequestTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetWebhookRequestRequestTypeDef",
    "StepTypeDef",
    "PaginatorConfigTypeDef",
    "ListAppsRequestRequestTypeDef",
    "ListArtifactsRequestRequestTypeDef",
    "ListBackendEnvironmentsRequestRequestTypeDef",
    "ListBranchesRequestRequestTypeDef",
    "ListDomainAssociationsRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWebhooksRequestRequestTypeDef",
    "StartDeploymentRequestRequestTypeDef",
    "StopJobRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateWebhookRequestRequestTypeDef",
    "AppPaginatorTypeDef",
    "AppTypeDef",
    "CreateAppRequestRequestTypeDef",
    "UpdateAppRequestRequestTypeDef",
    "BranchTypeDef",
    "CreateBranchRequestRequestTypeDef",
    "UpdateBranchRequestRequestTypeDef",
    "CreateBackendEnvironmentResultTypeDef",
    "CreateDeploymentResultTypeDef",
    "DeleteBackendEnvironmentResultTypeDef",
    "GenerateAccessLogsResultTypeDef",
    "GetArtifactUrlResultTypeDef",
    "GetBackendEnvironmentResultTypeDef",
    "ListArtifactsResultTypeDef",
    "ListBackendEnvironmentsResultTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "CreateDomainAssociationRequestRequestTypeDef",
    "SubDomainTypeDef",
    "UpdateDomainAssociationRequestRequestTypeDef",
    "CreateWebhookResultTypeDef",
    "DeleteWebhookResultTypeDef",
    "GetWebhookResultTypeDef",
    "ListWebhooksResultTypeDef",
    "UpdateWebhookResultTypeDef",
    "DeleteJobResultTypeDef",
    "ListJobsResultTypeDef",
    "StartDeploymentResultTypeDef",
    "StartJobResultTypeDef",
    "StopJobResultTypeDef",
    "GenerateAccessLogsRequestRequestTypeDef",
    "StartJobRequestRequestTypeDef",
    "JobTypeDef",
    "ListAppsRequestListAppsPaginateTypeDef",
    "ListBranchesRequestListBranchesPaginateTypeDef",
    "ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListAppsResultPaginatorTypeDef",
    "CreateAppResultTypeDef",
    "DeleteAppResultTypeDef",
    "GetAppResultTypeDef",
    "ListAppsResultTypeDef",
    "UpdateAppResultTypeDef",
    "CreateBranchResultTypeDef",
    "DeleteBranchResultTypeDef",
    "GetBranchResultTypeDef",
    "ListBranchesResultTypeDef",
    "UpdateBranchResultTypeDef",
    "DomainAssociationTypeDef",
    "GetJobResultTypeDef",
    "CreateDomainAssociationResultTypeDef",
    "DeleteDomainAssociationResultTypeDef",
    "GetDomainAssociationResultTypeDef",
    "ListDomainAssociationsResultTypeDef",
    "UpdateDomainAssociationResultTypeDef",
)

AutoBranchCreationConfigPaginatorTypeDef = TypedDict(
    "AutoBranchCreationConfigPaginatorTypeDef",
    {
        "stage": NotRequired[StageType],
        "framework": NotRequired[str],
        "enableAutoBuild": NotRequired[bool],
        "environmentVariables": NotRequired[Dict[str, str]],
        "basicAuthCredentials": NotRequired[str],
        "enableBasicAuth": NotRequired[bool],
        "enablePerformanceMode": NotRequired[bool],
        "buildSpec": NotRequired[str],
        "enablePullRequestPreview": NotRequired[bool],
        "pullRequestEnvironmentName": NotRequired[str],
    },
)

CustomRuleTypeDef = TypedDict(
    "CustomRuleTypeDef",
    {
        "source": str,
        "target": str,
        "status": NotRequired[str],
        "condition": NotRequired[str],
    },
)

ProductionBranchTypeDef = TypedDict(
    "ProductionBranchTypeDef",
    {
        "lastDeployTime": NotRequired[datetime],
        "status": NotRequired[str],
        "thumbnailUrl": NotRequired[str],
        "branchName": NotRequired[str],
    },
)

AutoBranchCreationConfigTypeDef = TypedDict(
    "AutoBranchCreationConfigTypeDef",
    {
        "stage": NotRequired[StageType],
        "framework": NotRequired[str],
        "enableAutoBuild": NotRequired[bool],
        "environmentVariables": NotRequired[Mapping[str, str]],
        "basicAuthCredentials": NotRequired[str],
        "enableBasicAuth": NotRequired[bool],
        "enablePerformanceMode": NotRequired[bool],
        "buildSpec": NotRequired[str],
        "enablePullRequestPreview": NotRequired[bool],
        "pullRequestEnvironmentName": NotRequired[str],
    },
)

ArtifactTypeDef = TypedDict(
    "ArtifactTypeDef",
    {
        "artifactFileName": str,
        "artifactId": str,
    },
)

BackendEnvironmentTypeDef = TypedDict(
    "BackendEnvironmentTypeDef",
    {
        "backendEnvironmentArn": str,
        "environmentName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "stackName": NotRequired[str],
        "deploymentArtifacts": NotRequired[str],
    },
)

BackendTypeDef = TypedDict(
    "BackendTypeDef",
    {
        "stackArn": NotRequired[str],
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

CreateBackendEnvironmentRequestRequestTypeDef = TypedDict(
    "CreateBackendEnvironmentRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
        "stackName": NotRequired[str],
        "deploymentArtifacts": NotRequired[str],
    },
)

CreateDeploymentRequestRequestTypeDef = TypedDict(
    "CreateDeploymentRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "fileMap": NotRequired[Mapping[str, str]],
    },
)

SubDomainSettingTypeDef = TypedDict(
    "SubDomainSettingTypeDef",
    {
        "prefix": str,
        "branchName": str,
    },
)

CreateWebhookRequestRequestTypeDef = TypedDict(
    "CreateWebhookRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "description": NotRequired[str],
    },
)

WebhookTypeDef = TypedDict(
    "WebhookTypeDef",
    {
        "webhookArn": str,
        "webhookId": str,
        "webhookUrl": str,
        "branchName": str,
        "description": str,
        "createTime": datetime,
        "updateTime": datetime,
    },
)

DeleteAppRequestRequestTypeDef = TypedDict(
    "DeleteAppRequestRequestTypeDef",
    {
        "appId": str,
    },
)

DeleteBackendEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteBackendEnvironmentRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)

DeleteBranchRequestRequestTypeDef = TypedDict(
    "DeleteBranchRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)

DeleteDomainAssociationRequestRequestTypeDef = TypedDict(
    "DeleteDomainAssociationRequestRequestTypeDef",
    {
        "appId": str,
        "domainName": str,
    },
)

DeleteJobRequestRequestTypeDef = TypedDict(
    "DeleteJobRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobId": str,
    },
)

JobSummaryTypeDef = TypedDict(
    "JobSummaryTypeDef",
    {
        "jobArn": str,
        "jobId": str,
        "commitId": str,
        "commitMessage": str,
        "commitTime": datetime,
        "startTime": datetime,
        "status": JobStatusType,
        "jobType": JobTypeType,
        "endTime": NotRequired[datetime],
    },
)

DeleteWebhookRequestRequestTypeDef = TypedDict(
    "DeleteWebhookRequestRequestTypeDef",
    {
        "webhookId": str,
    },
)

TimestampTypeDef = Union[datetime, str]
GetAppRequestRequestTypeDef = TypedDict(
    "GetAppRequestRequestTypeDef",
    {
        "appId": str,
    },
)

GetArtifactUrlRequestRequestTypeDef = TypedDict(
    "GetArtifactUrlRequestRequestTypeDef",
    {
        "artifactId": str,
    },
)

GetBackendEnvironmentRequestRequestTypeDef = TypedDict(
    "GetBackendEnvironmentRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)

GetBranchRequestRequestTypeDef = TypedDict(
    "GetBranchRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)

GetDomainAssociationRequestRequestTypeDef = TypedDict(
    "GetDomainAssociationRequestRequestTypeDef",
    {
        "appId": str,
        "domainName": str,
    },
)

GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobId": str,
    },
)

GetWebhookRequestRequestTypeDef = TypedDict(
    "GetWebhookRequestRequestTypeDef",
    {
        "webhookId": str,
    },
)

StepTypeDef = TypedDict(
    "StepTypeDef",
    {
        "stepName": str,
        "startTime": datetime,
        "status": JobStatusType,
        "endTime": datetime,
        "logUrl": NotRequired[str],
        "artifactsUrl": NotRequired[str],
        "testArtifactsUrl": NotRequired[str],
        "testConfigUrl": NotRequired[str],
        "screenshots": NotRequired[Dict[str, str]],
        "statusReason": NotRequired[str],
        "context": NotRequired[str],
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

ListAppsRequestRequestTypeDef = TypedDict(
    "ListAppsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListArtifactsRequestRequestTypeDef = TypedDict(
    "ListArtifactsRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListBackendEnvironmentsRequestRequestTypeDef = TypedDict(
    "ListBackendEnvironmentsRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": NotRequired[str],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListBranchesRequestRequestTypeDef = TypedDict(
    "ListBranchesRequestRequestTypeDef",
    {
        "appId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListDomainAssociationsRequestRequestTypeDef = TypedDict(
    "ListDomainAssociationsRequestRequestTypeDef",
    {
        "appId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
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

ListWebhooksRequestRequestTypeDef = TypedDict(
    "ListWebhooksRequestRequestTypeDef",
    {
        "appId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

StartDeploymentRequestRequestTypeDef = TypedDict(
    "StartDeploymentRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobId": NotRequired[str],
        "sourceUrl": NotRequired[str],
    },
)

StopJobRequestRequestTypeDef = TypedDict(
    "StopJobRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobId": str,
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

UpdateWebhookRequestRequestTypeDef = TypedDict(
    "UpdateWebhookRequestRequestTypeDef",
    {
        "webhookId": str,
        "branchName": NotRequired[str],
        "description": NotRequired[str],
    },
)

AppPaginatorTypeDef = TypedDict(
    "AppPaginatorTypeDef",
    {
        "appId": str,
        "appArn": str,
        "name": str,
        "description": str,
        "repository": str,
        "platform": PlatformType,
        "createTime": datetime,
        "updateTime": datetime,
        "environmentVariables": Dict[str, str],
        "defaultDomain": str,
        "enableBranchAutoBuild": bool,
        "enableBasicAuth": bool,
        "tags": NotRequired[Dict[str, str]],
        "iamServiceRoleArn": NotRequired[str],
        "enableBranchAutoDeletion": NotRequired[bool],
        "basicAuthCredentials": NotRequired[str],
        "customRules": NotRequired[List[CustomRuleTypeDef]],
        "productionBranch": NotRequired[ProductionBranchTypeDef],
        "buildSpec": NotRequired[str],
        "customHeaders": NotRequired[str],
        "enableAutoBranchCreation": NotRequired[bool],
        "autoBranchCreationPatterns": NotRequired[List[str]],
        "autoBranchCreationConfig": NotRequired[AutoBranchCreationConfigPaginatorTypeDef],
        "repositoryCloneMethod": NotRequired[RepositoryCloneMethodType],
    },
)

AppTypeDef = TypedDict(
    "AppTypeDef",
    {
        "appId": str,
        "appArn": str,
        "name": str,
        "description": str,
        "repository": str,
        "platform": PlatformType,
        "createTime": datetime,
        "updateTime": datetime,
        "environmentVariables": Dict[str, str],
        "defaultDomain": str,
        "enableBranchAutoBuild": bool,
        "enableBasicAuth": bool,
        "tags": NotRequired[Dict[str, str]],
        "iamServiceRoleArn": NotRequired[str],
        "enableBranchAutoDeletion": NotRequired[bool],
        "basicAuthCredentials": NotRequired[str],
        "customRules": NotRequired[List[CustomRuleTypeDef]],
        "productionBranch": NotRequired[ProductionBranchTypeDef],
        "buildSpec": NotRequired[str],
        "customHeaders": NotRequired[str],
        "enableAutoBranchCreation": NotRequired[bool],
        "autoBranchCreationPatterns": NotRequired[List[str]],
        "autoBranchCreationConfig": NotRequired[AutoBranchCreationConfigTypeDef],
        "repositoryCloneMethod": NotRequired[RepositoryCloneMethodType],
    },
)

CreateAppRequestRequestTypeDef = TypedDict(
    "CreateAppRequestRequestTypeDef",
    {
        "name": str,
        "description": NotRequired[str],
        "repository": NotRequired[str],
        "platform": NotRequired[PlatformType],
        "iamServiceRoleArn": NotRequired[str],
        "oauthToken": NotRequired[str],
        "accessToken": NotRequired[str],
        "environmentVariables": NotRequired[Mapping[str, str]],
        "enableBranchAutoBuild": NotRequired[bool],
        "enableBranchAutoDeletion": NotRequired[bool],
        "enableBasicAuth": NotRequired[bool],
        "basicAuthCredentials": NotRequired[str],
        "customRules": NotRequired[Sequence[CustomRuleTypeDef]],
        "tags": NotRequired[Mapping[str, str]],
        "buildSpec": NotRequired[str],
        "customHeaders": NotRequired[str],
        "enableAutoBranchCreation": NotRequired[bool],
        "autoBranchCreationPatterns": NotRequired[Sequence[str]],
        "autoBranchCreationConfig": NotRequired[AutoBranchCreationConfigTypeDef],
    },
)

UpdateAppRequestRequestTypeDef = TypedDict(
    "UpdateAppRequestRequestTypeDef",
    {
        "appId": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
        "platform": NotRequired[PlatformType],
        "iamServiceRoleArn": NotRequired[str],
        "environmentVariables": NotRequired[Mapping[str, str]],
        "enableBranchAutoBuild": NotRequired[bool],
        "enableBranchAutoDeletion": NotRequired[bool],
        "enableBasicAuth": NotRequired[bool],
        "basicAuthCredentials": NotRequired[str],
        "customRules": NotRequired[Sequence[CustomRuleTypeDef]],
        "buildSpec": NotRequired[str],
        "customHeaders": NotRequired[str],
        "enableAutoBranchCreation": NotRequired[bool],
        "autoBranchCreationPatterns": NotRequired[Sequence[str]],
        "autoBranchCreationConfig": NotRequired[AutoBranchCreationConfigTypeDef],
        "repository": NotRequired[str],
        "oauthToken": NotRequired[str],
        "accessToken": NotRequired[str],
    },
)

BranchTypeDef = TypedDict(
    "BranchTypeDef",
    {
        "branchArn": str,
        "branchName": str,
        "description": str,
        "stage": StageType,
        "displayName": str,
        "enableNotification": bool,
        "createTime": datetime,
        "updateTime": datetime,
        "environmentVariables": Dict[str, str],
        "enableAutoBuild": bool,
        "customDomains": List[str],
        "framework": str,
        "activeJobId": str,
        "totalNumberOfJobs": str,
        "enableBasicAuth": bool,
        "ttl": str,
        "enablePullRequestPreview": bool,
        "tags": NotRequired[Dict[str, str]],
        "enablePerformanceMode": NotRequired[bool],
        "thumbnailUrl": NotRequired[str],
        "basicAuthCredentials": NotRequired[str],
        "buildSpec": NotRequired[str],
        "associatedResources": NotRequired[List[str]],
        "pullRequestEnvironmentName": NotRequired[str],
        "destinationBranch": NotRequired[str],
        "sourceBranch": NotRequired[str],
        "backendEnvironmentArn": NotRequired[str],
        "backend": NotRequired[BackendTypeDef],
    },
)

CreateBranchRequestRequestTypeDef = TypedDict(
    "CreateBranchRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "description": NotRequired[str],
        "stage": NotRequired[StageType],
        "framework": NotRequired[str],
        "enableNotification": NotRequired[bool],
        "enableAutoBuild": NotRequired[bool],
        "environmentVariables": NotRequired[Mapping[str, str]],
        "basicAuthCredentials": NotRequired[str],
        "enableBasicAuth": NotRequired[bool],
        "enablePerformanceMode": NotRequired[bool],
        "tags": NotRequired[Mapping[str, str]],
        "buildSpec": NotRequired[str],
        "ttl": NotRequired[str],
        "displayName": NotRequired[str],
        "enablePullRequestPreview": NotRequired[bool],
        "pullRequestEnvironmentName": NotRequired[str],
        "backendEnvironmentArn": NotRequired[str],
        "backend": NotRequired[BackendTypeDef],
    },
)

UpdateBranchRequestRequestTypeDef = TypedDict(
    "UpdateBranchRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "description": NotRequired[str],
        "framework": NotRequired[str],
        "stage": NotRequired[StageType],
        "enableNotification": NotRequired[bool],
        "enableAutoBuild": NotRequired[bool],
        "environmentVariables": NotRequired[Mapping[str, str]],
        "basicAuthCredentials": NotRequired[str],
        "enableBasicAuth": NotRequired[bool],
        "enablePerformanceMode": NotRequired[bool],
        "buildSpec": NotRequired[str],
        "ttl": NotRequired[str],
        "displayName": NotRequired[str],
        "enablePullRequestPreview": NotRequired[bool],
        "pullRequestEnvironmentName": NotRequired[str],
        "backendEnvironmentArn": NotRequired[str],
        "backend": NotRequired[BackendTypeDef],
    },
)

CreateBackendEnvironmentResultTypeDef = TypedDict(
    "CreateBackendEnvironmentResultTypeDef",
    {
        "backendEnvironment": BackendEnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeploymentResultTypeDef = TypedDict(
    "CreateDeploymentResultTypeDef",
    {
        "jobId": str,
        "fileUploadUrls": Dict[str, str],
        "zipUploadUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBackendEnvironmentResultTypeDef = TypedDict(
    "DeleteBackendEnvironmentResultTypeDef",
    {
        "backendEnvironment": BackendEnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateAccessLogsResultTypeDef = TypedDict(
    "GenerateAccessLogsResultTypeDef",
    {
        "logUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetArtifactUrlResultTypeDef = TypedDict(
    "GetArtifactUrlResultTypeDef",
    {
        "artifactId": str,
        "artifactUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBackendEnvironmentResultTypeDef = TypedDict(
    "GetBackendEnvironmentResultTypeDef",
    {
        "backendEnvironment": BackendEnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListArtifactsResultTypeDef = TypedDict(
    "ListArtifactsResultTypeDef",
    {
        "artifacts": List[ArtifactTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackendEnvironmentsResultTypeDef = TypedDict(
    "ListBackendEnvironmentsResultTypeDef",
    {
        "backendEnvironments": List[BackendEnvironmentTypeDef],
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

CreateDomainAssociationRequestRequestTypeDef = TypedDict(
    "CreateDomainAssociationRequestRequestTypeDef",
    {
        "appId": str,
        "domainName": str,
        "subDomainSettings": Sequence[SubDomainSettingTypeDef],
        "enableAutoSubDomain": NotRequired[bool],
        "autoSubDomainCreationPatterns": NotRequired[Sequence[str]],
        "autoSubDomainIAMRole": NotRequired[str],
    },
)

SubDomainTypeDef = TypedDict(
    "SubDomainTypeDef",
    {
        "subDomainSetting": SubDomainSettingTypeDef,
        "verified": bool,
        "dnsRecord": str,
    },
)

UpdateDomainAssociationRequestRequestTypeDef = TypedDict(
    "UpdateDomainAssociationRequestRequestTypeDef",
    {
        "appId": str,
        "domainName": str,
        "enableAutoSubDomain": NotRequired[bool],
        "subDomainSettings": NotRequired[Sequence[SubDomainSettingTypeDef]],
        "autoSubDomainCreationPatterns": NotRequired[Sequence[str]],
        "autoSubDomainIAMRole": NotRequired[str],
    },
)

CreateWebhookResultTypeDef = TypedDict(
    "CreateWebhookResultTypeDef",
    {
        "webhook": WebhookTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteWebhookResultTypeDef = TypedDict(
    "DeleteWebhookResultTypeDef",
    {
        "webhook": WebhookTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWebhookResultTypeDef = TypedDict(
    "GetWebhookResultTypeDef",
    {
        "webhook": WebhookTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWebhooksResultTypeDef = TypedDict(
    "ListWebhooksResultTypeDef",
    {
        "webhooks": List[WebhookTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWebhookResultTypeDef = TypedDict(
    "UpdateWebhookResultTypeDef",
    {
        "webhook": WebhookTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteJobResultTypeDef = TypedDict(
    "DeleteJobResultTypeDef",
    {
        "jobSummary": JobSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsResultTypeDef = TypedDict(
    "ListJobsResultTypeDef",
    {
        "jobSummaries": List[JobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDeploymentResultTypeDef = TypedDict(
    "StartDeploymentResultTypeDef",
    {
        "jobSummary": JobSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartJobResultTypeDef = TypedDict(
    "StartJobResultTypeDef",
    {
        "jobSummary": JobSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopJobResultTypeDef = TypedDict(
    "StopJobResultTypeDef",
    {
        "jobSummary": JobSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateAccessLogsRequestRequestTypeDef = TypedDict(
    "GenerateAccessLogsRequestRequestTypeDef",
    {
        "domainName": str,
        "appId": str,
        "startTime": NotRequired[TimestampTypeDef],
        "endTime": NotRequired[TimestampTypeDef],
    },
)

StartJobRequestRequestTypeDef = TypedDict(
    "StartJobRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobType": JobTypeType,
        "jobId": NotRequired[str],
        "jobReason": NotRequired[str],
        "commitId": NotRequired[str],
        "commitMessage": NotRequired[str],
        "commitTime": NotRequired[TimestampTypeDef],
    },
)

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "summary": JobSummaryTypeDef,
        "steps": List[StepTypeDef],
    },
)

ListAppsRequestListAppsPaginateTypeDef = TypedDict(
    "ListAppsRequestListAppsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListBranchesRequestListBranchesPaginateTypeDef = TypedDict(
    "ListBranchesRequestListBranchesPaginateTypeDef",
    {
        "appId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef = TypedDict(
    "ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef",
    {
        "appId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "ListJobsRequestListJobsPaginateTypeDef",
    {
        "appId": str,
        "branchName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAppsResultPaginatorTypeDef = TypedDict(
    "ListAppsResultPaginatorTypeDef",
    {
        "apps": List[AppPaginatorTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAppResultTypeDef = TypedDict(
    "CreateAppResultTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAppResultTypeDef = TypedDict(
    "DeleteAppResultTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAppResultTypeDef = TypedDict(
    "GetAppResultTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppsResultTypeDef = TypedDict(
    "ListAppsResultTypeDef",
    {
        "apps": List[AppTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppResultTypeDef = TypedDict(
    "UpdateAppResultTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBranchResultTypeDef = TypedDict(
    "CreateBranchResultTypeDef",
    {
        "branch": BranchTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBranchResultTypeDef = TypedDict(
    "DeleteBranchResultTypeDef",
    {
        "branch": BranchTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBranchResultTypeDef = TypedDict(
    "GetBranchResultTypeDef",
    {
        "branch": BranchTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBranchesResultTypeDef = TypedDict(
    "ListBranchesResultTypeDef",
    {
        "branches": List[BranchTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBranchResultTypeDef = TypedDict(
    "UpdateBranchResultTypeDef",
    {
        "branch": BranchTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DomainAssociationTypeDef = TypedDict(
    "DomainAssociationTypeDef",
    {
        "domainAssociationArn": str,
        "domainName": str,
        "enableAutoSubDomain": bool,
        "domainStatus": DomainStatusType,
        "statusReason": str,
        "subDomains": List[SubDomainTypeDef],
        "autoSubDomainCreationPatterns": NotRequired[List[str]],
        "autoSubDomainIAMRole": NotRequired[str],
        "certificateVerificationDNSRecord": NotRequired[str],
    },
)

GetJobResultTypeDef = TypedDict(
    "GetJobResultTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDomainAssociationResultTypeDef = TypedDict(
    "CreateDomainAssociationResultTypeDef",
    {
        "domainAssociation": DomainAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDomainAssociationResultTypeDef = TypedDict(
    "DeleteDomainAssociationResultTypeDef",
    {
        "domainAssociation": DomainAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDomainAssociationResultTypeDef = TypedDict(
    "GetDomainAssociationResultTypeDef",
    {
        "domainAssociation": DomainAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDomainAssociationsResultTypeDef = TypedDict(
    "ListDomainAssociationsResultTypeDef",
    {
        "domainAssociations": List[DomainAssociationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDomainAssociationResultTypeDef = TypedDict(
    "UpdateDomainAssociationResultTypeDef",
    {
        "domainAssociation": DomainAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
