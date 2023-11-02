import pytest
from ..tracemate.logging_setup import setup_logging  # replace with your actual function

def test_setup_logging():
    backend_logger, ui_logger, console = setup_logging()
    assert backend_logger is not None
    assert ui_logger is not None
    assert console is not None
