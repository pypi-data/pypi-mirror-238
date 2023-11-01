import sgqlc.types

schema = sgqlc.types.Schema()


__docformat__ = "markdown"


########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean


class ExecutorMethodName(sgqlc.types.Enum):
    """Enumeration Choices:

    * `execute`None
    """

    __schema__ = schema
    __choices__ = ("execute",)


Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int


class JSON(sgqlc.types.Scalar):
    """The `JSON` scalar type represents JSON values as specified by
    [ECMA-404](http://www.ecma-
    international.org/publications/files/ECMA-ST/ECMA-404.pdf).
    """

    __schema__ = schema


class JobStatus(sgqlc.types.Enum):
    """Enumeration Choices:

    * `BUILDING`None
    * `EXECUTING`None
    * `FAILED`None
    * `PLANNED`None
    * `SUCCESSFUL`None
    """

    __schema__ = schema
    __choices__ = ("BUILDING", "EXECUTING", "FAILED", "PLANNED", "SUCCESSFUL")


class LONG(sgqlc.types.Scalar):
    """The `LONG` scalar type represents long int type."""

    __schema__ = schema


class ModelMethodName(sgqlc.types.Enum):
    """Enumeration Choices:

    * `evaluate_function`None
    * `finetune_function`None
    * `get_losses`None
    * `get_nn_module`None
    * `get_target_layer`None
    * `predict_function`None
    * `train_function`None
    """

    __schema__ = schema
    __choices__ = (
        "evaluate_function",
        "finetune_function",
        "get_losses",
        "get_nn_module",
        "get_target_layer",
        "predict_function",
        "train_function",
    )


class PeriodicType(sgqlc.types.Enum):
    """Enumeration Choices:

    * `ONCE`None
    * `PERIODIC`None
    """

    __schema__ = schema
    __choices__ = ("ONCE", "PERIODIC")


String = sgqlc.types.String


class UploadModelMode(sgqlc.types.Enum):
    """Enumeration Choices:

    * `new_model`None
    * `new_version`None
    * `none`None
    """

    __schema__ = schema
    __choices__ = ("new_model", "new_version", "none")


class UploadModelType(sgqlc.types.Enum):
    """Enumeration Choices:

    * `new_model`None
    * `new_version`None
    * `root`None
    """

    __schema__ = schema
    __choices__ = ("new_model", "new_version", "root")


########################################################################
# Input Objects
########################################################################
class DataParamsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ("dataset_loader_method_params", "collector_method_params")
    dataset_loader_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParamsInput"), graphql_name="datasetLoaderMethodParams")

    collector_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParamsInput"), graphql_name="collectorMethodParams")


class ExecutorModelParamsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ("executor_method_params", "model_methods_params")
    executor_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParamsInput"), graphql_name="executorMethodParams")

    model_methods_params = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MethodParamsInput"))), graphql_name="modelMethodsParams"
    )


class MethodParamsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ("method_name", "method_params")
    method_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="methodName")

    method_params = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="methodParams")


class ObjectVersionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ("name", "version")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")


