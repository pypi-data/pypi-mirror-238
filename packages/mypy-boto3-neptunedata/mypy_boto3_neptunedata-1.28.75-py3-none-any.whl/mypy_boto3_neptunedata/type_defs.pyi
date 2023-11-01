"""
Type annotations for neptunedata service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/type_defs/)

Usage::

    ```python
    from mypy_boto3_neptunedata.type_defs import CancelGremlinQueryInputRequestTypeDef

    data: CancelGremlinQueryInputRequestTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence

from botocore.response import StreamingBody

from .literals import (
    ActionType,
    FormatType,
    GraphSummaryTypeType,
    IteratorTypeType,
    ModeType,
    OpenCypherExplainModeType,
    ParallelismType,
    S3BucketRegionType,
    StatisticsAutoGenerationModeType,
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
    "CancelGremlinQueryInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CancelLoaderJobInputRequestTypeDef",
    "CancelMLDataProcessingJobInputRequestTypeDef",
    "CancelMLModelTrainingJobInputRequestTypeDef",
    "CancelMLModelTransformJobInputRequestTypeDef",
    "CancelOpenCypherQueryInputRequestTypeDef",
    "CreateMLEndpointInputRequestTypeDef",
    "CustomModelTrainingParametersTypeDef",
    "CustomModelTransformParametersTypeDef",
    "DeleteMLEndpointInputRequestTypeDef",
    "DeleteStatisticsValueMapTypeDef",
    "EdgeStructureTypeDef",
    "ExecuteFastResetInputRequestTypeDef",
    "FastResetTokenTypeDef",
    "ExecuteGremlinExplainQueryInputRequestTypeDef",
    "ExecuteGremlinProfileQueryInputRequestTypeDef",
    "ExecuteGremlinQueryInputRequestTypeDef",
    "GremlinQueryStatusAttributesTypeDef",
    "ExecuteOpenCypherExplainQueryInputRequestTypeDef",
    "ExecuteOpenCypherQueryInputRequestTypeDef",
    "QueryLanguageVersionTypeDef",
    "GetGremlinQueryStatusInputRequestTypeDef",
    "QueryEvalStatsTypeDef",
    "GetLoaderJobStatusInputRequestTypeDef",
    "GetMLDataProcessingJobInputRequestTypeDef",
    "MlResourceDefinitionTypeDef",
    "GetMLEndpointInputRequestTypeDef",
    "MlConfigDefinitionTypeDef",
    "GetMLModelTrainingJobInputRequestTypeDef",
    "GetMLModelTransformJobInputRequestTypeDef",
    "GetOpenCypherQueryStatusInputRequestTypeDef",
    "GetPropertygraphStreamInputRequestTypeDef",
    "GetPropertygraphSummaryInputRequestTypeDef",
    "GetRDFGraphSummaryInputRequestTypeDef",
    "GetSparqlStreamInputRequestTypeDef",
    "ListGremlinQueriesInputRequestTypeDef",
    "ListLoaderJobsInputRequestTypeDef",
    "LoaderIdResultTypeDef",
    "ListMLDataProcessingJobsInputRequestTypeDef",
    "ListMLEndpointsInputRequestTypeDef",
    "ListMLModelTrainingJobsInputRequestTypeDef",
    "ListMLModelTransformJobsInputRequestTypeDef",
    "ListOpenCypherQueriesInputRequestTypeDef",
    "ManagePropertygraphStatisticsInputRequestTypeDef",
    "RefreshStatisticsIdMapTypeDef",
    "ManageSparqlStatisticsInputRequestTypeDef",
    "NodeStructureTypeDef",
    "PropertygraphDataTypeDef",
    "SubjectStructureTypeDef",
    "SparqlDataTypeDef",
    "StartLoaderJobInputRequestTypeDef",
    "StartMLDataProcessingJobInputRequestTypeDef",
    "StatisticsSummaryTypeDef",
    "CancelGremlinQueryOutputTypeDef",
    "CancelLoaderJobOutputTypeDef",
    "CancelMLDataProcessingJobOutputTypeDef",
    "CancelMLModelTrainingJobOutputTypeDef",
    "CancelMLModelTransformJobOutputTypeDef",
    "CancelOpenCypherQueryOutputTypeDef",
    "CreateMLEndpointOutputTypeDef",
    "DeleteMLEndpointOutputTypeDef",
    "ExecuteGremlinExplainQueryOutputTypeDef",
    "ExecuteGremlinProfileQueryOutputTypeDef",
    "ExecuteOpenCypherExplainQueryOutputTypeDef",
    "ExecuteOpenCypherQueryOutputTypeDef",
    "GetLoaderJobStatusOutputTypeDef",
    "ListMLDataProcessingJobsOutputTypeDef",
    "ListMLEndpointsOutputTypeDef",
    "ListMLModelTrainingJobsOutputTypeDef",
    "ListMLModelTransformJobsOutputTypeDef",
    "StartLoaderJobOutputTypeDef",
    "StartMLDataProcessingJobOutputTypeDef",
    "StartMLModelTrainingJobOutputTypeDef",
    "StartMLModelTransformJobOutputTypeDef",
    "StartMLModelTrainingJobInputRequestTypeDef",
    "StartMLModelTransformJobInputRequestTypeDef",
    "DeletePropertygraphStatisticsOutputTypeDef",
    "DeleteSparqlStatisticsOutputTypeDef",
    "ExecuteFastResetOutputTypeDef",
    "ExecuteGremlinQueryOutputTypeDef",
    "GetEngineStatusOutputTypeDef",
    "GetGremlinQueryStatusOutputTypeDef",
    "GetOpenCypherQueryStatusOutputTypeDef",
    "GremlinQueryStatusTypeDef",
    "GetMLDataProcessingJobOutputTypeDef",
    "GetMLEndpointOutputTypeDef",
    "GetMLModelTrainingJobOutputTypeDef",
    "GetMLModelTransformJobOutputTypeDef",
    "ListLoaderJobsOutputTypeDef",
    "ManagePropertygraphStatisticsOutputTypeDef",
    "ManageSparqlStatisticsOutputTypeDef",
    "PropertygraphSummaryTypeDef",
    "PropertygraphRecordTypeDef",
    "RDFGraphSummaryTypeDef",
    "SparqlRecordTypeDef",
    "StatisticsTypeDef",
    "ListGremlinQueriesOutputTypeDef",
    "ListOpenCypherQueriesOutputTypeDef",
    "PropertygraphSummaryValueMapTypeDef",
    "GetPropertygraphStreamOutputTypeDef",
    "RDFGraphSummaryValueMapTypeDef",
    "GetSparqlStreamOutputTypeDef",
    "GetPropertygraphStatisticsOutputTypeDef",
    "GetSparqlStatisticsOutputTypeDef",
    "GetPropertygraphSummaryOutputTypeDef",
    "GetRDFGraphSummaryOutputTypeDef",
)

CancelGremlinQueryInputRequestTypeDef = TypedDict(
    "CancelGremlinQueryInputRequestTypeDef",
    {
        "queryId": str,
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

CancelLoaderJobInputRequestTypeDef = TypedDict(
    "CancelLoaderJobInputRequestTypeDef",
    {
        "loadId": str,
    },
)

CancelMLDataProcessingJobInputRequestTypeDef = TypedDict(
    "CancelMLDataProcessingJobInputRequestTypeDef",
    {
        "id": str,
        "neptuneIamRoleArn": NotRequired[str],
        "clean": NotRequired[bool],
    },
)

CancelMLModelTrainingJobInputRequestTypeDef = TypedDict(
    "CancelMLModelTrainingJobInputRequestTypeDef",
    {
        "id": str,
        "neptuneIamRoleArn": NotRequired[str],
        "clean": NotRequired[bool],
    },
)

CancelMLModelTransformJobInputRequestTypeDef = TypedDict(
    "CancelMLModelTransformJobInputRequestTypeDef",
    {
        "id": str,
        "neptuneIamRoleArn": NotRequired[str],
        "clean": NotRequired[bool],
    },
)

CancelOpenCypherQueryInputRequestTypeDef = TypedDict(
    "CancelOpenCypherQueryInputRequestTypeDef",
    {
        "queryId": str,
        "silent": NotRequired[bool],
    },
)

CreateMLEndpointInputRequestTypeDef = TypedDict(
    "CreateMLEndpointInputRequestTypeDef",
    {
        "id": NotRequired[str],
        "mlModelTrainingJobId": NotRequired[str],
        "mlModelTransformJobId": NotRequired[str],
        "update": NotRequired[bool],
        "neptuneIamRoleArn": NotRequired[str],
        "modelName": NotRequired[str],
        "instanceType": NotRequired[str],
        "instanceCount": NotRequired[int],
        "volumeEncryptionKMSKey": NotRequired[str],
    },
)

CustomModelTrainingParametersTypeDef = TypedDict(
    "CustomModelTrainingParametersTypeDef",
    {
        "sourceS3DirectoryPath": str,
        "trainingEntryPointScript": NotRequired[str],
        "transformEntryPointScript": NotRequired[str],
    },
)

CustomModelTransformParametersTypeDef = TypedDict(
    "CustomModelTransformParametersTypeDef",
    {
        "sourceS3DirectoryPath": str,
        "transformEntryPointScript": NotRequired[str],
    },
)

DeleteMLEndpointInputRequestTypeDef = TypedDict(
    "DeleteMLEndpointInputRequestTypeDef",
    {
        "id": str,
        "neptuneIamRoleArn": NotRequired[str],
        "clean": NotRequired[bool],
    },
)

DeleteStatisticsValueMapTypeDef = TypedDict(
    "DeleteStatisticsValueMapTypeDef",
    {
        "active": NotRequired[bool],
        "statisticsId": NotRequired[str],
    },
)

EdgeStructureTypeDef = TypedDict(
    "EdgeStructureTypeDef",
    {
        "count": NotRequired[int],
        "edgeProperties": NotRequired[List[str]],
    },
)

ExecuteFastResetInputRequestTypeDef = TypedDict(
    "ExecuteFastResetInputRequestTypeDef",
    {
        "action": ActionType,
        "token": NotRequired[str],
    },
)

FastResetTokenTypeDef = TypedDict(
    "FastResetTokenTypeDef",
    {
        "token": NotRequired[str],
    },
)

ExecuteGremlinExplainQueryInputRequestTypeDef = TypedDict(
    "ExecuteGremlinExplainQueryInputRequestTypeDef",
    {
        "gremlinQuery": str,
    },
)

ExecuteGremlinProfileQueryInputRequestTypeDef = TypedDict(
    "ExecuteGremlinProfileQueryInputRequestTypeDef",
    {
        "gremlinQuery": str,
        "results": NotRequired[bool],
        "chop": NotRequired[int],
        "serializer": NotRequired[str],
        "indexOps": NotRequired[bool],
    },
)

ExecuteGremlinQueryInputRequestTypeDef = TypedDict(
    "ExecuteGremlinQueryInputRequestTypeDef",
    {
        "gremlinQuery": str,
        "serializer": NotRequired[str],
    },
)

GremlinQueryStatusAttributesTypeDef = TypedDict(
    "GremlinQueryStatusAttributesTypeDef",
    {
        "message": NotRequired[str],
        "code": NotRequired[int],
        "attributes": NotRequired[Dict[str, Any]],
    },
)

ExecuteOpenCypherExplainQueryInputRequestTypeDef = TypedDict(
    "ExecuteOpenCypherExplainQueryInputRequestTypeDef",
    {
        "openCypherQuery": str,
        "explainMode": OpenCypherExplainModeType,
        "parameters": NotRequired[str],
    },
)

ExecuteOpenCypherQueryInputRequestTypeDef = TypedDict(
    "ExecuteOpenCypherQueryInputRequestTypeDef",
    {
        "openCypherQuery": str,
        "parameters": NotRequired[str],
    },
)

QueryLanguageVersionTypeDef = TypedDict(
    "QueryLanguageVersionTypeDef",
    {
        "version": str,
    },
)

GetGremlinQueryStatusInputRequestTypeDef = TypedDict(
    "GetGremlinQueryStatusInputRequestTypeDef",
    {
        "queryId": str,
    },
)

QueryEvalStatsTypeDef = TypedDict(
    "QueryEvalStatsTypeDef",
    {
        "waited": NotRequired[int],
        "elapsed": NotRequired[int],
        "cancelled": NotRequired[bool],
        "subqueries": NotRequired[Dict[str, Any]],
    },
)

GetLoaderJobStatusInputRequestTypeDef = TypedDict(
    "GetLoaderJobStatusInputRequestTypeDef",
    {
        "loadId": str,
        "details": NotRequired[bool],
        "errors": NotRequired[bool],
        "page": NotRequired[int],
        "errorsPerPage": NotRequired[int],
    },
)

GetMLDataProcessingJobInputRequestTypeDef = TypedDict(
    "GetMLDataProcessingJobInputRequestTypeDef",
    {
        "id": str,
        "neptuneIamRoleArn": NotRequired[str],
    },
)

MlResourceDefinitionTypeDef = TypedDict(
    "MlResourceDefinitionTypeDef",
    {
        "name": NotRequired[str],
        "arn": NotRequired[str],
        "status": NotRequired[str],
        "outputLocation": NotRequired[str],
        "failureReason": NotRequired[str],
        "cloudwatchLogUrl": NotRequired[str],
    },
)

GetMLEndpointInputRequestTypeDef = TypedDict(
    "GetMLEndpointInputRequestTypeDef",
    {
        "id": str,
        "neptuneIamRoleArn": NotRequired[str],
    },
)

MlConfigDefinitionTypeDef = TypedDict(
    "MlConfigDefinitionTypeDef",
    {
        "name": NotRequired[str],
        "arn": NotRequired[str],
    },
)

GetMLModelTrainingJobInputRequestTypeDef = TypedDict(
    "GetMLModelTrainingJobInputRequestTypeDef",
    {
        "id": str,
        "neptuneIamRoleArn": NotRequired[str],
    },
)

GetMLModelTransformJobInputRequestTypeDef = TypedDict(
    "GetMLModelTransformJobInputRequestTypeDef",
    {
        "id": str,
        "neptuneIamRoleArn": NotRequired[str],
    },
)

GetOpenCypherQueryStatusInputRequestTypeDef = TypedDict(
    "GetOpenCypherQueryStatusInputRequestTypeDef",
    {
        "queryId": str,
    },
)

GetPropertygraphStreamInputRequestTypeDef = TypedDict(
    "GetPropertygraphStreamInputRequestTypeDef",
    {
        "limit": NotRequired[int],
        "iteratorType": NotRequired[IteratorTypeType],
        "commitNum": NotRequired[int],
        "opNum": NotRequired[int],
        "encoding": NotRequired[Literal["gzip"]],
    },
)

GetPropertygraphSummaryInputRequestTypeDef = TypedDict(
    "GetPropertygraphSummaryInputRequestTypeDef",
    {
        "mode": NotRequired[GraphSummaryTypeType],
    },
)

GetRDFGraphSummaryInputRequestTypeDef = TypedDict(
    "GetRDFGraphSummaryInputRequestTypeDef",
    {
        "mode": NotRequired[GraphSummaryTypeType],
    },
)

GetSparqlStreamInputRequestTypeDef = TypedDict(
    "GetSparqlStreamInputRequestTypeDef",
    {
        "limit": NotRequired[int],
        "iteratorType": NotRequired[IteratorTypeType],
        "commitNum": NotRequired[int],
        "opNum": NotRequired[int],
        "encoding": NotRequired[Literal["gzip"]],
    },
)

ListGremlinQueriesInputRequestTypeDef = TypedDict(
    "ListGremlinQueriesInputRequestTypeDef",
    {
        "includeWaiting": NotRequired[bool],
    },
)

ListLoaderJobsInputRequestTypeDef = TypedDict(
    "ListLoaderJobsInputRequestTypeDef",
    {
        "limit": NotRequired[int],
        "includeQueuedLoads": NotRequired[bool],
    },
)

LoaderIdResultTypeDef = TypedDict(
    "LoaderIdResultTypeDef",
    {
        "loadIds": NotRequired[List[str]],
    },
)

ListMLDataProcessingJobsInputRequestTypeDef = TypedDict(
    "ListMLDataProcessingJobsInputRequestTypeDef",
    {
        "maxItems": NotRequired[int],
        "neptuneIamRoleArn": NotRequired[str],
    },
)

ListMLEndpointsInputRequestTypeDef = TypedDict(
    "ListMLEndpointsInputRequestTypeDef",
    {
        "maxItems": NotRequired[int],
        "neptuneIamRoleArn": NotRequired[str],
    },
)

ListMLModelTrainingJobsInputRequestTypeDef = TypedDict(
    "ListMLModelTrainingJobsInputRequestTypeDef",
    {
        "maxItems": NotRequired[int],
        "neptuneIamRoleArn": NotRequired[str],
    },
)

ListMLModelTransformJobsInputRequestTypeDef = TypedDict(
    "ListMLModelTransformJobsInputRequestTypeDef",
    {
        "maxItems": NotRequired[int],
        "neptuneIamRoleArn": NotRequired[str],
    },
)

ListOpenCypherQueriesInputRequestTypeDef = TypedDict(
    "ListOpenCypherQueriesInputRequestTypeDef",
    {
        "includeWaiting": NotRequired[bool],
    },
)

ManagePropertygraphStatisticsInputRequestTypeDef = TypedDict(
    "ManagePropertygraphStatisticsInputRequestTypeDef",
    {
        "mode": NotRequired[StatisticsAutoGenerationModeType],
    },
)

RefreshStatisticsIdMapTypeDef = TypedDict(
    "RefreshStatisticsIdMapTypeDef",
    {
        "statisticsId": NotRequired[str],
    },
)

ManageSparqlStatisticsInputRequestTypeDef = TypedDict(
    "ManageSparqlStatisticsInputRequestTypeDef",
    {
        "mode": NotRequired[StatisticsAutoGenerationModeType],
    },
)

NodeStructureTypeDef = TypedDict(
    "NodeStructureTypeDef",
    {
        "count": NotRequired[int],
        "nodeProperties": NotRequired[List[str]],
        "distinctOutgoingEdgeLabels": NotRequired[List[str]],
    },
)

PropertygraphDataTypeDef = TypedDict(
    "PropertygraphDataTypeDef",
    {
        "id": str,
        "type": str,
        "key": str,
        "value": Dict[str, Any],
        "from": NotRequired[str],
        "to": NotRequired[str],
    },
)

SubjectStructureTypeDef = TypedDict(
    "SubjectStructureTypeDef",
    {
        "count": NotRequired[int],
        "predicates": NotRequired[List[str]],
    },
)

SparqlDataTypeDef = TypedDict(
    "SparqlDataTypeDef",
    {
        "stmt": str,
    },
)

StartLoaderJobInputRequestTypeDef = TypedDict(
    "StartLoaderJobInputRequestTypeDef",
    {
        "source": str,
        "format": FormatType,
        "s3BucketRegion": S3BucketRegionType,
        "iamRoleArn": str,
        "mode": NotRequired[ModeType],
        "failOnError": NotRequired[bool],
        "parallelism": NotRequired[ParallelismType],
        "parserConfiguration": NotRequired[Mapping[str, str]],
        "updateSingleCardinalityProperties": NotRequired[bool],
        "queueRequest": NotRequired[bool],
        "dependencies": NotRequired[Sequence[str]],
        "userProvidedEdgeIds": NotRequired[bool],
    },
)

StartMLDataProcessingJobInputRequestTypeDef = TypedDict(
    "StartMLDataProcessingJobInputRequestTypeDef",
    {
        "inputDataS3Location": str,
        "processedDataS3Location": str,
        "id": NotRequired[str],
        "previousDataProcessingJobId": NotRequired[str],
        "sagemakerIamRoleArn": NotRequired[str],
        "neptuneIamRoleArn": NotRequired[str],
        "processingInstanceType": NotRequired[str],
        "processingInstanceVolumeSizeInGB": NotRequired[int],
        "processingTimeOutInSeconds": NotRequired[int],
        "modelType": NotRequired[str],
        "configFileName": NotRequired[str],
        "subnets": NotRequired[Sequence[str]],
        "securityGroupIds": NotRequired[Sequence[str]],
        "volumeEncryptionKMSKey": NotRequired[str],
        "s3OutputEncryptionKMSKey": NotRequired[str],
    },
)

StatisticsSummaryTypeDef = TypedDict(
    "StatisticsSummaryTypeDef",
    {
        "signatureCount": NotRequired[int],
        "instanceCount": NotRequired[int],
        "predicateCount": NotRequired[int],
    },
)

CancelGremlinQueryOutputTypeDef = TypedDict(
    "CancelGremlinQueryOutputTypeDef",
    {
        "status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelLoaderJobOutputTypeDef = TypedDict(
    "CancelLoaderJobOutputTypeDef",
    {
        "status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelMLDataProcessingJobOutputTypeDef = TypedDict(
    "CancelMLDataProcessingJobOutputTypeDef",
    {
        "status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelMLModelTrainingJobOutputTypeDef = TypedDict(
    "CancelMLModelTrainingJobOutputTypeDef",
    {
        "status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelMLModelTransformJobOutputTypeDef = TypedDict(
    "CancelMLModelTransformJobOutputTypeDef",
    {
        "status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelOpenCypherQueryOutputTypeDef = TypedDict(
    "CancelOpenCypherQueryOutputTypeDef",
    {
        "status": str,
        "payload": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMLEndpointOutputTypeDef = TypedDict(
    "CreateMLEndpointOutputTypeDef",
    {
        "id": str,
        "arn": str,
        "creationTimeInMillis": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMLEndpointOutputTypeDef = TypedDict(
    "DeleteMLEndpointOutputTypeDef",
    {
        "status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExecuteGremlinExplainQueryOutputTypeDef = TypedDict(
    "ExecuteGremlinExplainQueryOutputTypeDef",
    {
        "output": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExecuteGremlinProfileQueryOutputTypeDef = TypedDict(
    "ExecuteGremlinProfileQueryOutputTypeDef",
    {
        "output": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExecuteOpenCypherExplainQueryOutputTypeDef = TypedDict(
    "ExecuteOpenCypherExplainQueryOutputTypeDef",
    {
        "results": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExecuteOpenCypherQueryOutputTypeDef = TypedDict(
    "ExecuteOpenCypherQueryOutputTypeDef",
    {
        "results": Dict[str, Any],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLoaderJobStatusOutputTypeDef = TypedDict(
    "GetLoaderJobStatusOutputTypeDef",
    {
        "status": str,
        "payload": Dict[str, Any],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMLDataProcessingJobsOutputTypeDef = TypedDict(
    "ListMLDataProcessingJobsOutputTypeDef",
    {
        "ids": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMLEndpointsOutputTypeDef = TypedDict(
    "ListMLEndpointsOutputTypeDef",
    {
        "ids": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMLModelTrainingJobsOutputTypeDef = TypedDict(
    "ListMLModelTrainingJobsOutputTypeDef",
    {
        "ids": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMLModelTransformJobsOutputTypeDef = TypedDict(
    "ListMLModelTransformJobsOutputTypeDef",
    {
        "ids": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartLoaderJobOutputTypeDef = TypedDict(
    "StartLoaderJobOutputTypeDef",
    {
        "status": str,
        "payload": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMLDataProcessingJobOutputTypeDef = TypedDict(
    "StartMLDataProcessingJobOutputTypeDef",
    {
        "id": str,
        "arn": str,
        "creationTimeInMillis": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMLModelTrainingJobOutputTypeDef = TypedDict(
    "StartMLModelTrainingJobOutputTypeDef",
    {
        "id": str,
        "arn": str,
        "creationTimeInMillis": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMLModelTransformJobOutputTypeDef = TypedDict(
    "StartMLModelTransformJobOutputTypeDef",
    {
        "id": str,
        "arn": str,
        "creationTimeInMillis": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMLModelTrainingJobInputRequestTypeDef = TypedDict(
    "StartMLModelTrainingJobInputRequestTypeDef",
    {
        "dataProcessingJobId": str,
        "trainModelS3Location": str,
        "id": NotRequired[str],
        "previousModelTrainingJobId": NotRequired[str],
        "sagemakerIamRoleArn": NotRequired[str],
        "neptuneIamRoleArn": NotRequired[str],
        "baseProcessingInstanceType": NotRequired[str],
        "trainingInstanceType": NotRequired[str],
        "trainingInstanceVolumeSizeInGB": NotRequired[int],
        "trainingTimeOutInSeconds": NotRequired[int],
        "maxHPONumberOfTrainingJobs": NotRequired[int],
        "maxHPOParallelTrainingJobs": NotRequired[int],
        "subnets": NotRequired[Sequence[str]],
        "securityGroupIds": NotRequired[Sequence[str]],
        "volumeEncryptionKMSKey": NotRequired[str],
        "s3OutputEncryptionKMSKey": NotRequired[str],
        "enableManagedSpotTraining": NotRequired[bool],
        "customModelTrainingParameters": NotRequired[CustomModelTrainingParametersTypeDef],
    },
)

StartMLModelTransformJobInputRequestTypeDef = TypedDict(
    "StartMLModelTransformJobInputRequestTypeDef",
    {
        "modelTransformOutputS3Location": str,
        "id": NotRequired[str],
        "dataProcessingJobId": NotRequired[str],
        "mlModelTrainingJobId": NotRequired[str],
        "trainingJobName": NotRequired[str],
        "sagemakerIamRoleArn": NotRequired[str],
        "neptuneIamRoleArn": NotRequired[str],
        "customModelTransformParameters": NotRequired[CustomModelTransformParametersTypeDef],
        "baseProcessingInstanceType": NotRequired[str],
        "baseProcessingInstanceVolumeSizeInGB": NotRequired[int],
        "subnets": NotRequired[Sequence[str]],
        "securityGroupIds": NotRequired[Sequence[str]],
        "volumeEncryptionKMSKey": NotRequired[str],
        "s3OutputEncryptionKMSKey": NotRequired[str],
    },
)

DeletePropertygraphStatisticsOutputTypeDef = TypedDict(
    "DeletePropertygraphStatisticsOutputTypeDef",
    {
        "statusCode": int,
        "status": str,
        "payload": DeleteStatisticsValueMapTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSparqlStatisticsOutputTypeDef = TypedDict(
    "DeleteSparqlStatisticsOutputTypeDef",
    {
        "statusCode": int,
        "status": str,
        "payload": DeleteStatisticsValueMapTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExecuteFastResetOutputTypeDef = TypedDict(
    "ExecuteFastResetOutputTypeDef",
    {
        "status": str,
        "payload": FastResetTokenTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExecuteGremlinQueryOutputTypeDef = TypedDict(
    "ExecuteGremlinQueryOutputTypeDef",
    {
        "requestId": str,
        "status": GremlinQueryStatusAttributesTypeDef,
        "result": Dict[str, Any],
        "meta": Dict[str, Any],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEngineStatusOutputTypeDef = TypedDict(
    "GetEngineStatusOutputTypeDef",
    {
        "status": str,
        "startTime": str,
        "dbEngineVersion": str,
        "role": str,
        "dfeQueryEngine": str,
        "gremlin": QueryLanguageVersionTypeDef,
        "sparql": QueryLanguageVersionTypeDef,
        "opencypher": QueryLanguageVersionTypeDef,
        "labMode": Dict[str, str],
        "rollingBackTrxCount": int,
        "rollingBackTrxEarliestStartTime": str,
        "features": Dict[str, Dict[str, Any]],
        "settings": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGremlinQueryStatusOutputTypeDef = TypedDict(
    "GetGremlinQueryStatusOutputTypeDef",
    {
        "queryId": str,
        "queryString": str,
        "queryEvalStats": QueryEvalStatsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOpenCypherQueryStatusOutputTypeDef = TypedDict(
    "GetOpenCypherQueryStatusOutputTypeDef",
    {
        "queryId": str,
        "queryString": str,
        "queryEvalStats": QueryEvalStatsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GremlinQueryStatusTypeDef = TypedDict(
    "GremlinQueryStatusTypeDef",
    {
        "queryId": NotRequired[str],
        "queryString": NotRequired[str],
        "queryEvalStats": NotRequired[QueryEvalStatsTypeDef],
    },
)

GetMLDataProcessingJobOutputTypeDef = TypedDict(
    "GetMLDataProcessingJobOutputTypeDef",
    {
        "status": str,
        "id": str,
        "processingJob": MlResourceDefinitionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMLEndpointOutputTypeDef = TypedDict(
    "GetMLEndpointOutputTypeDef",
    {
        "status": str,
        "id": str,
        "endpoint": MlResourceDefinitionTypeDef,
        "endpointConfig": MlConfigDefinitionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMLModelTrainingJobOutputTypeDef = TypedDict(
    "GetMLModelTrainingJobOutputTypeDef",
    {
        "status": str,
        "id": str,
        "processingJob": MlResourceDefinitionTypeDef,
        "hpoJob": MlResourceDefinitionTypeDef,
        "modelTransformJob": MlResourceDefinitionTypeDef,
        "mlModels": List[MlConfigDefinitionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMLModelTransformJobOutputTypeDef = TypedDict(
    "GetMLModelTransformJobOutputTypeDef",
    {
        "status": str,
        "id": str,
        "baseProcessingJob": MlResourceDefinitionTypeDef,
        "remoteModelTransformJob": MlResourceDefinitionTypeDef,
        "models": List[MlConfigDefinitionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLoaderJobsOutputTypeDef = TypedDict(
    "ListLoaderJobsOutputTypeDef",
    {
        "status": str,
        "payload": LoaderIdResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ManagePropertygraphStatisticsOutputTypeDef = TypedDict(
    "ManagePropertygraphStatisticsOutputTypeDef",
    {
        "status": str,
        "payload": RefreshStatisticsIdMapTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ManageSparqlStatisticsOutputTypeDef = TypedDict(
    "ManageSparqlStatisticsOutputTypeDef",
    {
        "status": str,
        "payload": RefreshStatisticsIdMapTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PropertygraphSummaryTypeDef = TypedDict(
    "PropertygraphSummaryTypeDef",
    {
        "numNodes": NotRequired[int],
        "numEdges": NotRequired[int],
        "numNodeLabels": NotRequired[int],
        "numEdgeLabels": NotRequired[int],
        "nodeLabels": NotRequired[List[str]],
        "edgeLabels": NotRequired[List[str]],
        "numNodeProperties": NotRequired[int],
        "numEdgeProperties": NotRequired[int],
        "nodeProperties": NotRequired[List[Dict[str, int]]],
        "edgeProperties": NotRequired[List[Dict[str, int]]],
        "totalNodePropertyValues": NotRequired[int],
        "totalEdgePropertyValues": NotRequired[int],
        "nodeStructures": NotRequired[List[NodeStructureTypeDef]],
        "edgeStructures": NotRequired[List[EdgeStructureTypeDef]],
    },
)

PropertygraphRecordTypeDef = TypedDict(
    "PropertygraphRecordTypeDef",
    {
        "commitTimestampInMillis": int,
        "eventId": Dict[str, str],
        "data": PropertygraphDataTypeDef,
        "op": str,
        "isLastOp": NotRequired[bool],
    },
)

RDFGraphSummaryTypeDef = TypedDict(
    "RDFGraphSummaryTypeDef",
    {
        "numDistinctSubjects": NotRequired[int],
        "numDistinctPredicates": NotRequired[int],
        "numQuads": NotRequired[int],
        "numClasses": NotRequired[int],
        "classes": NotRequired[List[str]],
        "predicates": NotRequired[List[Dict[str, int]]],
        "subjectStructures": NotRequired[List[SubjectStructureTypeDef]],
    },
)

SparqlRecordTypeDef = TypedDict(
    "SparqlRecordTypeDef",
    {
        "commitTimestampInMillis": int,
        "eventId": Dict[str, str],
        "data": SparqlDataTypeDef,
        "op": str,
        "isLastOp": NotRequired[bool],
    },
)

StatisticsTypeDef = TypedDict(
    "StatisticsTypeDef",
    {
        "autoCompute": NotRequired[bool],
        "active": NotRequired[bool],
        "statisticsId": NotRequired[str],
        "date": NotRequired[datetime],
        "note": NotRequired[str],
        "signatureInfo": NotRequired[StatisticsSummaryTypeDef],
    },
)

ListGremlinQueriesOutputTypeDef = TypedDict(
    "ListGremlinQueriesOutputTypeDef",
    {
        "acceptedQueryCount": int,
        "runningQueryCount": int,
        "queries": List[GremlinQueryStatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOpenCypherQueriesOutputTypeDef = TypedDict(
    "ListOpenCypherQueriesOutputTypeDef",
    {
        "acceptedQueryCount": int,
        "runningQueryCount": int,
        "queries": List[GremlinQueryStatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PropertygraphSummaryValueMapTypeDef = TypedDict(
    "PropertygraphSummaryValueMapTypeDef",
    {
        "version": NotRequired[str],
        "lastStatisticsComputationTime": NotRequired[datetime],
        "graphSummary": NotRequired[PropertygraphSummaryTypeDef],
    },
)

GetPropertygraphStreamOutputTypeDef = TypedDict(
    "GetPropertygraphStreamOutputTypeDef",
    {
        "lastEventId": Dict[str, str],
        "lastTrxTimestampInMillis": int,
        "format": str,
        "records": List[PropertygraphRecordTypeDef],
        "totalRecords": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RDFGraphSummaryValueMapTypeDef = TypedDict(
    "RDFGraphSummaryValueMapTypeDef",
    {
        "version": NotRequired[str],
        "lastStatisticsComputationTime": NotRequired[datetime],
        "graphSummary": NotRequired[RDFGraphSummaryTypeDef],
    },
)

GetSparqlStreamOutputTypeDef = TypedDict(
    "GetSparqlStreamOutputTypeDef",
    {
        "lastEventId": Dict[str, str],
        "lastTrxTimestampInMillis": int,
        "format": str,
        "records": List[SparqlRecordTypeDef],
        "totalRecords": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPropertygraphStatisticsOutputTypeDef = TypedDict(
    "GetPropertygraphStatisticsOutputTypeDef",
    {
        "status": str,
        "payload": StatisticsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSparqlStatisticsOutputTypeDef = TypedDict(
    "GetSparqlStatisticsOutputTypeDef",
    {
        "status": str,
        "payload": StatisticsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPropertygraphSummaryOutputTypeDef = TypedDict(
    "GetPropertygraphSummaryOutputTypeDef",
    {
        "statusCode": int,
        "payload": PropertygraphSummaryValueMapTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRDFGraphSummaryOutputTypeDef = TypedDict(
    "GetRDFGraphSummaryOutputTypeDef",
    {
        "statusCode": int,
        "payload": RDFGraphSummaryValueMapTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
