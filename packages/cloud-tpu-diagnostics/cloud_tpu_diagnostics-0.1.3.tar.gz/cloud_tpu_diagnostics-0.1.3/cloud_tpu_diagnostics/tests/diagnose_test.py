from unittest import mock
from absl.testing import absltest
from cloud_tpu_diagnostics.src.config import debug_configuration
from cloud_tpu_diagnostics.src.config import diagnostic_configuration
from cloud_tpu_diagnostics.src.config import stack_trace_configuration
from cloud_tpu_diagnostics.src.diagnose import diagnose


class DiagnoseTest(absltest.TestCase):

  @mock.patch(
      'cloud_tpu_diagnostics.src.diagnose.start_debugging'
  )
  @mock.patch(
      'cloud_tpu_diagnostics.src.diagnose.stop_debugging'
  )
  def testDiagnoseContextManager(
      self, stop_debugging_mock, start_debugging_mock
  ):
    debug_config = debug_configuration.DebugConfig(
        stack_trace_config=stack_trace_configuration.StackTraceConfig(
            collect_stack_trace=True,
            stack_trace_to_cloud=True,
        ),
    )
    diagnostic_config = diagnostic_configuration.DiagnosticConfig(
        debug_config=debug_config,
    )
    with diagnose(diagnostic_config):
      pass
    start_debugging_mock.assert_called_once_with(debug_config)
    stop_debugging_mock.assert_called_once_with(debug_config)


if __name__ == '__main__':
  absltest.main()
