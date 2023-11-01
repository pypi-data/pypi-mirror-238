import dataclasses
from cloud_tpu_diagnostics.src.util import default


@dataclasses.dataclass
class StackTraceConfig:
  """Configuration for stack trace collection.

  Attributes:
    collect_stack_trace: enable/disable collection of stack trace in case fault
      occurs in the program. Default is False, which means stack trace will not
      be collected unless collect_stack_trace is set to True.
    stack_trace_to_cloud: enable/disable upload of stack trace to cloud. Default
      is False, which means stack trace will be displayed on the termial unless
      stack_trace_to_cloud is set to True.
    stack_trace_interval_seconds: time interval in seconds between collection of
      stack trace event. Default is 600, that is 10 minutes.
  """

  collect_stack_trace: bool = default.COLLECT_STACK_TRACE_DEFAULT
  stack_trace_to_cloud: bool = default.STACK_TRACE_TO_CLOUD_DEFAULT
  stack_trace_interval_seconds: int = default.STACK_TRACE_INTERVAL_SECONDS_DEFAULT
