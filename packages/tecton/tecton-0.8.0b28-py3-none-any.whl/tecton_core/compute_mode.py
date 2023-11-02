from enum import Enum

from tecton_core import conf
from tecton_core.query.dialect import Dialect
from tecton_proto.common import compute_mode_pb2


class ComputeMode(str, Enum):
    """Represents the compute mode for training data generation queries."""

    SPARK = "spark"
    SNOWFLAKE = "snowflake"
    ATHENA = "athena"
    DUCK_DB = "duckdb"

    def default_dialect(self) -> Dialect:
        return _COMPUTE_MODE_TO_DIALECT[self]


_COMPUTE_MODE_TO_DIALECT = {
    ComputeMode.SPARK: Dialect.SPARK,
    ComputeMode.SNOWFLAKE: Dialect.SNOWFLAKE,
    ComputeMode.ATHENA: Dialect.ATHENA,
    ComputeMode.DUCK_DB: Dialect.DUCKDB,
}


def get_compute_mode() -> ComputeMode:
    """Returns the default ComputeMode based on the environment."""

    compute_mode = conf.get_or_raise("TECTON_COMPUTE_MODE")
    if compute_mode == ComputeMode.DUCK_DB:
        return ComputeMode.DUCK_DB
    elif conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED") or compute_mode == ComputeMode.SNOWFLAKE:
        return ComputeMode.SNOWFLAKE
    elif conf.get_bool("ALPHA_ATHENA_COMPUTE_ENABLED") or compute_mode == ComputeMode.ATHENA:
        return ComputeMode.ATHENA
    elif compute_mode == ComputeMode.SPARK:
        return ComputeMode.SPARK
    else:
        msg = f"Invalid Tecton compute mode: {compute_mode}. Must be one of {[[e.value for e in ComputeMode]]}"
        raise ValueError(msg)


class BatchComputeMode(Enum):
    """Represents that compute mode for batch jobs associated with a FeatureView."""

    SPARK = compute_mode_pb2.ComputeMode.COMPUTE_MODE_SPARK
    SNOWFLAKE = compute_mode_pb2.ComputeMode.COMPUTE_MODE_SNOWFLAKE
    TECTON = compute_mode_pb2.ComputeMode.COMPUTE_MODE_TECTON

    @property
    def value(self) -> compute_mode_pb2.ComputeMode:
        return super().value


_COMPUTE_MODE_TO_BATCH = {
    ComputeMode.SPARK: BatchComputeMode.SPARK,
    ComputeMode.SNOWFLAKE: BatchComputeMode.SNOWFLAKE,
    ComputeMode.DUCK_DB: BatchComputeMode.TECTON,
}


def default_batch_compute_mode() -> BatchComputeMode:
    # For now this just returns the same thing as get_compute_mode(), but soon will be switched to use a different
    # config knob.
    return _COMPUTE_MODE_TO_BATCH[get_compute_mode()]
