import os
from tracemate.logging_setup import setup_logging

def test_log_file_creation():
    setup_logging()
    assert os.path.exists('tracemate_backend.log')
