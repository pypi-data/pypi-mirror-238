import contextlib

from cloud_tpu_diagnostics.src.debug import start_debugging
from cloud_tpu_diagnostics.src.debug import stop_debugging


@contextlib.contextmanager
def diagnose(config):
  """Context manager to debug and identify errors."""
  if config is not None and config.debug_config is not None:
    start_debugging(config.debug_config)
  try:
    yield
  finally:
    if config is not None and config.debug_config is not None:
      stop_debugging(config.debug_config)