class TimestampInterval(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ("start", "end")
    start = sgqlc.types.Field(LONG, graphql_name="start")

    end = sgqlc.types.Field(LONG, graphql_name="end")


########################################################################
# Output Objects and Interfaces
########################################################################
class DataParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("dataset_loader_method_params", "collector_method_params")
    dataset_loader_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParams"), graphql_name="datasetLoaderMethodParams")

    collector_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParams"), graphql_name="collectorMethodParams")


class DataSchema(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("dataset_loader_method_schema", "collector_method_schema")
    dataset_loader_method_schema = sgqlc.types.Field(sgqlc.types.non_null("MethodSchema"), graphql_name="datasetLoaderMethodSchema")

    collector_method_schema = sgqlc.types.Field(sgqlc.types.non_null("MethodSchema"), graphql_name="collectorMethodSchema")


class DatasetLoader(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "name",
        "description",
        "owner_id",
        "tags",
        "creation_timestamp",
        "last_updated_timestamp",
        "owner",
        "latest_dataset_loader_version",
        "init_dataset_loader_version",
        "list_dataset_loader_version",
        "pagination_dataset_loader_version",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="name")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    owner_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="ownerId")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    owner = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="owner")

    latest_dataset_loader_version = sgqlc.types.Field(
        sgqlc.types.non_null("DatasetLoaderVersion"), graphql_name="latestDatasetLoaderVersion"
    )

    init_dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null("DatasetLoaderVersion"), graphql_name="initDatasetLoaderVersion")

    list_dataset_loader_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("DatasetLoaderVersion"))), graphql_name="listDatasetLoaderVersion"
    )

    pagination_dataset_loader_version = sgqlc.types.Field(
        sgqlc.types.non_null("DatasetLoaderVersionPagination"),
        graphql_name="paginationDatasetLoaderVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """


class DatasetLoaderPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("list_dataset_loader", "total")
    list_dataset_loader = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoader))), graphql_name="listDatasetLoader"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class DatasetLoaderVersion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "name",
        "version",
        "run_id",
        "source_path",
        "tags",
        "description",
        "status",
        "status_message",
        "creation_timestamp",
        "last_updated_timestamp",
        "dataset_loader_method_schema",
        "dataset_loader_method_schema_name",
        "run",
        "dataset_loader",
        "data_json_schema",
        "list_deployed_jobs",
        "pagination_deployed_jobs",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")

    run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="runId")

    source_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sourcePath")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")

    status_message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="statusMessage")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    dataset_loader_method_schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="datasetLoaderMethodSchema")

    dataset_loader_method_schema_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="datasetLoaderMethodSchemaName")

    run = sgqlc.types.Field(sgqlc.types.non_null("Run"), graphql_name="run")

    dataset_loader = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoader), graphql_name="datasetLoader")

    data_json_schema = sgqlc.types.Field(
        sgqlc.types.non_null(DataSchema),
        graphql_name="dataJsonSchema",
        args=sgqlc.types.ArgDict(
            (("collector_name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="collectorName", default=None)),)
        ),
    )
    """Arguments:

    * `collector_name` (`String!`)None
    """

    list_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Job"))), graphql_name="listDeployedJobs"
    )

    pagination_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null("JobPagination"),
        graphql_name="paginationDeployedJobs",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """


class DatasetLoaderVersionPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("list_dataset_loader_version", "total")
    list_dataset_loader_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoaderVersion))), graphql_name="listDatasetLoaderVersion"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class Executor(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "name",
        "description",
        "owner_id",
        "tags",
        "creation_timestamp",
        "last_updated_timestamp",
        "owner",
        "latest_executor_version",
        "init_executor_version",
        "list_executor_version",
        "pagination_executor_version",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="name")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    owner_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="ownerId")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    owner = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="owner")

    latest_executor_version = sgqlc.types.Field(sgqlc.types.non_null("ExecutorVersion"), graphql_name="latestExecutorVersion")

    init_executor_version = sgqlc.types.Field(sgqlc.types.non_null("ExecutorVersion"), graphql_name="initExecutorVersion")

    list_executor_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ExecutorVersion"))), graphql_name="listExecutorVersion"
    )

    pagination_executor_version = sgqlc.types.Field(
        sgqlc.types.non_null("ExecutorVersionPagination"),
        graphql_name="paginationExecutorVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """


class ExecutorModelParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("executor_method_params", "model_methods_params")
    executor_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParams"), graphql_name="executorMethodParams")

    model_methods_params = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MethodParams"))), graphql_name="modelMethodsParams"
    )


class ExecutorPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("list_executor", "total")
    list_executor = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Executor))), graphql_name="listExecutor"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class ExecutorVersion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "name",
        "version",
        "run_id",
        "source_path",
        "tags",
        "description",
        "status",
        "status_message",
        "creation_timestamp",
        "last_updated_timestamp",
        "executor_method_schema",
        "executor_method_schema_name",
        "desired_model_methods",
        "desired_model_patterns",
        "upload_model_mode",
        "run",
        "executor",
        "list_deployed_jobs",
        "pagination_deployed_jobs",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")

    run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="runId")

    source_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sourcePath")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")

    status_message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="statusMessage")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    executor_method_schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="executorMethodSchema")

    executor_method_schema_name = sgqlc.types.Field(sgqlc.types.non_null(ExecutorMethodName), graphql_name="executorMethodSchemaName")

    desired_model_methods = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelMethodName))), graphql_name="desiredModelMethods"
    )

    desired_model_patterns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name="desiredModelPatterns"
    )

    upload_model_mode = sgqlc.types.Field(sgqlc.types.non_null(UploadModelMode), graphql_name="uploadModelMode")

    run = sgqlc.types.Field(sgqlc.types.non_null("Run"), graphql_name="run")

    executor = sgqlc.types.Field(sgqlc.types.non_null(Executor), graphql_name="executor")

    list_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Job"))), graphql_name="listDeployedJobs"
    )

    pagination_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null("JobPagination"),
        graphql_name="paginationDeployedJobs",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """


class ExecutorVersionPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("list_executor_version", "total")
    list_executor_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutorVersion))), graphql_name="listExecutorVersion"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class Experiment(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("name", "experiment_id", "artifact_location", "lifecycle_stage", "list_run", "pagination_run", "tags")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    experiment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="experimentId")

    artifact_location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="artifactLocation")

    lifecycle_stage = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="lifecycleStage")

    list_run = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Run"))), graphql_name="listRun")

    pagination_run = sgqlc.types.Field(
        sgqlc.types.non_null("RunPagination"),
        graphql_name="paginationRun",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")


class ExperimentPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("list_experiment", "total")
    list_experiment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Experiment))), graphql_name="listExperiment"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class GraphNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "run_id",
        "name",
        "version",
        "source_run_id",
        "source_name",
        "source_version",
        "root_run_id",
        "upload_model_type",
        "list_next_node",
    )
    run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="runId")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")

    source_run_id = sgqlc.types.Field(ID, graphql_name="sourceRunId")

    source_name = sgqlc.types.Field(String, graphql_name="sourceName")

    source_version = sgqlc.types.Field(String, graphql_name="sourceVersion")

    root_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="rootRunId")

    upload_model_type = sgqlc.types.Field(sgqlc.types.non_null(UploadModelType), graphql_name="uploadModelType")

    list_next_node = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("GraphNode")), graphql_name="listNextNode")


class Job(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "name",
        "owner_id",
        "periodic_type",
        "status",
        "experiment_name",
        "registration_timestamp",
        "start_timestamp",
        "end_timestamp",
        "start_build_timestamp",
        "end_build_timestamp",
        "exception",
        "exception_traceback",
        "job_run_id",
        "init_model_version_run_id",
        "dataset_loader_version_run_id",
        "executor_version_run_id",
        "params",
        "run",
        "experiment",
        "init_model_version",
        "dataset_loader_version",
        "executor_version",
        "result_model_version",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="name")

    owner_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="ownerId")

    periodic_type = sgqlc.types.Field(sgqlc.types.non_null(PeriodicType), graphql_name="periodicType")

    status = sgqlc.types.Field(sgqlc.types.non_null(JobStatus), graphql_name="status")

    experiment_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="experimentName")

    registration_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="registrationTimestamp")

    start_timestamp = sgqlc.types.Field(LONG, graphql_name="startTimestamp")

    end_timestamp = sgqlc.types.Field(LONG, graphql_name="endTimestamp")

    start_build_timestamp = sgqlc.types.Field(LONG, graphql_name="startBuildTimestamp")

    end_build_timestamp = sgqlc.types.Field(LONG, graphql_name="endBuildTimestamp")

    exception = sgqlc.types.Field(String, graphql_name="exception")

    exception_traceback = sgqlc.types.Field(String, graphql_name="exceptionTraceback")

    job_run_id = sgqlc.types.Field(String, graphql_name="jobRunId")

    init_model_version_run_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="initModelVersionRunId")

    dataset_loader_version_run_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="datasetLoaderVersionRunId")

    executor_version_run_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="executorVersionRunId")

    params = sgqlc.types.Field(sgqlc.types.non_null("JobParams"), graphql_name="params")

    run = sgqlc.types.Field("Run", graphql_name="run")

    experiment = sgqlc.types.Field(Experiment, graphql_name="experiment")

    init_model_version = sgqlc.types.Field(sgqlc.types.non_null("ModelVersion"), graphql_name="initModelVersion")

    dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderVersion), graphql_name="datasetLoaderVersion")

    executor_version = sgqlc.types.Field(sgqlc.types.non_null(ExecutorVersion), graphql_name="executorVersion")

    result_model_version = sgqlc.types.Field("ModelVersion", graphql_name="resultModelVersion")


class JobPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("list_job", "total")
    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Job))), graphql_name="listJob")

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class JobParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "name",
        "job_executor_name",
        "job_executor_version",
        "dataset_loader_name",
        "dataset_loader_version",
        "model_name",
        "model_version",
        "new_model_name",
        "experiment_name",
        "cron_expression",
        "periodic_type",
        "metric_name",
        "optimal_min",
        "choice_criteria",
        "executor_model_params",
        "data_params",
        "collector_name",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    job_executor_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="jobExecutorName")

    job_executor_version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="jobExecutorVersion")

    dataset_loader_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="datasetLoaderName")

    dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="datasetLoaderVersion")

    model_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="modelName")

    model_version = sgqlc.types.Field(Int, graphql_name="modelVersion")

    new_model_name = sgqlc.types.Field(String, graphql_name="newModelName")

    experiment_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="experimentName")

    cron_expression = sgqlc.types.Field(String, graphql_name="cronExpression")

    periodic_type = sgqlc.types.Field(sgqlc.types.non_null(PeriodicType), graphql_name="periodicType")

    metric_name = sgqlc.types.Field(String, graphql_name="metricName")

    optimal_min = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="optimalMin")

    choice_criteria = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="choiceCriteria")

    executor_model_params = sgqlc.types.Field(sgqlc.types.non_null(ExecutorModelParams), graphql_name="executorModelParams")

    data_params = sgqlc.types.Field(sgqlc.types.non_null(DataParams), graphql_name="dataParams")

    collector_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="collectorName")


class JobSchema(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("executor_method_schema", "model_methods_schema")
    executor_method_schema = sgqlc.types.Field(sgqlc.types.non_null("MethodSchema"), graphql_name="executorMethodSchema")

    model_methods_schema = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MethodSchema"))), graphql_name="modelMethodsSchema"
    )


class MethodParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("method_name", "method_params")
    method_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="methodName")

    method_params = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="methodParams")


class MethodSchema(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("schema_name", "json_schema")
    schema_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="schemaName")

    json_schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="jsonSchema")


class Metric(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("key", "value", "step", "timestamp")
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    value = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name="value")

    step = sgqlc.types.Field(Int, graphql_name="step")

    timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="timestamp")


class Model(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "name",
        "description",
        "owner_id",
        "tags",
        "creation_timestamp",
        "last_updated_timestamp",
        "owner",
        "latest_model_version",
        "init_model_version",
        "list_model_version",
        "pagination_model_version",
        "best_model_version",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="name")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    owner_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="ownerId")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    owner = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="owner")

    latest_model_version = sgqlc.types.Field(sgqlc.types.non_null("ModelVersion"), graphql_name="latestModelVersion")

    init_model_version = sgqlc.types.Field("ModelVersion", graphql_name="initModelVersion")

    list_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listModelVersion"
    )

    pagination_model_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationModelVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    best_model_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersion"),
        graphql_name="bestModelVersion",
        args=sgqlc.types.ArgDict(
            (
                ("metric", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="metric", default=None)),
                ("optimal_min", sgqlc.types.Arg(Boolean, graphql_name="optimalMin", default=False)),
            )
        ),
    )
    """Arguments:

    * `metric` (`String!`)None
    * `optimal_min` (`Boolean`)None (default: `false`)
    """


class ModelPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("list_model", "total")
    list_model = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Model))), graphql_name="listModel")

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class ModelVersion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "name",
        "version",
        "source_path",
        "run_id",
        "root_run_id",
        "source_run_id",
        "source_model_name",
        "source_model_version",
        "default_experiment_name",
        "tags",
        "eval_run_ids",
        "description",
        "status",
        "status_message",
        "creation_timestamp",
        "last_updated_timestamp",
        "upload_model_type",
        "model_methods_schema",
        "docker_image_tag",
        "list_deployed_jobs",
        "pagination_deployed_jobs",
        "list_eval_run",
        "pagination_eval_run",
        "run",
        "source_run",
        "root_run",
        "model",
        "job_json_schema",
        "available_executor_versions",
        "available_dataset_loaders",
        "available_collectors",
        "list_next_graph_nodes",
        "list_next_model_version",
        "list_new_model_from_version",
        "list_new_version_from_version",
        "pagination_next_model_version",
        "pagination_new_model_from_version",
        "pagination_new_version_from_version",
        "root_model_version",
        "list_lineage_model_version",
        "pagination_lineage_model_version",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")

    source_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sourcePath")

    run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="runId")

    root_run_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="rootRunId")

    source_run_id = sgqlc.types.Field(String, graphql_name="sourceRunId")

    source_model_name = sgqlc.types.Field(String, graphql_name="sourceModelName")

    source_model_version = sgqlc.types.Field("ModelVersion", graphql_name="sourceModelVersion")

    default_experiment_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="defaultExperimentName")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    eval_run_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name="evalRunIds")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")

    status_message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="statusMessage")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    upload_model_type = sgqlc.types.Field(sgqlc.types.non_null(UploadModelType), graphql_name="uploadModelType")

    model_methods_schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="modelMethodsSchema")

    docker_image_tag = sgqlc.types.Field(String, graphql_name="dockerImageTag")

    list_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Job))), graphql_name="listDeployedJobs"
    )

    pagination_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null(JobPagination),
        graphql_name="paginationDeployedJobs",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    list_eval_run = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Run"))), graphql_name="listEvalRun")

    pagination_eval_run = sgqlc.types.Field(
        sgqlc.types.non_null("RunPagination"),
        graphql_name="paginationEvalRun",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    run = sgqlc.types.Field(sgqlc.types.non_null("Run"), graphql_name="run")

    source_run = sgqlc.types.Field("Run", graphql_name="sourceRun")

    root_run = sgqlc.types.Field(sgqlc.types.non_null("Run"), graphql_name="rootRun")

    model = sgqlc.types.Field(sgqlc.types.non_null(Model), graphql_name="model")

    job_json_schema = sgqlc.types.Field(
        sgqlc.types.non_null(JobSchema),
        graphql_name="jobJsonSchema",
        args=sgqlc.types.ArgDict(
            (
                ("executor_name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="executorName", default=None)),
                ("executor_version", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="executorVersion", default=None)),
            )
        ),
    )
    """Arguments:

    * `executor_name` (`String!`)None
    * `executor_version` (`Int!`)None
    """

    available_executor_versions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutorVersion))), graphql_name="availableExecutorVersions"
    )

    available_dataset_loaders = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoader))), graphql_name="availableDatasetLoaders"
    )

    available_collectors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name="availableCollectors"
    )

    list_next_graph_nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GraphNode))), graphql_name="listNextGraphNodes"
    )

    list_next_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listNextModelVersion"
    )

    list_new_model_from_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listNewModelFromVersion"
    )

    list_new_version_from_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listNewVersionFromVersion"
    )

    pagination_next_model_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationNextModelVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    pagination_new_model_from_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationNewModelFromVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    pagination_new_version_from_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationNewVersionFromVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    root_model_version = sgqlc.types.Field(sgqlc.types.non_null("ModelVersion"), graphql_name="rootModelVersion")

    list_lineage_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listLineageModelVersion"
    )

    pagination_lineage_model_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationLineageModelVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """


class ModelVersionPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("list_model_version", "total")
    list_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelVersion))), graphql_name="listModelVersion"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class Mutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "rename_experiment",
        "add_ml_job",
        "delete_model",
        "set_model_tag",
        "delete_model_tag",
        "set_model_description",
        "delete_model_version_from_name_version",
        "set_model_version_tag",
        "delete_model_version_tag",
        "set_model_version_description",
        "delete_dataset_loader",
        "set_dataset_loader_tag",
        "delete_dataset_loader_tag",
        "set_dataset_loader_description",
        "delete_dataset_loader_version_from_name_version",
        "set_dataset_loader_version_tag",
        "delete_dataset_loader_version_tag",
        "set_dataset_loader_version_description",
        "delete_executor",
        "set_executor_tag",
        "delete_executor_tag",
        "set_executor_description",
        "delete_executor_version_from_name_version",
        "set_executor_version_tag",
        "delete_executor_version_tag",
        "set_executor_version_description",
    )
    rename_experiment = sgqlc.types.Field(
        sgqlc.types.non_null(Experiment),
        graphql_name="renameExperiment",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("new_name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="newName", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `new_name` (`String!`)None
    """

    add_ml_job = sgqlc.types.Field(
        sgqlc.types.non_null(Job),
        graphql_name="addMlJob",
        args=sgqlc.types.ArgDict(
            (
                ("job_executor_name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="jobExecutorName", default=None)),
                ("model_name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="modelName", default=None)),
                ("dataset_loader_name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="datasetLoaderName", default=None)),
                (
                    "executor_model_params",
                    sgqlc.types.Arg(sgqlc.types.non_null(ExecutorModelParamsInput), graphql_name="executorModelParams", default=None),
                ),
                ("data_params", sgqlc.types.Arg(sgqlc.types.non_null(DataParamsInput), graphql_name="dataParams", default=None)),
                ("collector_name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="collectorName", default=None)),
                ("choice_criteria", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="choiceCriteria", default="latest")),
                ("dataset_loader_version", sgqlc.types.Arg(Int, graphql_name="datasetLoaderVersion", default=None)),
                ("job_executor_version", sgqlc.types.Arg(Int, graphql_name="jobExecutorVersion", default=None)),
                ("model_version", sgqlc.types.Arg(Int, graphql_name="modelVersion", default=None)),
                ("new_model_name", sgqlc.types.Arg(String, graphql_name="newModelName", default=None)),
                ("experiment_name", sgqlc.types.Arg(String, graphql_name="experimentName", default=None)),
                ("cron_expression", sgqlc.types.Arg(String, graphql_name="cronExpression", default=None)),
                ("periodic_type", sgqlc.types.Arg(PeriodicType, graphql_name="periodicType", default="ONCE")),
                ("metric_name", sgqlc.types.Arg(String, graphql_name="metricName", default=None)),
                ("optimal_min", sgqlc.types.Arg(sgqlc.types.non_null(Boolean), graphql_name="optimalMin", default=False)),
                ("force_rebuild", sgqlc.types.Arg(Boolean, graphql_name="forceRebuild", default=False)),
                ("gpu", sgqlc.types.Arg(Boolean, graphql_name="gpu", default=False)),
            )
        ),
    )
    """Arguments:

    * `job_executor_name` (`String!`)None
    * `model_name` (`String!`)None
    * `dataset_loader_name` (`String!`)None
    * `executor_model_params` (`ExecutorModelParamsInput!`)None
    * `data_params` (`DataParamsInput!`)None
    * `collector_name` (`String!`)None
    * `choice_criteria` (`String!`)None (default: `"latest"`)
    * `dataset_loader_version` (`Int`)None (default: `null`)
    * `job_executor_version` (`Int`)None (default: `null`)
    * `model_version` (`Int`)None (default: `null`)
    * `new_model_name` (`String`)None (default: `null`)
    * `experiment_name` (`String`)None (default: `null`)
    * `cron_expression` (`String`)None (default: `null`)
    * `periodic_type` (`PeriodicType`)None (default: `ONCE`)
    * `metric_name` (`String`)None (default: `null`)
    * `optimal_min` (`Boolean!`)None (default: `false`)
    * `force_rebuild` (`Boolean`)None (default: `false`)
    * `gpu` (`Boolean`)None (default: `false`)
    """

    delete_model = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteModel",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    set_model_tag = sgqlc.types.Field(
        sgqlc.types.non_null(Model),
        graphql_name="setModelTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_model_tag = sgqlc.types.Field(
        sgqlc.types.non_null(Model),
        graphql_name="deleteModelTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    """

    set_model_description = sgqlc.types.Field(
        sgqlc.types.non_null(Model),
        graphql_name="setModelDescription",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `description` (`String!`)None
    """

    delete_model_version_from_name_version = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteModelVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (("model_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="modelVersion", default=None)),)
        ),
    )
    """Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    """

    set_model_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersion),
        graphql_name="setModelVersionTag",
        args=sgqlc.types.ArgDict(
            (
                ("model_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="modelVersion", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_model_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersion),
        graphql_name="deleteModelVersionTag",
        args=sgqlc.types.ArgDict(
            (
                ("model_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="modelVersion", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    """

    set_model_version_description = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersion),
        graphql_name="setModelVersionDescription",
        args=sgqlc.types.ArgDict(
            (
                ("model_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="modelVersion", default=None)),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    * `description` (`String!`)None
    """

    delete_dataset_loader = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteDatasetLoader",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    set_dataset_loader_tag = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoader),
        graphql_name="setDatasetLoaderTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_dataset_loader_tag = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoader),
        graphql_name="deleteDatasetLoaderTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    """

    set_dataset_loader_description = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoader),
        graphql_name="setDatasetLoaderDescription",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `description` (`String!`)None
    """

    delete_dataset_loader_version_from_name_version = sgqlc.types.Field(
        Boolean,
        graphql_name="deleteDatasetLoaderVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dataset_loader_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="datasetLoaderVersion", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    """

    set_dataset_loader_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderVersion),
        graphql_name="setDatasetLoaderVersionTag",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dataset_loader_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="datasetLoaderVersion", default=None),
                ),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_dataset_loader_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderVersion),
        graphql_name="deleteDatasetLoaderVersionTag",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dataset_loader_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="datasetLoaderVersion", default=None),
                ),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    """

    set_dataset_loader_version_description = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderVersion),
        graphql_name="setDatasetLoaderVersionDescription",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dataset_loader_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="datasetLoaderVersion", default=None),
                ),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    * `description` (`String!`)None
    """

    delete_executor = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteExecutor",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    set_executor_tag = sgqlc.types.Field(
        sgqlc.types.non_null(Executor),
        graphql_name="setExecutorTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_executor_tag = sgqlc.types.Field(
        sgqlc.types.non_null(Executor),
        graphql_name="deleteExecutorTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    """

    set_executor_description = sgqlc.types.Field(
        sgqlc.types.non_null(Executor),
        graphql_name="setExecutorDescription",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `description` (`String!`)None
    """

    delete_executor_version_from_name_version = sgqlc.types.Field(
        Boolean,
        graphql_name="deleteExecutorVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (("executor_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="executorVersion", default=None)),)
        ),
    )
    """Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    """

    set_executor_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersion),
        graphql_name="setExecutorVersionTag",
        args=sgqlc.types.ArgDict(
            (
                (
                    "executor_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="executorVersion", default=None),
                ),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_executor_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersion),
        graphql_name="deleteExecutorVersionTag",
        args=sgqlc.types.ArgDict(
            (
                (
                    "executor_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="executorVersion", default=None),
                ),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    """

    set_executor_version_description = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersion),
        graphql_name="setExecutorVersionDescription",
        args=sgqlc.types.ArgDict(
            (
                (
                    "executor_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="executorVersion", default=None),
                ),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    * `description` (`String!`)None
    """


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "graph_node",
        "list_graph_node",
        "list_subtree_graph_node",
        "run_from_run_id",
        "search_runs",
        "list_experiment",
        "pagination_experiment",
        "experiment_from_name",
        "experiment_from_id",
        "job_from_name",
        "list_job",
        "pagination_job",
        "search_job",
        "model_from_name",
        "warning_delete_model_query",
        "list_model",
        "pagination_model",
        "model_version_from_run_id",
        "model_version_from_name_version",
        "list_initial_model_version",
        "pagination_initial_model_version",
        "list_dataset_loader",
        "pagination_dataset_loader",
        "dataset_loader_from_name",
        "dataset_loader_version_from_name_version",
        "dataset_loader_version_from_run_id",
        "executor_from_name",
        "list_executor",
        "pagination_executor",
        "executor_version_from_name_version",
        "executor_version_from_run_id",
        "list_initial_executor_version",
    )
    graph_node = sgqlc.types.Field(
        sgqlc.types.non_null(GraphNode),
        graphql_name="graphNode",
        args=sgqlc.types.ArgDict((("run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="runId", default=None)),)),
    )
    """Arguments:

    * `run_id` (`String!`)None
    """

    list_graph_node = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GraphNode))), graphql_name="listGraphNode"
    )

    list_subtree_graph_node = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GraphNode))),
        graphql_name="listSubtreeGraphNode",
        args=sgqlc.types.ArgDict((("root_run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="rootRunId", default=None)),)),
    )
    """Arguments:

    * `root_run_id` (`String!`)None
    """

    run_from_run_id = sgqlc.types.Field(
        sgqlc.types.non_null("Run"),
        graphql_name="runFromRunId",
        args=sgqlc.types.ArgDict((("run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="runId", default=None)),)),
    )
    """Arguments:

    * `run_id` (`String!`)None
    """

    search_runs = sgqlc.types.Field(
        sgqlc.types.non_null("RunPagination"),
        graphql_name="searchRuns",
        args=sgqlc.types.ArgDict(
            (
                (
                    "experiment_ids",
                    sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="experimentIds", default=None),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                ("filter_string", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="filterString", default="")),
                ("run_view_type", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="runViewType", default=1)),
                ("order_by", sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="orderBy", default=None)),
                (
                    "experiment_names",
                    sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="experimentNames", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `experiment_ids` (`[String!]`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `filter_string` (`String!`)None (default: `""`)
    * `run_view_type` (`Int!`)None (default: `1`)
    * `order_by` (`[String!]`)None (default: `null`)
    * `experiment_names` (`[String!]`)None (default: `null`)
    """

    list_experiment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Experiment))), graphql_name="listExperiment"
    )

    pagination_experiment = sgqlc.types.Field(
        sgqlc.types.non_null(ExperimentPagination),
        graphql_name="paginationExperiment",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    experiment_from_name = sgqlc.types.Field(
        sgqlc.types.non_null(Experiment),
        graphql_name="experimentFromName",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    experiment_from_id = sgqlc.types.Field(
        sgqlc.types.non_null(Experiment),
        graphql_name="experimentFromId",
        args=sgqlc.types.ArgDict(
            (("experiment_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="experimentId", default=None)),)
        ),
    )
    """Arguments:

    * `experiment_id` (`String!`)None
    """

    job_from_name = sgqlc.types.Field(
        sgqlc.types.non_null(Job),
        graphql_name="jobFromName",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Job))), graphql_name="listJob")

    pagination_job = sgqlc.types.Field(
        sgqlc.types.non_null(JobPagination),
        graphql_name="paginationJob",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    search_job = sgqlc.types.Field(
        sgqlc.types.non_null(JobPagination),
        graphql_name="searchJob",
        args=sgqlc.types.ArgDict(
            (
                ("periodic_type", sgqlc.types.Arg(PeriodicType, graphql_name="periodicType", default=None)),
                ("status", sgqlc.types.Arg(JobStatus, graphql_name="status", default=None)),
                ("init_model_version", sgqlc.types.Arg(ObjectVersionInput, graphql_name="initModelVersion", default=None)),
                ("dataset_loader_version", sgqlc.types.Arg(ObjectVersionInput, graphql_name="datasetLoaderVersion", default=None)),
                ("executor_version", sgqlc.types.Arg(ObjectVersionInput, graphql_name="executorVersion", default=None)),
                ("start_interval", sgqlc.types.Arg(TimestampInterval, graphql_name="startInterval", default=None)),
                ("end_interval", sgqlc.types.Arg(TimestampInterval, graphql_name="endInterval", default=None)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `periodic_type` (`PeriodicType`)None (default: `null`)
    * `status` (`JobStatus`)None (default: `null`)
    * `init_model_version` (`ObjectVersionInput`)None (default:
      `null`)
    * `dataset_loader_version` (`ObjectVersionInput`)None (default:
      `null`)
    * `executor_version` (`ObjectVersionInput`)None (default: `null`)
    * `start_interval` (`TimestampInterval`)None (default: `null`)
    * `end_interval` (`TimestampInterval`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    model_from_name = sgqlc.types.Field(
        sgqlc.types.non_null(Model),
        graphql_name="modelFromName",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    warning_delete_model_query = sgqlc.types.Field(
        sgqlc.types.non_null("WarningDeleteModel"),
        graphql_name="warningDeleteModelQuery",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    list_model = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Model))), graphql_name="listModel")

    pagination_model = sgqlc.types.Field(
        sgqlc.types.non_null(ModelPagination),
        graphql_name="paginationModel",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    model_version_from_run_id = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersion),
        graphql_name="modelVersionFromRunId",
        args=sgqlc.types.ArgDict((("run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="runId", default=None)),)),
    )
    """Arguments:

    * `run_id` (`String!`)None
    """

    model_version_from_name_version = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersion),
        graphql_name="modelVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (("model_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="modelVersion", default=None)),)
        ),
    )
    """Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    """

    list_initial_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelVersion))), graphql_name="listInitialModelVersion"
    )

    pagination_initial_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersionPagination),
        graphql_name="paginationInitialModelVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    list_dataset_loader = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoader))), graphql_name="listDatasetLoader"
    )

    pagination_dataset_loader = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderPagination),
        graphql_name="paginationDatasetLoader",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    dataset_loader_from_name = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoader),
        graphql_name="datasetLoaderFromName",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    dataset_loader_version_from_name_version = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderVersion),
        graphql_name="datasetLoaderVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dataset_loader_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="datasetLoaderVersion", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    """

    dataset_loader_version_from_run_id = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderVersion),
        graphql_name="datasetLoaderVersionFromRunId",
        args=sgqlc.types.ArgDict((("run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="runId", default=None)),)),
    )
    """Arguments:

    * `run_id` (`String!`)None
    """

    executor_from_name = sgqlc.types.Field(
        sgqlc.types.non_null(Executor),
        graphql_name="executorFromName",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    list_executor = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Executor))), graphql_name="listExecutor"
    )

    pagination_executor = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorPagination),
        graphql_name="paginationExecutor",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    executor_version_from_name_version = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersion),
        graphql_name="executorVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (("executor_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="executorVersion", default=None)),)
        ),
    )
    """Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    """

    executor_version_from_run_id = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersion),
        graphql_name="executorVersionFromRunId",
        args=sgqlc.types.ArgDict((("run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="runId", default=None)),)),
    )
    """Arguments:

    * `run_id` (`String!`)None
    """

    list_initial_executor_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutorVersion))), graphql_name="listInitialExecutorVersion"
    )


