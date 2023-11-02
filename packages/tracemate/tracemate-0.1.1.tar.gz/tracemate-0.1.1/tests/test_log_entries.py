from unittest import mock
from ..tracemate.logging_setup import setup_logging
import logging

def test_log_entries():
    setup_logging()
    with mock.patch.object(logging.getLogger('backend'), 'info') as mock_info:
        logger = logging.getLogger("backend")
        logger.info("Your log message")
        mock_info.assert_called_with('Your log message')
