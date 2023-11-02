import sys
from io import StringIO
from ..tracemate.logging_setup import setup_logging

def test_console_output():
    captured_output = StringIO()
    sys.stdout = captured_output
    ui_logger, backend_logger, console = setup_logging()
    console.print("Expected console message")
    sys.stdout = sys.__stdout__

    assert "Expected console message" in captured_output.getvalue()  # Replace with your actual console message
