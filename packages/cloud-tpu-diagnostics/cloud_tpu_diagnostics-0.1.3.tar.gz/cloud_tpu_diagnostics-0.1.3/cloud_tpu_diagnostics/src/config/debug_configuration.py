import dataclasses
from typing import Optional
from cloud_tpu_diagnostics.src.config import stack_trace_configuration


@dataclasses.dataclass
class DebugConfig:
  """Configuration for debugging.

  Attributes:
    stack_trace_config: config object for stack trace collection, default is
      None
  """

  stack_trace_config: Optional[stack_trace_configuration.StackTraceConfig] = (
      None
  )
