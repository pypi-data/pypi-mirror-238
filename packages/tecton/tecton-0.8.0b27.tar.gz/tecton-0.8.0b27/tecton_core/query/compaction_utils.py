import datetime
from collections import defaultdict
from typing import List
from typing import Optional
from typing import Tuple

import attrs

from tecton_core import feature_definition_wrapper
from tecton_core import schema
from tecton_core import schema_derivation_utils
from tecton_core.specs import TimeWindowSpec
from tecton_proto.args import feature_view_pb2 as feature_view__args_pb2
from tecton_proto.common import schema_pb2
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2


@attrs.frozen
class AggregationGroup:
    """AggregationGroup represents a group of aggregate features to compute with a corresponding start/end.

    The typical usage of this will be in compaction jobs, where we will use the start/end time to determine
    eligible rows for each individual aggregate.
    """

    window_index: int
    inclusive_start_time: Optional[datetime.datetime]
    exclusive_end_time: datetime.datetime
    aggregate_features: Tuple[feature_view__data_pb2.AggregateFeature, ...]
    schema: schema.Schema


def compute_batch_table_schema_for_aggregate_feature_view(
    view_schema: schema_pb2.Schema,
    aggregations: List[feature_view__args_pb2.FeatureAggregation],
) -> schema_pb2.OnlineBatchTableFormat:
    view_schema_column_map = {column.name: column for column in view_schema.columns}

    grouped_aggs = defaultdict(list)

    # Group by
    for aggregation in aggregations:
        key = TimeWindowSpec.from_args_proto(aggregation.time_window)
        grouped_aggs[key].append(aggregation)

    # Sort by two keys
    sorted_grouped_aggs = sorted(grouped_aggs.items(), key=lambda item: item[0])

    parts = []

    for index, (window, sub_aggs) in enumerate(sorted_grouped_aggs):
        added = set()
        columns = []
        for aggregation in sub_aggs:
            # NOTE: we are intentionally avoiding the special code paths for is_continuous
            # since they are not a desired pattern long term.
            aggregation_columns = schema_derivation_utils._get_aggregation_columns(
                view_schema_column_map, aggregation, is_continuous=False
            )
            for col in aggregation_columns:
                if col.name not in added:
                    columns.append(col)
                    added.add(col.name)

        output_schema = schema_pb2.Schema(columns=sorted(columns, key=lambda col: col.name))
        part = schema_pb2.OnlineBatchTablePart(
            window_index=index, time_window=window.to_data_proto(), schema=output_schema
        )
        parts.append(part)

    return schema_pb2.OnlineBatchTableFormat(online_batch_table_parts=parts)


def aggregation_groups(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper, exclusive_end_time: datetime.datetime
) -> Tuple[AggregationGroup, ...]:
    aggregation_map = defaultdict(list)
    for aggregation in fdw.trailing_time_window_aggregation.features:
        aggregation_map[TimeWindowSpec.from_data_proto(aggregation.time_window)].append(aggregation)

    agg_groups = fdw.fv_spec.online_batch_table_format.online_batch_table_parts

    if len(agg_groups) != len(aggregation_map):
        msg = "unexpected difference in length of the spec's online_batch_table_format and trailing_time_window_aggregation"
        raise ValueError(msg)

    return tuple(
        AggregationGroup(
            window_index=group.window_index,
            inclusive_start_time=exclusive_end_time + group.time_window.window_start,
            exclusive_end_time=exclusive_end_time + group.time_window.window_end,
            aggregate_features=tuple(aggregation_map[group.time_window]),
            schema=group.schema,
        )
        for group in agg_groups
    )
