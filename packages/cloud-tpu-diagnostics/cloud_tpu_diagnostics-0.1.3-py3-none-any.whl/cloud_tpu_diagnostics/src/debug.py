import signal
import threading
import time

from cloud_tpu_diagnostics.src.stack_trace import disable_stack_trace_dumping
from cloud_tpu_diagnostics.src.stack_trace import enable_stack_trace_dumping


def start_debugging(debug_config):
  """Context manager to debug and identify errors."""
  if (
      debug_config.stack_trace_config is not None
      and debug_config.stack_trace_config.collect_stack_trace
  ):
    thread = threading.Thread(
        target=send_user_signal,
        daemon=True,
        args=(debug_config.stack_trace_config.stack_trace_interval_seconds,),
    )
    thread.start()  # start a daemon thread
    enable_stack_trace_dumping(debug_config.stack_trace_config)


def stop_debugging(debug_config):
  """Context manager to debug and identify errors."""
  if (
      debug_config.stack_trace_config is not None
      and debug_config.stack_trace_config.collect_stack_trace
  ):
    disable_stack_trace_dumping(debug_config.stack_trace_config)


def send_user_signal(stack_trace_interval_seconds):
  """Send SIGUSR1 signal to main thread after every stack_trace_interval_seconds seconds."""
  while True:
    time.sleep(stack_trace_interval_seconds)
    signal.pthread_kill(threading.main_thread().ident, signal.SIGUSR1)
