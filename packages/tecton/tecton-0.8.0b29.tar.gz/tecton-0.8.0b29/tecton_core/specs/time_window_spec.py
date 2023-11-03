import datetime

import attrs
from google.protobuf.duration_pb2 import Duration
from typeguard import typechecked

from tecton_core.time_utils import timedelta_to_proto
from tecton_core.time_utils import to_human_readable_str
from tecton_proto.args.feature_view_pb2 import TimeWindow as TimeWindowArgs
from tecton_proto.common.time_window_pb2 import TimeWindow


__all__ = [
    "TimeWindowSpec",
]


@attrs.frozen(order=True)
class TimeWindowSpec:
    # window_start and window_end are both negative timedeltas as window_end represents the offset and window_start
    # represents the offset - window_duration
    window_start: datetime.timedelta
    window_end: datetime.timedelta

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: TimeWindow) -> "TimeWindowSpec":
        return cls(
            window_start=proto.window_start.ToTimedelta(),
            window_end=proto.window_end.ToTimedelta(),
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: TimeWindowArgs) -> "TimeWindowSpec":
        return cls(
            window_start=Duration(
                seconds=proto.offset.seconds - proto.window_duration.seconds,
                nanos=proto.offset.nanos - proto.window_duration.nanos,
            ).ToTimedelta(),
            window_end=Duration(seconds=proto.offset.seconds, nanos=proto.offset.nanos).ToTimedelta(),
        )

    def to_data_proto(self) -> TimeWindow:
        return TimeWindow(
            window_start=timedelta_to_proto(self.window_start),
            window_end=timedelta_to_proto(self.window_end),
        )

    @property
    def window_duration(self) -> datetime.timedelta:
        return self.window_end - self.window_start

    @property
    def offset(self) -> datetime.timedelta:
        return self.window_end

    def to_args_proto(self) -> TimeWindowArgs:
        return TimeWindowArgs(
            window_duration=timedelta_to_proto(self.window_duration),
            offset=timedelta_to_proto(self.offset),
        )

    def to_tuple(self) -> tuple:
        return (self.window_start, self.window_end)

    def offset_string(self) -> str:
        return "offset_" + to_human_readable_str(-self.offset) if self.offset.total_seconds() < 0 else ""

    def window_duration_string(self) -> str:
        return to_human_readable_str(self.window_duration)

    def to_string(self) -> str:
        offset_name = self.offset_string()
        if offset_name:
            offset_name = f"_{self.offset_string()}"
        return f"{self.window_duration_string()}{offset_name}"
