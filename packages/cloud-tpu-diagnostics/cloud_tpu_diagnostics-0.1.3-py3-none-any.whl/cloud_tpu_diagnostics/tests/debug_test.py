import signal
import threading
from unittest import mock
from absl.testing import absltest
from cloud_tpu_diagnostics.src.config import debug_configuration
from cloud_tpu_diagnostics.src.config import stack_trace_configuration
from cloud_tpu_diagnostics.src.debug import send_user_signal
from cloud_tpu_diagnostics.src.debug import start_debugging
from cloud_tpu_diagnostics.src.debug import stop_debugging


class DebugTest(absltest.TestCase):

  def testDaemonThreadRunningWhenCollectStackTraceTrue(self):
    debug_config = debug_configuration.DebugConfig(
        stack_trace_config=stack_trace_configuration.StackTraceConfig(
            collect_stack_trace=True,
            stack_trace_to_cloud=False,
        ),
    )
    start_debugging(debug_config)
    self.assertEqual(threading.active_count(), 2)
    daemon_thread_list = list(
        filter(lambda thread: thread.daemon is True, threading.enumerate())
    )
    self.assertLen(daemon_thread_list, 1)

  def testDaemonThreadNotRunningWhenCollectStackTraceFalse(self):
    debug_config = debug_configuration.DebugConfig(
        stack_trace_config=stack_trace_configuration.StackTraceConfig(
            collect_stack_trace=False,
            stack_trace_to_cloud=False,
        ),
    )
    start_debugging(debug_config)
    self.assertEqual(threading.active_count(), 1)
    daemon_thread_list = list(
        filter(lambda thread: thread.daemon is True, threading.enumerate())
    )
    self.assertLen(daemon_thread_list, 0)

  @mock.patch(
      'cloud_tpu_diagnostics.src.debug.disable_stack_trace_dumping'
  )
  def testStopDebuggingDisableStackTraceDumpingCalled(
      self, disable_stack_trace_dumping_mock
  ):
    debug_config = debug_configuration.DebugConfig(
        stack_trace_config=stack_trace_configuration.StackTraceConfig(
            collect_stack_trace=True,
            stack_trace_to_cloud=True,
        ),
    )
    stop_debugging(debug_config)
    disable_stack_trace_dumping_mock.assert_called_once()

  def testSendUserSignalSIGUSR1SignalReceived(self):
    signal.signal(signal.SIGUSR1, user_signal_handler)
    stack_trace_interval_seconds = 1
    with self.assertRaises(Exception) as e:
      send_user_signal(stack_trace_interval_seconds)
    self.assertEqual(str(e.exception), 'SIGSUR1 signal received.')


def user_signal_handler(signum, _):
  raise Exception('SIGSUR1 signal received.')  # pylint: disable=broad-exception-caught


if __name__ == '__main__':
  absltest.main()
