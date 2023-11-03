import argparse
import base64
import datetime
import json
import logging
import os.path
import re
import signal
import sys
import time
from typing import List
from typing import Optional

import pendulum
import py4j.protocol
import pyspark
from google.protobuf.json_format import MessageToJson
from google.protobuf.timestamp_pb2 import Timestamp
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import concat
from pyspark.sql.functions import expr
from pyspark.sql.functions import from_json
from pyspark.sql.functions import lit
from pyspark.sql.functions import row_number
from pyspark.sql.functions import struct
from pyspark.sql.functions import to_json
from pyspark.sql.types import LongType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
from pyspark.sql.utils import AnalysisException
from pyspark.sql.window import Window


try:
    import boto3
    from botocore.errorfactory import ClientError
except ImportError as ex:
    print(f"Unable to import boto3 or botocore.errorfactory.ClientError: {ex}")
    # not available and unused in dataproc
    boto3 = None
    ClientError = None

from tecton_core import conf
from tecton_core import feature_view_utils
from tecton_core import specs
from tecton_core.fco_container import FcoContainer
from tecton_core.fco_container import create_fco_container
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.id_helper import IdHelper
from tecton_core.offline_store import get_offline_store_partition_params
from tecton_core.offline_store import get_offline_store_type
from tecton_core.query_consts import anchor_time
from tecton_core.time_utils import align_time_downwards
from tecton_core.time_utils import backfill_jobs_periods
from tecton_core.time_utils import convert_timestamp_for_version
from tecton_materialization.job_metadata import dynamodb_client
from tecton_materialization.job_metadata import get_job_exec
from tecton_materialization.job_metadata import update_job_exec
from tecton_proto.materialization.job_metadata_pb2 import JobMetadata
from tecton_proto.materialization.job_metadata_pb2 import JobMetadataTableType
from tecton_proto.materialization.job_metadata_pb2 import OfflineStoreType
from tecton_proto.materialization.job_metadata_pb2 import OnlineStoreType
from tecton_proto.materialization.params_pb2 import MaterializationTaskParams
from tecton_spark import feature_view_spark_utils
from tecton_spark import materialization_plan
from tecton_spark.data_observability import create_feature_metrics_collector
from tecton_spark.materialization_plan import MATERIALIZED_RAW_DATA_END_TIME
from tecton_spark.materialization_plan import MaterializationPlan
from tecton_spark.offline_store import DeltaMetadataWriter
from tecton_spark.offline_store import DeltaWriter
from tecton_spark.offline_store import OfflineStoreWriterParams
from tecton_spark.offline_store import get_offline_store_reader
from tecton_spark.offline_store import get_offline_store_writer
from tecton_spark.time_utils import convert_timestamp_to_epoch


# Partitions being written to S3 should be small to minimize number of parquet files.
COALESCE_FOR_SMALL_PARTITIONS = 1
DEFAULT_COALESCE_FOR_S3 = 10
# Partitions being written to OSW can be higher to better utilize available executors.
DEFAULT_COALESCE_FOR_OSW = 64
WRITTEN_BY_BATCH = "written_by_batch"
BATCH_STATUS_ENTRY = "update_status_only"
COLUMNS = "columns"
CANARY_ID_COLUMN = "canary_id"

EMR_CLUSTER_INFO_FILE = "job-flow.json"
EMR_CLUSTER_INFO_PATH = f"/mnt/var/lib/info/{EMR_CLUSTER_INFO_FILE}"

# This section of constants should be used purely for ensuring idempotence of spark jobs.
IDEMPOTENCE_KEY_ATTRIBUTE = "idempotence_key"
VALUE_ATTRIBUTE = "value"
TTL_ATTRIBUTE = "ttl"
LAST_UPDATED_ATTRIBUTE = "last_updated"
RUN_ID_PREFIX = "id:"

TTL_DURATION_SECONDS = int(datetime.timedelta(days=60).total_seconds())

logger = logging.getLogger(__name__)

SPARK_ONLINE_STORE_SINK = None


# TODO(Alex): Migrate checkpointing into JMT
# We use task as the idempotence key for checkpointing because we don't need to recompute the same tiles already processed within the same task.
# In a different task, they may correspond to a different store type, or be an overwrite, so we'd want to still process them.
# The run_id isn't required but could be useful for debugging.
def write_checkpoint(spark, materialization_task_params, anchor_time, run_id):
    dynamodb = dynamodb_client(materialization_task_params)
    table = materialization_task_params.spark_job_execution_table
    idempotence_key = materialization_task_params.materialization_task_id + "@" + str(anchor_time)
    now_seconds = int(time.time())
    statsd_client = get_statsd_client(spark)
    dynamodb.put_item(
        TableName=table,
        Item={
            IDEMPOTENCE_KEY_ATTRIBUTE: {"S": idempotence_key},
            VALUE_ATTRIBUTE: {"S": f"{RUN_ID_PREFIX}{run_id}"},
            TTL_ATTRIBUTE: {"N": str(now_seconds + TTL_DURATION_SECONDS)},
            LAST_UPDATED_ATTRIBUTE: {"N": str(now_seconds)},
        },
    )
    statsd_client.incr("materialization.checkpoint_write", 1)


def is_checkpoint_complete(spark, materialization_task_params, anchor_time):
    dynamodb = dynamodb_client(materialization_task_params)
    table = materialization_task_params.spark_job_execution_table
    idempotence_key = materialization_task_params.materialization_task_id + "@" + str(anchor_time)
    now_seconds = int(time.time())
    statsd_client = get_statsd_client(spark)
    try:
        dynamodb.put_item(
            TableName=table,
            Item={
                IDEMPOTENCE_KEY_ATTRIBUTE: {"S": idempotence_key},
                VALUE_ATTRIBUTE: {"S": ""},
                TTL_ATTRIBUTE: {"N": str(now_seconds + TTL_DURATION_SECONDS)},
                LAST_UPDATED_ATTRIBUTE: {"N": str(now_seconds)},
            },
            ConditionExpression=f"attribute_not_exists({IDEMPOTENCE_KEY_ATTRIBUTE}) OR #val = :val",
            ExpressionAttributeNames={"#val": VALUE_ATTRIBUTE},
            ExpressionAttributeValues={":val": {"S": ""}},
        )
        statsd_client.incr("materialization.checkpoint_check_incomplete", 1)
        return False
    except ClientError as e:
        # Condition failed means we've previously committed the checkpoint
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            statsd_client.incr("materialization.checkpoint_check_complete", 1)
            return True
        else:
            raise e


def _handle_stream_handoff(materialization_task_params):
    """
    If stream handoff is enabled, we need to wait for the previous job to finish before starting the next one.
    """

    def set_ready_state(job_metadata: JobMetadata) -> Optional[JobMetadata]:
        new_proto = JobMetadata()
        new_proto.CopyFrom(job_metadata)
        new_proto.spark_execution_info.stream_handoff_synchronization_info.new_cluster_started = True
        return new_proto

    if materialization_task_params.stream_task_info.stream_parameters.stream_handoff_config.enabled:
        start_time = time.time()
        update_job_exec(materialization_task_params, set_ready_state)
        logger.info("Using stream handoff; waiting for ready state...")
        job_metadata, _ = get_job_exec(materialization_task_params)
        while not job_metadata.spark_execution_info.stream_handoff_synchronization_info.stream_query_start_allowed:
            if time.time() - start_time > 3600.0:
                msg = "Timed out waiting for ready state"
                raise Exception(msg)
            time.sleep(1)
            job_metadata, _ = get_job_exec(materialization_task_params)
        logger.info("Ready state reached; starting streaming query")


