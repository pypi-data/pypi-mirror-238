from tecton_core.compute_mode import ComputeMode
from tecton_core.compute_mode import get_compute_mode


def default_case(field_name: str) -> str:
    # Snowflake defaults to uppercase
    if get_compute_mode() == ComputeMode.SNOWFLAKE:
        return field_name.upper()
    else:
        return field_name


def anchor_time() -> str:
    return default_case("_anchor_time")


def effective_timestamp() -> str:
    return default_case("_effective_timestamp")


def expiration_timestamp() -> str:
    return default_case("_expiration_timestamp")


def timestamp_plus_ttl() -> str:
    return default_case("_timestamp_plus_ttl")


def tecton_secondary_key_aggregation_indicator_col() -> str:
    return default_case("_tecton_secondary_key_aggregation_indicator")


def tecton_unique_id_col() -> str:
    return default_case("_tecton_unique_id")


def udf_internal() -> str:
    """Namespace used in `FeatureDefinitionAndJoinConfig` for dependent feature view
    columns. Dependent FVs to ODFVs have this prefix in the name and are
    filtered out before being returned to the user.
    """
    return default_case("_udf_internal")


def odfv_internal_staging_table() -> str:
    return default_case("_odfv_internal_table")


def aggregation_group_id() -> str:
    return default_case("_tecton_aggregation_window_id")


def inclusive_start_time() -> str:
    return default_case("_tecton_inclusive_start_time")


def exclusive_end_time() -> str:
    return default_case("_tecton_exclusive_end_time")


def window_end_column_name() -> str:
    return default_case("tile_end_time")
