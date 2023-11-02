import logging
from rich.console import Console

def setup_logging(log_file_name='tracemate_backend.log'):
    logging.basicConfig(filename=log_file_name, level=logging.INFO, force=True)
    with open(log_file_name, 'a'):
        pass
    backend_logger = logging.getLogger('backend')
    ui_logger = logging.getLogger('ui')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    ui_logger.addHandler(console_handler)
    console = Console()
    return backend_logger, ui_logger, console