class Run(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        "run_id",
        "artifact_uri",
        "status",
        "latest_metrics",
        "experiment_id",
        "params",
        "start_time",
        "end_time",
        "lifecycle_stage",
        "parent_job",
        "list_artifacts",
        "experiment",
        "tags",
        "metric_history",
    )
    run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="runId")

    artifact_uri = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="artifactUri")

    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")

    latest_metrics = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="latestMetrics")

    experiment_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="experimentId")

    params = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="params")

    start_time = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="startTime")

    end_time = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="endTime")

    lifecycle_stage = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="lifecycleStage")

    parent_job = sgqlc.types.Field(Job, graphql_name="parentJob")

    list_artifacts = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name="listArtifacts"
    )

    experiment = sgqlc.types.Field(sgqlc.types.non_null(Experiment), graphql_name="experiment")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    metric_history = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Metric))),
        graphql_name="metricHistory",
        args=sgqlc.types.ArgDict((("metric", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="metric", default=None)),)),
    )
    """Arguments:

    * `metric` (`String!`)None
    """


class RunPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("list_run", "total")
    list_run = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Run))), graphql_name="listRun")

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class User(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class WarningDeleteModel(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ("delete_possible", "list_model_version")
    delete_possible = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="deletePossible")

    list_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelVersion))), graphql_name="listModelVersion"
    )


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = Mutation
schema.subscription_type = None