def _check_spark_job_uniqueness(materialization_task_params, run_id, spark, step, skip_legacy_execution_table_check):
    if step not in (1, None):
        return
    if (
        not skip_legacy_execution_table_check
        and materialization_task_params.job_metadata_table_type != JobMetadataTableType.JOB_METADATA_TABLE_TYPE_GCS
    ):
        dynamodb = dynamodb_client(materialization_task_params)
        table = materialization_task_params.spark_job_execution_table
        idempotence_key = materialization_task_params.idempotence_key

        # TODO: remove once job_metadata_table is enabled everywhere
        statsd_client = get_statsd_client(spark)
        try:
            existing_record = dynamodb.get_item(
                TableName=table,
                Key={IDEMPOTENCE_KEY_ATTRIBUTE: {"S": idempotence_key}},
                ConsistentRead=True,
            ).get("Item", None)
            statsd_client.incr("materialization.dynamo_get_item_success", 1)
        except ClientError:
            existing_record = None
            statsd_client.incr("materialization.dynamo_get_item_errors", 1)

        try:
            now_seconds = int(time.time())
            dynamodb.put_item(
                TableName=table,
                Item={
                    IDEMPOTENCE_KEY_ATTRIBUTE: {"S": idempotence_key},
                    VALUE_ATTRIBUTE: {"S": f"{RUN_ID_PREFIX}{run_id}"},
                    TTL_ATTRIBUTE: {"N": str(now_seconds + TTL_DURATION_SECONDS)},
                    LAST_UPDATED_ATTRIBUTE: {"N": str(now_seconds)},
                },
                ConditionExpression=f"attribute_not_exists({IDEMPOTENCE_KEY_ATTRIBUTE})",
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                if existing_record:
                    logger.error(f"Existing Spark unique key record found: {existing_record}")
                else:
                    logger.error(f"Conditional check failed, but no record found for {idempotence_key}")
                msg = f"Value is already set for idempotence_key: {idempotence_key}"
                raise RuntimeError(msg) from e
            raise e

    # TODO: remove above code and remove jobidempotencemanager code once NEW_JOB_EXECUTION_TABLE migration is done
    # after all customers have dynamodb:GetItem permission
    def updater(job_metadata: JobMetadata) -> Optional[JobMetadata]:
        new_proto = JobMetadata()
        new_proto.CopyFrom(job_metadata)
        if new_proto.spark_execution_info.HasField("run_id"):
            attempt_id = IdHelper.to_string(materialization_task_params.attempt_id)
            msg = f"Value is already set for attempt_id: {attempt_id}: {new_proto.spark_execution_info.run_id}"
            raise RuntimeError(msg)
        elif new_proto.spark_execution_info.is_revoked:
            msg = "Job cancelled by orchestrator before lock acquired"
            raise RuntimeError(msg)
        new_proto.spark_execution_info.run_id = run_id
        return new_proto

    if materialization_task_params.HasField("job_metadata_table"):
        update_job_exec(materialization_task_params, updater)


def construct_anchor_times(
    fdw: FeatureDefinition, start_time: datetime.datetime, num_tiles: int, version: int
) -> List[int]:
    """Creates `num_tiles` consecutive anchor_times starting from `start_time`.

    :return: An increasing list of consecutive anchor times.
    """
    anchor_times = []
    for i in range(num_tiles):
        anchor_time = start_time + i * fdw.get_tile_interval
        anchor_time_val = convert_timestamp_to_epoch(anchor_time, version)
        anchor_times.append(anchor_time_val)

    return anchor_times


def construct_tile_end_times(
    fdw: FeatureDefinition, latest_tile_end_time: datetime.datetime, num_tiles: int, version: int
) -> List[int]:
    """Creates `num_tiles` consecutive tile_end_times where latest one ends at `latest_tile_end_time`.

    :return: An increasing list of consecutive tile end times.
    """
    tile_end_times = []
    for i in range(num_tiles):
        tile_end_time = latest_tile_end_time - i * fdw.batch_materialization_schedule
        time_val = convert_timestamp_to_epoch(tile_end_time, version)
        tile_end_times.append(time_val)

    tile_end_times.reverse()
    return tile_end_times


def wait_for_metric_scrape():
    # Sleep for 1 minute before closing to ensure metrics are collected by Chronosphere (30 second
    # scrape interval).
    sleep_time = 60  # 1 minute
    logger.info(f"Waiting {sleep_time}s for metrics to be scraped.")
    time.sleep(sleep_time)


def fco_container_from_task_params(materialization_task_params: MaterializationTaskParams) -> FcoContainer:
    return create_fco_container(
        list(materialization_task_params.virtual_data_sources) + list(materialization_task_params.transformations),
        deserialize_funcs_to_main=True,
    )


def dedupe_online_store_writes(
    fd: FeatureDefinition,
    df: DataFrame,
) -> DataFrame:
    # this mimics the conditional writes in the OnlineStoreWriter
    if fd.is_temporal:
        # we take the latest record for each entity for temporal FVs
        window = Window.partitionBy(fd.join_keys).orderBy(col(fd.time_key).desc())
        row_number_col = "__tecton_row_num"
        assert row_number_col not in df.columns
        df = df.withColumn(row_number_col, row_number().over(window))
        df = df.filter(col(row_number_col) == 1).drop(row_number_col)
        return df
    else:
        return df


def make_dynamodb_json_dataframe(
    spark: SparkSession, fd: FeatureDefinition, materialization_task_params: MaterializationTaskParams, df: DataFrame
) -> DataFrame:
    df = _df_to_online_store_msg(df, fd.id, is_batch=True, is_status=False, canary_id=None)
    udf_name = f"to_dynamodb_json_{fd.id}"
    spark._jvm.com.tecton.onlinestorewriter.RegisterFeatureToDynamoDbJsonUDF().register(
        udf_name, materialization_task_params.SerializeToString()
    )
    return df.select(expr(f"{udf_name}(value)"))


def write_dynamodb_json(
    spark: SparkSession, fd: FeatureDefinition, materialization_task_params: MaterializationTaskParams, df: DataFrame
) -> int:
    dynamodb_json_df = make_dynamodb_json_dataframe(spark, fd, materialization_task_params, df)
    output_path = materialization_task_params.batch_task_info.dynamodb_json_output_path
    # we shuffle the rows randomly to avoid hot partitions (as recommended by AWS for dynamodb:importtable)
    # 128 is a magic number that should work well for large files but not too much overhead for small files; but it
    # is merely theoretical, feel free to change
    dynamodb_json_df.orderBy(expr("rand()")).repartition(128).write.format("text").option("compression", "gzip").option(
        "sep", "\n"
    ).mode("overwrite").save(output_path)
    return dynamodb_json_df.count()


def make_batch_status_dataframe(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    fd: FeatureDefinition,
    feature_start_time: datetime.datetime,
    feature_end_time: datetime.datetime,
) -> DataFrame:
    # For continuous aggregation when writing uncompacted data we will default to writing
    # tile end times
    version = fd.get_feature_store_format_version
    batch_params = materialization_task_params.batch_task_info.batch_parameters
    if fd.is_temporal_aggregate and not fd.is_continuous:
        # For BWAFVs, write all materialized anchor times in the status table
        anchor_times = construct_anchor_times(fd, feature_start_time, batch_params.tile_count, version)
        anchor_times_df_format = [[x] for x in anchor_times]
        schema = StructType([StructField(anchor_time(), LongType())])
        return spark.createDataFrame(anchor_times_df_format, schema=schema)
    else:
        # For BFVs, write materialized tile end times in the status table
        tile_end_times = construct_tile_end_times(fd, feature_end_time, batch_params.tile_count, version)
        tile_end_times_df_format = [[x] for x in tile_end_times]
        schema = StructType([StructField(MATERIALIZED_RAW_DATA_END_TIME, LongType())])
        return spark.createDataFrame(tile_end_times_df_format, schema=schema)


def write_batch_to_hdfs(plan: MaterializationPlan, hdfs_output_path: str):
    plan.base_data_frame.write.parquet(hdfs_output_path)


def materialize_batch_to_offline(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    feature_start_time: datetime.datetime,
    feature_end_time: datetime.datetime,
    plan: MaterializationPlan,
):
    fco_container = fco_container_from_task_params(materialization_task_params)
    fv_spec = specs.create_feature_view_spec_from_data_proto(materialization_task_params.feature_view)
    fd = FeatureDefinition(fv_spec, fco_container)
    version = fd.get_feature_store_format_version
    coalesce = (
        COALESCE_FOR_SMALL_PARTITIONS
        if get_offline_store_partition_params(fd).partition_interval.as_timedelta() <= datetime.timedelta(hours=1)
        else DEFAULT_COALESCE_FOR_S3
    )
    should_avoid_coalesce = (
        get_offline_store_type(fd) == "delta"
        and spark.conf.get("spark.databricks.delta.optimizeWrite.enabled", None) == "true"
    )
    offline_store_df = (
        plan.offline_store_data_frame if should_avoid_coalesce else plan.offline_store_data_frame.coalesce(coalesce)
    )

    if fd.is_temporal_aggregate:
        time_column = anchor_time()
    else:
        time_column = fd.time_key

    offline_store_params = OfflineStoreWriterParams(
        s3_path=materialization_task_params.offline_store_path,
        always_store_anchor_column=True,
        time_column=time_column,
        join_key_columns=fd.join_keys,
        is_continuous=fd.is_continuous,
    )

    # We need to first clean up the time range if doing a manual retry of a successful past job
    start_time_proto = Timestamp()
    start_time_proto.FromDatetime(feature_start_time)
    if _has_prior_delta_commit(spark, materialization_task_params, start_time_proto.ToJsonString()):
        store_writer = get_offline_store_writer(offline_store_params, fd, version, spark)

        start = time.time()

        logger.info(f"Cleaning up old writes to offline store for FV {fd.id}")
        store_writer.delete_time_range(
            feature_start_time,
            feature_end_time,
        )

        latency = time.time() - start
        logger.info(f"Finished cleanup of offline store for FV {fd.id} ({latency}s)")

    store_writer = get_offline_store_writer(offline_store_params, fd, version, spark)

    start = time.time()

    logger.info(f"Writing to offline store for FV {fd.id} for interval {feature_start_time} to {feature_end_time}")
    store_writer.append_dataframe(offline_store_df)
    store_reader = get_offline_store_reader(spark, fd, path=materialization_task_params.offline_store_path)
    unhandled_analysis_exception = False
    try:
        start_time_col = convert_timestamp_for_version(feature_start_time, version)
        end_time_col = convert_timestamp_for_version(feature_end_time, version)
        # We need to subtract 1 microsecond from the end time to ensure that we don't
        # read the next tile
        offline_store_count = (
            store_reader.read(
                pendulum.period(feature_start_time, feature_end_time - datetime.timedelta(microseconds=1))
            )
            .filter((col(anchor_time()) >= lit(start_time_col)) & (col(anchor_time()) < lit(end_time_col)))
            .count()
        )
    except AnalysisException as e:
        is_df_empty = len(offline_store_df.take(1)) == 0
        if not is_df_empty:
            unhandled_analysis_exception = True
            logger.info(f"Unhandled AnalysisException checking Dataframe size: {e}")
        offline_store_count = 0
    export_consumption_debug_metrics(spark, offline_store_count, plan.cached_count(), unhandled_analysis_exception)

    latency = time.time() - start
    logger.info(f"Finished writing to offline store ({latency}s)")

    export_consumption_metrics(spark, fd, plan.cached_count(), materialization_task_params, store_type="offline")


def materialize_batch_to_online(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    feature_start_time: datetime.datetime,
    feature_end_time: datetime.datetime,
    plan: MaterializationPlan,
    resources,
):
    batch_task_info = materialization_task_params.batch_task_info
    batch_params = batch_task_info.batch_parameters
    fco_container = fco_container_from_task_params(materialization_task_params)
    fv_spec = specs.create_feature_view_spec_from_data_proto(materialization_task_params.feature_view)
    fd = FeatureDefinition(fv_spec, fco_container)
    online_store_df = plan.online_store_data_frame
    start = time.time()

    logger.info(f"Writing to online store for FV {fd.id} for interval {feature_start_time} to {feature_end_time}")
    if batch_task_info.should_dedupe_online_store_writes:
        online_store_df = dedupe_online_store_writes(fd, online_store_df)

    if batch_params.create_online_table:
        # note that it's okay to write the status table entries here ahead of time, because it won't be
        # marked as servable until the import table is complete
        # additionally, the status table range never shrinks, so even if we retry, it will be okay
        dynamo_import_row_count = write_dynamodb_json(spark, fd, materialization_task_params, online_store_df)
        # we export consumption metrics here for dynamo import instead of OSW because we don't use OSW
        export_consumption_metrics(
            spark,
            fd,
            dynamo_import_row_count,
            materialization_task_params,
            store_type="online",
            online_store_type=OnlineStoreType.ONLINE_STORE_TYPE_DYNAMO,
        )
    else:
        # Write materialized features to the online feature store
        online_store_df = online_store_df.coalesce(DEFAULT_COALESCE_FOR_OSW)
        _batch_write_to_online_store(
            online_store_df, materialization_task_params, resources.get_online_store_sink(), fd.id, is_status=False
        )

    status_df = make_batch_status_dataframe(
        spark, materialization_task_params, fd, feature_start_time, feature_end_time
    )

    _batch_write_to_online_store(
        status_df, materialization_task_params, resources.get_online_store_sink(), fd.id, is_status=True
    )
    latency = time.time() - start
    logger.info(f"Finished writing to online store ({latency}s)")


def export_consumption_metrics(
    spark: SparkSession,
    fd: FeatureDefinition,
    row_count,
    params: MaterializationTaskParams,
    store_type,
    online_store_type: OnlineStoreType = None,
):
    assert store_type in ("offline", "online")
    # we only use this for dynamo now. no easy way to get the online_store_type
    assert store_type != "online" or online_store_type == OnlineStoreType.ONLINE_STORE_TYPE_DYNAMO
    # Don't want to call fd.features, since in the
    # temporal aggregate case it will return a feature for each time window,
    # which is not how the data is actually materialized.
    materialized_feature_columns = get_materialized_feature_columns(fd)

    num_rows = row_count
    num_values = num_rows * len(materialized_feature_columns)

    statsd_client = get_statsd_client(spark)

    statsd_safe_fd_name = fd.name.replace(":", "__")
    statsd_safe_workspace = fd.workspace.replace(":", "__")
    statsd_client.incr(
        f"tecton-{store_type}-store.cm_feature_write_rows.{statsd_safe_workspace}.{statsd_safe_fd_name}.", num_rows
    )
    statsd_client.incr(
        f"tecton-{store_type}-store.cm_feature_write_values.{statsd_safe_workspace}.{statsd_safe_fd_name}", num_values
    )

    def updater(job_metadata: JobMetadata) -> Optional[JobMetadata]:
        new_proto = JobMetadata()
        new_proto.CopyFrom(job_metadata)
        aligned_bucket_start = int(
            align_time_downwards(datetime.datetime.now(), datetime.timedelta(hours=1)).timestamp()
        )
        if store_type == "offline":
            offline = new_proto.materialization_consumption_info.offline_store_consumption
            bucket = offline.consumption_info[aligned_bucket_start]

            if params.offline_store_path.startswith("s3"):
                offline.offline_store_type = OfflineStoreType.OFFLINE_STORE_TYPE_S3
            elif params.offline_store_path.startswith("dbfs"):
                offline.offline_store_type = OfflineStoreType.OFFLINE_STORE_TYPE_DBFS
            elif params.offline_store_path.startswith("gs"):
                offline.offline_store_type = OfflineStoreType.OFFLINE_STORE_TYPE_GCS
            else:
                msg = f"Unknown offline store type path: {offline.offline_store_type}"
                raise Exception(msg)
        elif store_type == "online":
            online = new_proto.materialization_consumption_info.online_store_consumption
            bucket = online.consumption_info[aligned_bucket_start]

            online.online_store_type = online_store_type
        else:
            exc_msg = f"Unknown store type: {store_type}"
            raise Exception(exc_msg)

        bucket.rows_written += num_rows
        bucket.features_written += num_values

        return new_proto

    if params.HasField("job_metadata_table") and params.use_new_consumption_metrics:
        update_job_exec(params, updater)

    logger.info(f"Exported {store_type} consumption metrics")


def get_materialized_feature_columns(fd: FeatureDefinition):
    return feature_view_utils.get_input_feature_columns(
        fd.view_schema.to_proto(),
        fd.join_keys,
        fd.timestamp_key,
    )


def run_delta_maintenance(spark: SparkSession, materialization_task_params: MaterializationTaskParams):
    path = materialization_task_params.offline_store_path
    delta_metadata_writer = DeltaMetadataWriter(spark)
    delta_maintenance_params = materialization_task_params.delta_maintenance_task_info.delta_maintenance_parameters
    if delta_maintenance_params.generate_manifest:
        # regardless, the manual run is necessary because the auto generation
        # is not safe to race conditions. see https://docs.delta.io/latest/presto-integration.html#language-python
        delta_metadata_writer.generate_symlink_manifest(path)
    if delta_maintenance_params.execute_compaction:
        delta_metadata_writer.optimize_execute_compaction(path)
    if delta_maintenance_params.vacuum:
        delta_metadata_writer.vacuum(path)


def run_online_store_deleter(spark: SparkSession, materialization_task_params: MaterializationTaskParams):
    start = time.time()
    report = spark._jvm.com.tecton.onlinestorewriter.deleter.OnlineStoreDeleter.fromMaterializationTaskParams(
        materialization_task_params.SerializeToString()
    ).run()
    latency = time.time() - start

    if materialization_task_params.HasField("online_store_writer_config"):
        store_type = materialization_task_params.online_store_writer_config.online_store_params.WhichOneof("store_type")
    else:
        store_type = "dynamo"

    export_deletion_metrics(
        spark,
        store_type,
        metric_source="tecton-online-store-deleter",
        requested_num_keys=report.getRequestedNumKeys(),
        deleted_num_keys=report.getDeletedNumKeys(),
        latency=latency,
    )

    if report.getError():
        msg = f"Deletion was interrupted due to the error received from storage: {report.getError()}"
        raise RuntimeError(msg)


def export_deletion_metrics(
    spark: SparkSession,
    store_type: str,
    metric_source: str,
    requested_num_keys: int,
    deleted_num_keys: int,
    latency: Optional[float] = None,
):
    statsd_client = get_statsd_client(spark)

    statsd_client.incr(f"{metric_source}.{store_type}.num_keys_deletion_requested", requested_num_keys)
    statsd_client.incr(f"{metric_source}.{store_type}.num_keys_deletion_success", deleted_num_keys)

    if latency:
        # timing expects number of milliseconds
        statsd_client.timing(f"{metric_source}.{store_type}.deletion_latency", latency * 1000)


def export_consumption_debug_metrics(
    spark: SparkSession,
    offline_store_count: int,
    dataframe_count: int,
    unhandled_analysis_exception: bool,
):
    statsd_client = get_statsd_client(spark)

    if unhandled_analysis_exception:
        statsd_client.incr("consumption.unhandled_analysis_exception")
    elif offline_store_count != dataframe_count:
        statsd_client.incr("consumption.diff_rows_count", offline_store_count - dataframe_count)
    else:
        statsd_client.incr("consumption.same_rows")


def run_offline_store_deleter(spark: SparkSession, materialization_task_params: MaterializationTaskParams):
    deletion_params = materialization_task_params.deletion_task_info.deletion_parameters
    spark.conf.set(
        "spark.databricks.delta.commitInfo.userMetadata",
        f'{{"deletionPath":"{deletion_params.offline_join_keys_path}"}}',
    )
    fco_container = fco_container_from_task_params(materialization_task_params)
    fv_spec = specs.create_feature_view_spec_from_data_proto(materialization_task_params.feature_view)
    fd = FeatureDefinition(fv_spec, fco_container)
    if fd.is_temporal_aggregate:
        time_column = anchor_time()
    else:
        time_column = fd.time_key
    offline_store_params = OfflineStoreWriterParams(
        s3_path=materialization_task_params.offline_store_path,
        always_store_anchor_column=False,
        time_column=time_column,
        join_key_columns=fd.join_keys,
        is_continuous=False,
    )
    store_writer = get_offline_store_writer(offline_store_params, fd, fd.get_feature_store_format_version, spark)
    keys = spark.read.parquet(deletion_params.offline_join_keys_path)
    keys = keys.distinct()
    requested_num_keys = keys.count()
    start = time.time()
    deleted_num_keys = store_writer.delete_keys(keys)
    latency = time.time() - start

    store_type = fd.offline_store_config.WhichOneof("store_type") if fd.offline_store_config else None
    store_type = store_type or "delta"

    export_deletion_metrics(
        spark,
        store_type=store_type,
        metric_source="tecton-offline-store-deleter",
        requested_num_keys=requested_num_keys,
        deleted_num_keys=deleted_num_keys,
        latency=latency,
    )


def ingest_pushed_df(spark: SparkSession, raw_df: DataFrame, materialization_task_params: MaterializationTaskParams):
    ingest_task_info = materialization_task_params.ingest_task_info
    ingest_path = ingest_task_info.ingest_parameters.ingest_path
    spark.conf.set(
        "spark.databricks.delta.commitInfo.userMetadata",
        f'{{"ingestPath":"{ingest_path}"}}',
    )
    fco_container = fco_container_from_task_params(materialization_task_params)
    fv_spec = specs.create_feature_view_spec_from_data_proto(materialization_task_params.feature_view)
    fd = FeatureDefinition(fv_spec, fco_container)

    feature_view_spark_utils.validate_df_columns_and_feature_types(raw_df, fd.view_schema)

    # Drop extra columns
    df = raw_df.select(*fd.view_schema.column_names())

    timestamp_key = fd.timestamp_key
    assert timestamp_key is not None
    version = fd.get_feature_store_format_version

    if ingest_task_info.ingest_parameters.write_to_online_feature_store:
        logger.info(f"Ingesting to the OnlineStore FT: {fd.id}")
        # Find the last timestamp
        raw_data_end_time_ts = df.agg({timestamp_key: "max"}).collect()[0][0]
        raw_data_end_time_epoch = convert_timestamp_to_epoch(raw_data_end_time_ts, version)

        online_df = df.withColumn(MATERIALIZED_RAW_DATA_END_TIME, lit(raw_data_end_time_epoch))

        sink = _set_up_online_store_sink(spark, materialization_task_params)
        metrics_collector = create_feature_metrics_collector(spark, materialization_task_params)

        # collect metrics
        online_df = metrics_collector.observe(online_df)

        # TODO: For large DFs consider splitting into "chunks" to load balance across partitions and FSW instances
        _batch_write_to_online_store(online_df, materialization_task_params, sink, fd.id, is_status=False)

        # Status table
        status_df = [[raw_data_end_time_epoch]]
        schema = StructType([StructField(MATERIALIZED_RAW_DATA_END_TIME, LongType())])
        status_df = spark.createDataFrame(status_df, schema=schema)
        _batch_write_to_online_store(status_df, materialization_task_params, sink, fd.id, is_status=True)
        if sink is not None:
            # Temporarily wrap closeGlobalResources() for ingest since this
            # runs in the internal cluster. This is because we may run this
            # code before the new OSW jar is installed on the internal cluster.
            # This isn't a problem for other types of materialization since
            # they use short-lived clusters that use materialization library
            # and OSW from the same release.
            #
            # TODO(brian): remove try/except after all validation clusters are
            # restarted.
            try:
                sink.closeGlobalResources()
            except py4j.protocol.Py4JError:
                pass

        # publish metrics
        try:
            metrics_collector.publish()
        except Exception as e:
            logger.error(f"Metrics publishing failed: {e}")

    # skip delta write if we detect a prior job has successfully committed the data already
    if ingest_task_info.ingest_parameters.write_to_offline_feature_store and not _has_prior_delta_commit(
        spark, materialization_task_params, ingest_path
    ):
        logger.info(f"Ingesting to the OfflineStore FT: {fd.id}")
        offline_store_params = OfflineStoreWriterParams(
            s3_path=materialization_task_params.offline_store_path,
            always_store_anchor_column=False,
            time_column=timestamp_key,
            join_key_columns=fd.join_keys,
            is_continuous=False,
        )
        offline_store_config = fd.offline_store_config
        assert offline_store_config.HasField("delta"), "FeatureTables do not support Parquet-based Offline storage"
        store_writer = get_offline_store_writer(offline_store_params, fd, version, spark)
        store_writer.upsert_dataframe(df)

    wait_for_metric_scrape()


# TODO (TEC-17019): fix edge case bug where offline jobs can have different start-end ranges so this can
# return false when in fact there is data materialized for that range
# for ingest, use ingest_path as idempotence key, and for batch materialization, use feature start time
def _has_prior_delta_commit(spark, materialization_params, idempotence_key):
    assert materialization_params.HasField("offline_store_path")
    if not materialization_params.feature_view.materialization_params.offline_store_config.HasField("delta"):
        return False
    from delta.tables import DeltaTable

    try:
        delta_table = DeltaTable.forPath(spark, materialization_params.offline_store_path)
    except AnalysisException as e:
        # no prior commits if table doesn't exist yet
        return False
    metadata_schema = StructType().add("featureStartTime", StringType())
    commit_count = (
        delta_table.history()
        .select(from_json("userMetadata", metadata_schema).alias("metadataJson"))
        .filter(f"metadataJson.featureStartTime = '{idempotence_key}'")
        .count()
    )
    return commit_count != 0


def _set_up_online_store_sink(spark: SparkSession, materialization_task_params: MaterializationTaskParams):
    sink = spark._jvm.com.tecton.onlinestorewriter.SparkOnlineStoreSinkFactory.fromMaterializationTaskParams(
        materialization_task_params.SerializeToString()
    )
    signal.signal(signal.SIGINT, lambda signum, frame: sink.closeGlobalResources())
    signal.signal(signal.SIGTERM, lambda signum, frame: sink.closeGlobalResources())
    return sink


def _batch_write_to_online_store(
    dataframe,
    materialization_task_params: MaterializationTaskParams,
    sink,
    fv_id: str,
    is_status: bool,
):
    start = time.time()
    canary_id = materialization_task_params.canary_id if materialization_task_params.HasField("canary_id") else None
    write_df = _df_to_online_store_msg(dataframe, fv_id, is_batch=True, is_status=is_status, canary_id=canary_id)

    logger.info(f"Starting batch write to Tecton Online Store for the FV '{fv_id}'")
    write_df._jdf.foreachPartition(sink)

    latency = time.time() - start
    logger.info(f"Finished batch write for the FV '{fv_id}' ({latency}s)")


def _df_to_online_store_msg(
    dataframe, feature_view_id_str: str, is_batch: bool, is_status: bool, canary_id: Optional[str] = None
):
    """Produces a dataframe to be written to the online store.

    The dataframe will have two columns: 'key' and 'value'. The 'key' column will look like:

    feature_view_id_str # for SFVs and SWAFVs
    or
    feature_view_id_str + "|" + _anchor_time # for BWAFVs
    or
    feature_view_id_str + "|" + _materialized_raw_data_end_time # for batch BFVs

    In order to construct these keys, the input dataframe must have a column named `_anchor_time` for BWAFVs or a column
    named `_materialized_raw_data_end_time` for BFVs. It does not need to have either for SFVs or SWAFVs.

    For BWAFVs, the 'value' column will look like:
        value = {WRITTEN_BY_BATCH: true, "_anchor_time": 196000, COLUMNS: {"num_users": 1, ...}} # `is_status` is False
        or
        value = {BATCH_STATUS_ENTRY: true, WRITTEN_BY_BATCH: true, "_anchor_time": 196000} # `is_status` is True
    For BFVs, the 'value' column will look like:
        value = {WRITTEN_BY_BATCH: true, "_materialized_raw_data_end_time": 196000, COLUMNS: {"num_users": 1, ...}} # `is_status` is False
        or
        value = {BATCH_STATUS_ENTRY: true, WRITTEN_BY_BATCH: true, "_materialized_raw_data_end_time": 196000} # `is_status` is True
    For SFVs and SWAFVs, the 'value' column will look like:
        value = {COLUMNS: {"num_users": 1, ...}} # `is_status` must be False when `is_batch` is False
    """
    # only batch sends data and status separately
    assert not is_status or is_batch

    # add additional columns if needed; wrap original columns except anchor time in COLUMNS struct
    payload_schema = dataframe.schema.fieldNames()

    # Only used when `is_batch` is True.
    is_temporal_aggregate = False

    if anchor_time() in payload_schema:
        is_temporal_aggregate = True
        payload_schema.remove(anchor_time())
    elif is_batch:
        payload_schema.remove(MATERIALIZED_RAW_DATA_END_TIME)

    if is_status:
        dataframe = dataframe.withColumn(BATCH_STATUS_ENTRY, lit(True))
    else:
        dataframe = dataframe.withColumn(COLUMNS, struct(payload_schema))
    if is_batch:
        dataframe = dataframe.withColumn(WRITTEN_BY_BATCH, lit(True))
    if canary_id:
        dataframe = dataframe.withColumn(CANARY_ID_COLUMN, lit(canary_id))

    # Remove original columns (except anchor_time or materialized_raw_data_end_time) from
    # a top-level dataframe
    for col_name in payload_schema:
        dataframe = dataframe.drop(col_name)

    # wrap all columns in json object as `value`
    row_schema = dataframe.schema.fieldNames()
    key = lit(feature_view_id_str)
    if is_batch:
        if is_temporal_aggregate:
            key = concat(key, lit("|"), anchor_time())
        else:
            key = concat(key, lit("|"), MATERIALIZED_RAW_DATA_END_TIME)

    dataframe = dataframe.select(key.alias("key"), to_json(struct(row_schema)).alias("value"))
    if is_batch and is_status and not is_temporal_aggregate:
        logger.info(f"Writing status table update for BFV: {feature_view_id_str}")

    return dataframe


def _start_stream_job_with_online_store_sink(
    spark: SparkSession, dataframe, materialization_task_params, sink
) -> "pyspark.sql.streaming.StreamingQuery":
    canary_id = materialization_task_params.canary_id if materialization_task_params.HasField("canary_id") else None
    # TODO(amargvela): For SFV add feature timestamp as MATERIALIZED_RAW_DATA_END_TIME column.
    fco_container = fco_container_from_task_params(materialization_task_params)
    fv_spec = specs.create_feature_view_spec_from_data_proto(materialization_task_params.feature_view)
    fd = FeatureDefinition(fv_spec, fco_container)

    stream_task_info = materialization_task_params.stream_task_info

    if stream_task_info.HasField("streaming_trigger_interval_override"):
        processing_time = stream_task_info.streaming_trigger_interval_override
    elif fd.is_continuous:
        processing_time = "0 seconds"
    else:
        processing_time = "30 seconds"

    write_df = _df_to_online_store_msg(dataframe, fd.id, is_batch=False, is_status=False, canary_id=canary_id)

    logger.info(f"Starting stream write to Tecton Online Store for FV {fd.id}")
    trigger = spark._jvm.org.apache.spark.sql.streaming.Trigger.ProcessingTime(processing_time)
    writer = (
        write_df._jdf.writeStream()
        .queryName("tecton_osw_sink")
        .foreach(sink)
        .option(
            "checkpointLocation", f"{stream_task_info.streaming_checkpoint_path}-k"
        )  # append -k to differentiate from Dynamo checkpoint path; keep this in sync with the Canary process.
        .outputMode("update")
        .trigger(trigger)
    )
    return writer.start()


def start_stream_materialization(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    sink,
) -> "pyspark.sql.streaming.StreamingQuery":
    logger.info(
        f"Starting materialization task {materialization_task_params.materialization_task_id} for feature view {IdHelper.to_string(materialization_task_params.feature_view.feature_view_id)}"
    )

    fco_container = fco_container_from_task_params(materialization_task_params)
    fv_spec = specs.create_feature_view_spec_from_data_proto(materialization_task_params.feature_view)
    fd = FeatureDefinition(fv_spec, fco_container)

    plan = materialization_plan.get_stream_materialization_plan(
        spark=spark,
        feature_definition=fd,
    )
    spark_df = plan.online_store_data_frame

    _handle_stream_handoff(materialization_task_params)

    online_store_query = _start_stream_job_with_online_store_sink(spark, spark_df, materialization_task_params, sink)

    return online_store_query


def _deserialize_materialization_task_params(serialized_materialization_task_params) -> MaterializationTaskParams:
    params = MaterializationTaskParams()
    params.ParseFromString(base64.standard_b64decode(serialized_materialization_task_params))
    return params


def watch_stream_query(
    materialization_task_params: MaterializationTaskParams, stream_query: "pyspark.sql.streaming.StreamingQuery"
):
    def set_terminated_state(job_metadata: JobMetadata) -> Optional[JobMetadata]:
        new_proto = JobMetadata()
        new_proto.CopyFrom(job_metadata)
        new_proto.spark_execution_info.stream_handoff_synchronization_info.query_cancellation_complete = True
        return new_proto

    stream_params = materialization_task_params.stream_task_info.stream_parameters
    if stream_params.stream_handoff_config.enabled:
        while stream_query.isActive():
            job_metadata, _ = get_job_exec(materialization_task_params)
            # check if the materialization task has been cancelled
            if job_metadata.spark_execution_info.stream_handoff_synchronization_info.query_cancellation_requested:
                logger.info("Stream query cancellation requested. Stopping stream query.")
                try:
                    stream_query.stop()
                    stream_query.awaitTermination()
                finally:
                    logger.info("Query cancellation complete")
                    update_job_exec(materialization_task_params, set_terminated_state)
                return
            time.sleep(60)
        # returns immediately or throws exception, given that isActive() is false
        stream_query.awaitTermination()
    else:
        stream_query.awaitTermination()


def stream_materialize_from_params(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
):
    sink = _set_up_online_store_sink(spark, materialization_task_params)
    online_store_sink = start_stream_materialization(spark, materialization_task_params, sink)

    should_publish_stream_metrics = spark.conf.get("spark.tecton.publish_stream_metrics", "true") == "true"

    if should_publish_stream_metrics:
        metricsReportingListener = spark._jvm.com.tecton.onlinestorewriter.MetricsReportingListener(
            materialization_task_params.SerializeToString()
        )
        spark.streams._jsqm.addListener(metricsReportingListener)

    watch_stream_query(materialization_task_params, online_store_sink)
    if sink is not None:
        sink.closeGlobalResources()


class MaterializationResourceContainer:
    def __init__(self, spark: SparkSession, materialization_task_params: MaterializationTaskParams):
        self.spark = spark
        self.materialization_task_params = materialization_task_params
        self.online_store_sink = None
        self.materialization_plan = {}

    def get_online_store_sink(self):
        if self.online_store_sink is None:
            self.online_store_sink = _set_up_online_store_sink(self.spark, self.materialization_task_params)
        return self.online_store_sink

    def close(self):
        if self.online_store_sink is not None:
            self.online_store_sink.closeGlobalResources()


def get_hdfs_path(materialization_task_params: MaterializationTaskParams, end_time):
    hdfs_path_base = f"transformed_data_{IdHelper.to_string(materialization_task_params.attempt_id)}"
    formatted_time = end_time.strftime("%Y_%m_%d_%H_%M_%S")
    return f"{hdfs_path_base}_{formatted_time}"


def split_job_into_queries(fd: FeatureDefinition, start_time, end_time):
    # for incremental backfills, we split the job into each batch interval
    if fd.is_incremental_backfill:
        return backfill_jobs_periods(start_time, end_time, fd.batch_materialization_schedule)
    else:
        return [(start_time, end_time)]


def batch_materialize_from_params(
    spark: SparkSession,
    materialization_task_params: MaterializationTaskParams,
    run_id,
    step=None,
):
    batch_params = materialization_task_params.batch_task_info.batch_parameters
    resources = MaterializationResourceContainer(spark, materialization_task_params)
    spark.conf.set(
        "spark.databricks.delta.commitInfo.userMetadata",
        f'{{"featureStartTime":"{batch_params.feature_start_time.ToJsonString()}"}}',
    )
    fco_container = fco_container_from_task_params(materialization_task_params)
    fv_spec = specs.create_feature_view_spec_from_data_proto(materialization_task_params.feature_view)
    fd = FeatureDefinition(fv_spec, fco_container)
    task_feature_start_time = batch_params.feature_start_time.ToDatetime()
    task_feature_end_time = batch_params.feature_end_time.ToDatetime()

    # we only use checkpoints in steps that write to actual stores and have multiple intervals to write
    use_checkpoints = step != 1 and not materialization_task_params.HasField("canary_id") and fd.is_incremental_backfill

    write_to_offline_store_from_source = batch_params.write_to_offline_feature_store
    # if we are reading from the offline store, we don't need to split up the query, like we do from source
    # we actually don't want to, because dynamo json will not support this
    write_to_online_from_source = (
        batch_params.write_to_online_feature_store and not batch_params.read_from_offline_store_for_online_write
    )
    write_to_online_from_offline_store = (
        batch_params.write_to_online_feature_store and batch_params.read_from_offline_store_for_online_write
    )

    reads_data_from_source = write_to_offline_store_from_source or write_to_online_from_source
    if step == 1 and not reads_data_from_source:
        # we only need step 1 if we are reading data from source (which executes transformations)
        logger.info("Skipping step 1 since no data is read from source")
        return

    total_rows = 0

    if write_to_offline_store_from_source or write_to_online_from_source:
        # when reading from source, we must split the queries up into intervals based on incremental_backfills
        # note that we don't need to do this for 2 step materialization, but we keep it here to preserve old behavior
        # and not break existing customer jobs
        for query_feature_start_time, query_feature_end_time in split_job_into_queries(
            fd, task_feature_start_time, task_feature_end_time
        ):
            if use_checkpoints and is_checkpoint_complete(spark, materialization_task_params, query_feature_start_time):
                logger.info(
                    "Checkpoint complete for interval %s to %s; skipping",
                    query_feature_start_time,
                    query_feature_end_time,
                )
                continue
            query_feature_time_limits = pendulum.instance(query_feature_end_time) - pendulum.instance(
                query_feature_start_time
            )
            if step in (1, None):
                metrics_collector = create_feature_metrics_collector(
                    spark,
                    materialization_task_params,
                    feature_start_time=query_feature_start_time,
                    feature_end_time=query_feature_end_time,
                )
                plan = materialization_plan.get_batch_materialization_plan(
                    spark=spark,
                    feature_definition=fd,
                    feature_data_time_limits=query_feature_time_limits,
                    metrics_collector=metrics_collector,
                )
                # we must cache here so metrics_collector does not double-count rows. However, this is not reliable
                # as the cache is subject to eviction
                # TODO(dataobs): fix this
                plan.base_data_frame.cache()
            else:
                assert step == 2
                # we don't collect metrics in step 2, since they are already collected in step 1
                metrics_collector = None
                # for step 2, we read from the transformed data written in step 1
                plan = MaterializationPlan.from_parquet(
                    spark=spark, fd=fd, path=get_hdfs_path(materialization_task_params, query_feature_end_time)
                )
            if step == 1:
                # for step 1, we write the transformed data to hdfs, to be read in step 2
                write_batch_to_hdfs(plan, get_hdfs_path(materialization_task_params, query_feature_end_time))
            else:
                if write_to_offline_store_from_source:
                    materialize_batch_to_offline(
                        spark, materialization_task_params, query_feature_start_time, query_feature_end_time, plan
                    )
                if write_to_online_from_source:
                    materialize_batch_to_online(
                        spark,
                        materialization_task_params,
                        query_feature_start_time,
                        query_feature_end_time,
                        plan,
                        resources,
                    )
            if metrics_collector:
                try:
                    metrics_collector.publish()
                except Exception as e:
                    logger.error(f"Metrics publishing failed: {e}")
            if step in (None, 2):
                logger.info(
                    f"Wrote {plan.cached_count()} rows for interval {query_feature_start_time} to {query_feature_end_time}"
                )
                total_rows += plan.cached_count()
            if use_checkpoints:
                write_checkpoint(spark, materialization_task_params, query_feature_start_time, run_id)

    logger.info(f"Wrote {total_rows} total rows")

    if write_to_online_from_offline_store:
        assert not materialization_task_params.HasField("canary_id")
        # we don't do metrics collection here, because they already got collected in the jobs writing to the offline store
        plan = MaterializationPlan.from_offline_store(fd, task_feature_start_time, task_feature_end_time, spark)
        materialize_batch_to_online(
            spark, materialization_task_params, task_feature_start_time, task_feature_end_time, plan, resources
        )

    wait_for_metric_scrape()
    resources.close()


def feature_export_from_params(spark: SparkSession, task_params: MaterializationTaskParams):
    export_params = task_params.feature_export_info.feature_export_parameters
    start_time = export_params.feature_start_time.ToDatetime()
    end_time = export_params.feature_end_time.ToDatetime()
    feature_view_id_str = IdHelper.to_string(task_params.feature_view.feature_view_id)
    parent_materialization_id_str = IdHelper.to_string(export_params.parent_materialization_task_id)

    logger.info(
        f"Starting feature export {task_params.materialization_task_id} job for feature view {feature_view_id_str}: parent_materialization_task_id: {parent_materialization_id_str} for time range {start_time} to {end_time}"
    )
    fco_container = create_fco_container(
        list(task_params.virtual_data_sources) + list(task_params.transformations) + list(task_params.entities),
        deserialize_funcs_to_main=True,
    )
    fv_spec = specs.create_feature_view_spec_from_data_proto(task_params.feature_view)

    # TODO (vitaly): move local import once tecton and materialization sdk is unified in all scenarios
    from tecton.framework.feature_view import feature_view_from_spec

    fd = FeatureDefinition(fv_spec, fco_container)
    fv = feature_view_from_spec(fv_spec, fco_container)

    tecton_df = fv.get_historical_features(start_time=start_time, end_time=end_time)
    spark_df = tecton_df.to_spark()
    if spark_df.isEmpty():
        logging.info(f"No features found for time range {start_time} to {end_time}")
        return

    spark.conf.set(
        "spark.databricks.delta.commitInfo.userMetadata",
        f'{{"featureStartTime":"{export_params.feature_start_time.ToJsonString()}"}}',
    )
    is_write_optimized = spark.conf.get("spark.databricks.delta.optimizeWrite.enabled", None) == "true"
    df_to_write = spark_df if is_write_optimized else spark_df.coalesce(DEFAULT_COALESCE_FOR_S3)

    table_location = export_params.export_store_path
    # TODO (vitaly): allow customer to define a partition size that works for them
    partition_size = datetime.timedelta(days=1)
    version = fd.get_feature_store_format_version
    logging.info(
        f"Writing features to {table_location} for time range {start_time} to {end_time} with partition size={partition_size}"
    )

    assert fd.timestamp_key is not None, "feature definition needs to have a timestamp key for feature export"

    export_store_params = OfflineStoreWriterParams(
        s3_path=table_location,
        always_store_anchor_column=True,
        time_column=fd.timestamp_key,
        join_key_columns=fd.join_keys,
        is_continuous=fd.is_continuous,
    )

    writer = DeltaWriter(export_store_params, spark, version, partition_size)
    tile = pendulum.period(start_time, end_time)
    writer.upsert_dataframe_in_tile(df_to_write, tile)


def _run_id_from_dbutils(dbutils):
    context = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    run_id = json.loads(context).get("currentRunId", {}).get("id")
    if not run_id:
        msg = f"Unable to get Databricks run ID from context: {context}"
        raise RuntimeError(msg)
    logger.info(f"Found Databricks run ID: {run_id}")
    return str(run_id)


def _run_id_from_emr():
    try:
        with open(EMR_CLUSTER_INFO_PATH, "r") as f:
            emr_cluster_info = json.load(f)
        run_id = emr_cluster_info["jobFlowId"]
    except Exception as e:
        # for yarn docker runtime the file is mounted (not the entire path)
        try:
            with open(EMR_CLUSTER_INFO_FILE, "r") as f:
                emr_cluster_info = json.load(f)
            run_id = emr_cluster_info["jobFlowId"]
        except Exception:
            logger.error(f"Cluster info on EMR: FAILED with: {e}")
            raise e
    logger.info(f"Found EMR run ID: {run_id}")
    return run_id


def databricks_main(env):
    configure_logging()

    dbutils = env["dbutils"]
    spark = env["spark"]

    conf.set("TECTON_RUNTIME_ENV", "DATABRICKS")
    conf.set("TECTON_RUNTIME_MODE", "MATERIALIZATION")
    run_id = _run_id_from_dbutils(dbutils)
    serialized_params = dbutils.widgets.get("materialization_params")

    if serialized_params.startswith("s3://"):
        print(f"{serialized_params} appears to be an S3 URI, reading contents")
        bucket, key = _parse_bucket_key_from_uri(serialized_params)
        print(f"Bucket: {bucket}, Key: {key}")
        s3 = boto3.resource("s3")
        params_object = s3.Object(bucket, key)
        serialized_params = params_object.get()["Body"].read()
    elif serialized_params.startswith("dbfs:/"):
        print(f"{serialized_params} appears to be an DBFS Path, reading contents")
        dbfsPath = serialized_params.replace("dbfs:/", "/dbfs/")
        if os.path.exists(dbfsPath):
            with open(dbfsPath, "r") as f:
                serialized_params = f.read().strip()
        else:
            msg = f"Unable to find Materializaton Params in DBFS Path: {dbfsPath}"
            raise RuntimeError(msg)

    params = _deserialize_materialization_task_params(serialized_params)
    main(params, run_id, spark, step=None)


def main(params, run_id, spark, step, skip_legacy_execution_table_check=False):
    id_ = IdHelper.to_string(params.feature_view.feature_view_id)
    msg = f"Starting materialization for the FV '{id_}' params: {MessageToJson(params)}"
    # Both print and log so it will show up in the log (for Splunk) and on
    # the notebook page
    print(msg)
    logger.info(msg)

    _check_spark_job_uniqueness(
        params,
        run_id,
        spark,
        step,
        skip_legacy_execution_table_check,
    )

    # Run job twice if we are injecting a check for idempotency
    tries = 2 if "forced_retry" in params.feature_view.fco_metadata.workspace else 1
    for _ in range(tries):
        if params.HasField("ingest_task_info"):
            assert step is None
            raw_df = spark.read.parquet(params.ingest_task_info.ingest_parameters.ingest_path)
            ingest_pushed_df(spark, raw_df, params)
        elif params.HasField("deletion_task_info"):
            assert step is None
            deletion_parameters = params.deletion_task_info.deletion_parameters
            if deletion_parameters.online:
                run_online_store_deleter(spark, params)
            if deletion_parameters.offline:
                run_offline_store_deleter(spark, params)
        elif params.HasField("delta_maintenance_task_info"):
            assert step is None
            run_delta_maintenance(spark, params)
        elif params.HasField("batch_task_info"):
            batch_materialize_from_params(spark, params, run_id, step=step)
        elif params.HasField("stream_task_info"):
            stream_materialize_from_params(spark, params)
        elif params.HasField("feature_export_info"):
            feature_export_from_params(spark, params)
        else:
            msg = "Unknown task info"
            raise Exception(msg)


def _set_statsd_client_prefix(statsd_client, spark):
    # Calling the statsd client directly will always emit metrics from the driver.
    app_name = spark.conf.get("spark.app.name")
    statsd_client._prefix = f"spark.{app_name}.driver"


# There's a separate entrypoint in EMR, since it doesn't have `dbutils` by which we can read input params.
def _parse_bucket_key_from_uri(serialized_params):
    regex = r"s3://(\S+?)/(\S+)"
    match = re.search(regex, serialized_params)
    return match.group(1), match.group(2)


def get_statsd_client(spark: SparkSession):
    # TEMPORARY: statsd is a new library and requires restarting the internal
    # cluster, so we import it here and gate it behind a flag. This will allow
    # us to gradually roll it out to customers, so we don't have to restart all
    # clusters upon a single release.
    import statsd

    statsd_client = statsd.StatsClient("0.0.0.0", 3031)
    _set_statsd_client_prefix(statsd_client, spark)
    return statsd_client


def emr_main() -> None:
    configure_logging()

    parser = argparse.ArgumentParser(description="Tecton materialization library.")
    parser.add_argument(
        "--materialization-params", type=str, help="The parameters for this materialization task", default=None
    )
    parser.add_argument(
        "--spark-session-name", type=str, help="The name of the spark session created for this task", default=None
    )
    parser.add_argument(
        "--materialization-step",
        type=int,
        help="Materialization step",
        default=None,
    )

    parsed_args, unknown_args = parser.parse_known_args()
    print("Parsed: {}".format(parsed_args))
    print("Unknown: {}".format(unknown_args))
    print("Cluster region: {}".format(os.getenv("CLUSTER_REGION")))

    step = parsed_args.materialization_step
    serialized_params = parsed_args.materialization_params
    if os.path.exists(serialized_params):
        print(f"{serialized_params} appears to be a file, reading contents")
        with open(serialized_params, "r") as f:
            serialized_params = f.read()
            print(f"Materialization params contents: {serialized_params}")
    elif serialized_params.startswith("s3://"):
        print(f"{serialized_params} appears to be an S3 URI, reading contents")
        bucket, key = _parse_bucket_key_from_uri(serialized_params)
        print(f"Bucket: {bucket}, Key: {key}")
        s3 = boto3.resource("s3")
        params_object = s3.Object(bucket, key)
        serialized_params = params_object.get()["Body"].read()
    else:
        print(f"{serialized_params} appears to be the contents")

    params = _deserialize_materialization_task_params(serialized_params)

    spark = SparkSession.builder.appName(parsed_args.spark_session_name).getOrCreate()
    run_id = _run_id_from_emr()
    conf.set("TECTON_RUNTIME_ENV", "EMR")
    conf.set("TECTON_RUNTIME_MODE", "MATERIALIZATION")

    main(params, run_id, spark, step)


def local_test_main(spark, mat_params_path):
    configure_logging()

    with open(mat_params_path, "r") as f:
        serialized_params = f.read()

    params = _deserialize_materialization_task_params(serialized_params)
    main(params, 0, spark, step=None)


def configure_logging() -> None:
    # Set the logging level to INFO since materialization logs are internal.
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stderr,
        format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    # This spams logs on INFO or above.
    logging.getLogger("py4j.java_gateway").setLevel(logging.WARN)


if __name__ == "__main__":
    emr_main()
