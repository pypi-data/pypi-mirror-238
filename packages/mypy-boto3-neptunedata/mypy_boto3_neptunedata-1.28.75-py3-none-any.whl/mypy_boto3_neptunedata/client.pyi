"""
Type annotations for neptunedata service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_neptunedata.client import NeptuneDataClient

    session = Session()
    client: NeptuneDataClient = session.client("neptunedata")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

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
from .type_defs import (
    CancelGremlinQueryOutputTypeDef,
    CancelLoaderJobOutputTypeDef,
    CancelMLDataProcessingJobOutputTypeDef,
    CancelMLModelTrainingJobOutputTypeDef,
    CancelMLModelTransformJobOutputTypeDef,
    CancelOpenCypherQueryOutputTypeDef,
    CreateMLEndpointOutputTypeDef,
    CustomModelTrainingParametersTypeDef,
    CustomModelTransformParametersTypeDef,
    DeleteMLEndpointOutputTypeDef,
    DeletePropertygraphStatisticsOutputTypeDef,
    DeleteSparqlStatisticsOutputTypeDef,
    ExecuteFastResetOutputTypeDef,
    ExecuteGremlinExplainQueryOutputTypeDef,
    ExecuteGremlinProfileQueryOutputTypeDef,
    ExecuteGremlinQueryOutputTypeDef,
    ExecuteOpenCypherExplainQueryOutputTypeDef,
    ExecuteOpenCypherQueryOutputTypeDef,
    GetEngineStatusOutputTypeDef,
    GetGremlinQueryStatusOutputTypeDef,
    GetLoaderJobStatusOutputTypeDef,
    GetMLDataProcessingJobOutputTypeDef,
    GetMLEndpointOutputTypeDef,
    GetMLModelTrainingJobOutputTypeDef,
    GetMLModelTransformJobOutputTypeDef,
    GetOpenCypherQueryStatusOutputTypeDef,
    GetPropertygraphStatisticsOutputTypeDef,
    GetPropertygraphStreamOutputTypeDef,
    GetPropertygraphSummaryOutputTypeDef,
    GetRDFGraphSummaryOutputTypeDef,
    GetSparqlStatisticsOutputTypeDef,
    GetSparqlStreamOutputTypeDef,
    ListGremlinQueriesOutputTypeDef,
    ListLoaderJobsOutputTypeDef,
    ListMLDataProcessingJobsOutputTypeDef,
    ListMLEndpointsOutputTypeDef,
    ListMLModelTrainingJobsOutputTypeDef,
    ListMLModelTransformJobsOutputTypeDef,
    ListOpenCypherQueriesOutputTypeDef,
    ManagePropertygraphStatisticsOutputTypeDef,
    ManageSparqlStatisticsOutputTypeDef,
    StartLoaderJobOutputTypeDef,
    StartMLDataProcessingJobOutputTypeDef,
    StartMLModelTrainingJobOutputTypeDef,
    StartMLModelTransformJobOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("NeptuneDataClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    BulkLoadIdNotFoundException: Type[BotocoreClientError]
    CancelledByUserException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientTimeoutException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConstraintViolationException: Type[BotocoreClientError]
    ExpiredStreamException: Type[BotocoreClientError]
    FailureByQueryException: Type[BotocoreClientError]
    IllegalArgumentException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidNumericDataException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LoadUrlAccessDeniedException: Type[BotocoreClientError]
    MLResourceNotFoundException: Type[BotocoreClientError]
    MalformedQueryException: Type[BotocoreClientError]
    MemoryLimitExceededException: Type[BotocoreClientError]
    MethodNotAllowedException: Type[BotocoreClientError]
    MissingParameterException: Type[BotocoreClientError]
    ParsingException: Type[BotocoreClientError]
    PreconditionsFailedException: Type[BotocoreClientError]
    QueryLimitExceededException: Type[BotocoreClientError]
    QueryLimitException: Type[BotocoreClientError]
    QueryTooLargeException: Type[BotocoreClientError]
    ReadOnlyViolationException: Type[BotocoreClientError]
    S3Exception: Type[BotocoreClientError]
    ServerShutdownException: Type[BotocoreClientError]
    StatisticsNotAvailableException: Type[BotocoreClientError]
    StreamRecordsNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TimeLimitExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]

class NeptuneDataClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NeptuneDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#can_paginate)
        """

    def cancel_gremlin_query(self, *, queryId: str) -> CancelGremlinQueryOutputTypeDef:
        """
        Cancels a Gremlin query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.cancel_gremlin_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#cancel_gremlin_query)
        """

    def cancel_loader_job(self, *, loadId: str) -> CancelLoaderJobOutputTypeDef:
        """
        Cancels a specified load job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.cancel_loader_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#cancel_loader_job)
        """

    def cancel_ml_data_processing_job(
        self, *, id: str, neptuneIamRoleArn: str = ..., clean: bool = ...
    ) -> CancelMLDataProcessingJobOutputTypeDef:
        """
        Cancels a Neptune ML data processing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.cancel_ml_data_processing_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#cancel_ml_data_processing_job)
        """

    def cancel_ml_model_training_job(
        self, *, id: str, neptuneIamRoleArn: str = ..., clean: bool = ...
    ) -> CancelMLModelTrainingJobOutputTypeDef:
        """
        Cancels a Neptune ML model training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.cancel_ml_model_training_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#cancel_ml_model_training_job)
        """

    def cancel_ml_model_transform_job(
        self, *, id: str, neptuneIamRoleArn: str = ..., clean: bool = ...
    ) -> CancelMLModelTransformJobOutputTypeDef:
        """
        Cancels a specified model transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.cancel_ml_model_transform_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#cancel_ml_model_transform_job)
        """

    def cancel_open_cypher_query(
        self, *, queryId: str, silent: bool = ...
    ) -> CancelOpenCypherQueryOutputTypeDef:
        """
        Cancels a specified openCypher query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.cancel_open_cypher_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#cancel_open_cypher_query)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#close)
        """

    def create_ml_endpoint(
        self,
        *,
        id: str = ...,
        mlModelTrainingJobId: str = ...,
        mlModelTransformJobId: str = ...,
        update: bool = ...,
        neptuneIamRoleArn: str = ...,
        modelName: str = ...,
        instanceType: str = ...,
        instanceCount: int = ...,
        volumeEncryptionKMSKey: str = ...
    ) -> CreateMLEndpointOutputTypeDef:
        """
        Creates a new Neptune ML inference endpoint that lets you query one specific
        model that the model-training process
        constructed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.create_ml_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#create_ml_endpoint)
        """

    def delete_ml_endpoint(
        self, *, id: str, neptuneIamRoleArn: str = ..., clean: bool = ...
    ) -> DeleteMLEndpointOutputTypeDef:
        """
        Cancels the creation of a Neptune ML inference endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.delete_ml_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#delete_ml_endpoint)
        """

    def delete_propertygraph_statistics(self) -> DeletePropertygraphStatisticsOutputTypeDef:
        """
        Deletes statistics for Gremlin and openCypher (property graph) data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.delete_propertygraph_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#delete_propertygraph_statistics)
        """

    def delete_sparql_statistics(self) -> DeleteSparqlStatisticsOutputTypeDef:
        """
        Deletes SPARQL statistics When invoking this operation in a Neptune cluster
        that has IAM authentication enabled, the IAM user or role making the request
        must have a policy attached that allows the `neptune-db:DeleteStatistics
        <https://docs.aws.amazon.com/neptune/latest/userguide/iam-dp-actio...`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.delete_sparql_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#delete_sparql_statistics)
        """

    def execute_fast_reset(
        self, *, action: ActionType, token: str = ...
    ) -> ExecuteFastResetOutputTypeDef:
        """
        The fast reset REST API lets you reset a Neptune graph quicky and easily,
        removing all of its
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.execute_fast_reset)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#execute_fast_reset)
        """

    def execute_gremlin_explain_query(
        self, *, gremlinQuery: str
    ) -> ExecuteGremlinExplainQueryOutputTypeDef:
        """
        Executes a Gremlin Explain query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.execute_gremlin_explain_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#execute_gremlin_explain_query)
        """

    def execute_gremlin_profile_query(
        self,
        *,
        gremlinQuery: str,
        results: bool = ...,
        chop: int = ...,
        serializer: str = ...,
        indexOps: bool = ...
    ) -> ExecuteGremlinProfileQueryOutputTypeDef:
        """
        Executes a Gremlin Profile query, which runs a specified traversal, collects
        various metrics about the run, and produces a profile report as
        output.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.execute_gremlin_profile_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#execute_gremlin_profile_query)
        """

    def execute_gremlin_query(
        self, *, gremlinQuery: str, serializer: str = ...
    ) -> ExecuteGremlinQueryOutputTypeDef:
        """
        This commands executes a Gremlin query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.execute_gremlin_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#execute_gremlin_query)
        """

    def execute_open_cypher_explain_query(
        self, *, openCypherQuery: str, explainMode: OpenCypherExplainModeType, parameters: str = ...
    ) -> ExecuteOpenCypherExplainQueryOutputTypeDef:
        """
        Executes an openCypher `explain` request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.execute_open_cypher_explain_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#execute_open_cypher_explain_query)
        """

    def execute_open_cypher_query(
        self, *, openCypherQuery: str, parameters: str = ...
    ) -> ExecuteOpenCypherQueryOutputTypeDef:
        """
        Executes an openCypher query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.execute_open_cypher_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#execute_open_cypher_query)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#generate_presigned_url)
        """

    def get_engine_status(self) -> GetEngineStatusOutputTypeDef:
        """
        Retrieves the status of the graph database on the host.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_engine_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_engine_status)
        """

    def get_gremlin_query_status(self, *, queryId: str) -> GetGremlinQueryStatusOutputTypeDef:
        """
        Gets the status of a specified Gremlin query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_gremlin_query_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_gremlin_query_status)
        """

    def get_loader_job_status(
        self,
        *,
        loadId: str,
        details: bool = ...,
        errors: bool = ...,
        page: int = ...,
        errorsPerPage: int = ...
    ) -> GetLoaderJobStatusOutputTypeDef:
        """
        Gets status information about a specified load job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_loader_job_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_loader_job_status)
        """

    def get_ml_data_processing_job(
        self, *, id: str, neptuneIamRoleArn: str = ...
    ) -> GetMLDataProcessingJobOutputTypeDef:
        """
        Retrieves information about a specified data processing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_ml_data_processing_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_ml_data_processing_job)
        """

    def get_ml_endpoint(
        self, *, id: str, neptuneIamRoleArn: str = ...
    ) -> GetMLEndpointOutputTypeDef:
        """
        Retrieves details about an inference endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_ml_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_ml_endpoint)
        """

    def get_ml_model_training_job(
        self, *, id: str, neptuneIamRoleArn: str = ...
    ) -> GetMLModelTrainingJobOutputTypeDef:
        """
        Retrieves information about a Neptune ML model training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_ml_model_training_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_ml_model_training_job)
        """

    def get_ml_model_transform_job(
        self, *, id: str, neptuneIamRoleArn: str = ...
    ) -> GetMLModelTransformJobOutputTypeDef:
        """
        Gets information about a specified model transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_ml_model_transform_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_ml_model_transform_job)
        """

    def get_open_cypher_query_status(
        self, *, queryId: str
    ) -> GetOpenCypherQueryStatusOutputTypeDef:
        """
        Retrieves the status of a specified openCypher query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_open_cypher_query_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_open_cypher_query_status)
        """

    def get_propertygraph_statistics(self) -> GetPropertygraphStatisticsOutputTypeDef:
        """
        Gets property graph statistics (Gremlin and openCypher).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_propertygraph_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_propertygraph_statistics)
        """

    def get_propertygraph_stream(
        self,
        *,
        limit: int = ...,
        iteratorType: IteratorTypeType = ...,
        commitNum: int = ...,
        opNum: int = ...,
        encoding: Literal["gzip"] = ...
    ) -> GetPropertygraphStreamOutputTypeDef:
        """
        Gets a stream for a property graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_propertygraph_stream)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_propertygraph_stream)
        """

    def get_propertygraph_summary(
        self, *, mode: GraphSummaryTypeType = ...
    ) -> GetPropertygraphSummaryOutputTypeDef:
        """
        Gets a graph summary for a property graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_propertygraph_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_propertygraph_summary)
        """

    def get_rdf_graph_summary(
        self, *, mode: GraphSummaryTypeType = ...
    ) -> GetRDFGraphSummaryOutputTypeDef:
        """
        Gets a graph summary for an RDF graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_rdf_graph_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_rdf_graph_summary)
        """

    def get_sparql_statistics(self) -> GetSparqlStatisticsOutputTypeDef:
        """
        Gets RDF statistics (SPARQL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_sparql_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_sparql_statistics)
        """

    def get_sparql_stream(
        self,
        *,
        limit: int = ...,
        iteratorType: IteratorTypeType = ...,
        commitNum: int = ...,
        opNum: int = ...,
        encoding: Literal["gzip"] = ...
    ) -> GetSparqlStreamOutputTypeDef:
        """
        Gets a stream for an RDF graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.get_sparql_stream)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#get_sparql_stream)
        """

    def list_gremlin_queries(
        self, *, includeWaiting: bool = ...
    ) -> ListGremlinQueriesOutputTypeDef:
        """
        Lists active Gremlin queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.list_gremlin_queries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#list_gremlin_queries)
        """

    def list_loader_jobs(
        self, *, limit: int = ..., includeQueuedLoads: bool = ...
    ) -> ListLoaderJobsOutputTypeDef:
        """
        Retrieves a list of the `loadIds` for all active loader jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.list_loader_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#list_loader_jobs)
        """

    def list_ml_data_processing_jobs(
        self, *, maxItems: int = ..., neptuneIamRoleArn: str = ...
    ) -> ListMLDataProcessingJobsOutputTypeDef:
        """
        Returns a list of Neptune ML data processing jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.list_ml_data_processing_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#list_ml_data_processing_jobs)
        """

    def list_ml_endpoints(
        self, *, maxItems: int = ..., neptuneIamRoleArn: str = ...
    ) -> ListMLEndpointsOutputTypeDef:
        """
        Lists existing inference endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.list_ml_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#list_ml_endpoints)
        """

    def list_ml_model_training_jobs(
        self, *, maxItems: int = ..., neptuneIamRoleArn: str = ...
    ) -> ListMLModelTrainingJobsOutputTypeDef:
        """
        Lists Neptune ML model-training jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.list_ml_model_training_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#list_ml_model_training_jobs)
        """

    def list_ml_model_transform_jobs(
        self, *, maxItems: int = ..., neptuneIamRoleArn: str = ...
    ) -> ListMLModelTransformJobsOutputTypeDef:
        """
        Returns a list of model transform job IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.list_ml_model_transform_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#list_ml_model_transform_jobs)
        """

    def list_open_cypher_queries(
        self, *, includeWaiting: bool = ...
    ) -> ListOpenCypherQueriesOutputTypeDef:
        """
        Lists active openCypher queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.list_open_cypher_queries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#list_open_cypher_queries)
        """

    def manage_propertygraph_statistics(
        self, *, mode: StatisticsAutoGenerationModeType = ...
    ) -> ManagePropertygraphStatisticsOutputTypeDef:
        """
        Manages the generation and use of property graph statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.manage_propertygraph_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#manage_propertygraph_statistics)
        """

    def manage_sparql_statistics(
        self, *, mode: StatisticsAutoGenerationModeType = ...
    ) -> ManageSparqlStatisticsOutputTypeDef:
        """
        Manages the generation and use of RDF graph statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.manage_sparql_statistics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#manage_sparql_statistics)
        """

    def start_loader_job(
        self,
        *,
        source: str,
        format: FormatType,
        s3BucketRegion: S3BucketRegionType,
        iamRoleArn: str,
        mode: ModeType = ...,
        failOnError: bool = ...,
        parallelism: ParallelismType = ...,
        parserConfiguration: Mapping[str, str] = ...,
        updateSingleCardinalityProperties: bool = ...,
        queueRequest: bool = ...,
        dependencies: Sequence[str] = ...,
        userProvidedEdgeIds: bool = ...
    ) -> StartLoaderJobOutputTypeDef:
        """
        Starts a Neptune bulk loader job to load data from an Amazon S3 bucket into a
        Neptune DB
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.start_loader_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#start_loader_job)
        """

    def start_ml_data_processing_job(
        self,
        *,
        inputDataS3Location: str,
        processedDataS3Location: str,
        id: str = ...,
        previousDataProcessingJobId: str = ...,
        sagemakerIamRoleArn: str = ...,
        neptuneIamRoleArn: str = ...,
        processingInstanceType: str = ...,
        processingInstanceVolumeSizeInGB: int = ...,
        processingTimeOutInSeconds: int = ...,
        modelType: str = ...,
        configFileName: str = ...,
        subnets: Sequence[str] = ...,
        securityGroupIds: Sequence[str] = ...,
        volumeEncryptionKMSKey: str = ...,
        s3OutputEncryptionKMSKey: str = ...
    ) -> StartMLDataProcessingJobOutputTypeDef:
        """
        Creates a new Neptune ML data processing job for processing the graph data
        exported from Neptune for
        training.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.start_ml_data_processing_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#start_ml_data_processing_job)
        """

    def start_ml_model_training_job(
        self,
        *,
        dataProcessingJobId: str,
        trainModelS3Location: str,
        id: str = ...,
        previousModelTrainingJobId: str = ...,
        sagemakerIamRoleArn: str = ...,
        neptuneIamRoleArn: str = ...,
        baseProcessingInstanceType: str = ...,
        trainingInstanceType: str = ...,
        trainingInstanceVolumeSizeInGB: int = ...,
        trainingTimeOutInSeconds: int = ...,
        maxHPONumberOfTrainingJobs: int = ...,
        maxHPOParallelTrainingJobs: int = ...,
        subnets: Sequence[str] = ...,
        securityGroupIds: Sequence[str] = ...,
        volumeEncryptionKMSKey: str = ...,
        s3OutputEncryptionKMSKey: str = ...,
        enableManagedSpotTraining: bool = ...,
        customModelTrainingParameters: CustomModelTrainingParametersTypeDef = ...
    ) -> StartMLModelTrainingJobOutputTypeDef:
        """
        Creates a new Neptune ML model training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.start_ml_model_training_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#start_ml_model_training_job)
        """

    def start_ml_model_transform_job(
        self,
        *,
        modelTransformOutputS3Location: str,
        id: str = ...,
        dataProcessingJobId: str = ...,
        mlModelTrainingJobId: str = ...,
        trainingJobName: str = ...,
        sagemakerIamRoleArn: str = ...,
        neptuneIamRoleArn: str = ...,
        customModelTransformParameters: CustomModelTransformParametersTypeDef = ...,
        baseProcessingInstanceType: str = ...,
        baseProcessingInstanceVolumeSizeInGB: int = ...,
        subnets: Sequence[str] = ...,
        securityGroupIds: Sequence[str] = ...,
        volumeEncryptionKMSKey: str = ...,
        s3OutputEncryptionKMSKey: str = ...
    ) -> StartMLModelTransformJobOutputTypeDef:
        """
        Creates a new model transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client.start_ml_model_transform_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_neptunedata/client/#start_ml_model_transform_job)
        """
