from unittest import mock
from ..tracemate.logging_setup import setup_logging
import logging

def test_ui_logger():
    with mock.patch('logging.getLogger') as MockLogger:
        ui_logger = MockLogger.return_value
        setup_logging()
        logger = logging.getLogger("ui")
        logger.info("Your ui log message")
        ui_logger.info.assert_called_with('Your ui log message')
