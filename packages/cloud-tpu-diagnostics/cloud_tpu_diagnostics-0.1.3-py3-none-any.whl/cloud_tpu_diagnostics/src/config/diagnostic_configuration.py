import dataclasses
from typing import Optional
from cloud_tpu_diagnostics.src.config import debug_configuration


@dataclasses.dataclass
class DiagnosticConfig:
  """Configuration for diagnostic.

  Attributes:
    debug_config: config object for debugging, default is None
  """

  debug_config: Optional[debug_configuration.DebugConfig] = None
