# Tracemate :mag_right:

![Python](https://img.shields.io/badge/python-v3.9-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/github/workflow/status/alexfigueroa-solutions/Tracemate/Python%20package)
![PyPI](https://img.shields.io/pypi/v/tracemate)
![Downloads](https://img.shields.io/pypi/dm/tracemate)

_Automated logging setup for Python applications_

Tracemate is a Python library designed to make logging hassle-free. Just import it into your `main.py`, and Tracemate takes care of setting up logging for all your functions. It's lightweight, easy to integrate, and designed to have minimal impact on application performance.

![Tracemate Logo](assets/logo.png) <!-- replace with your actual logo -->

---

## :rocket: Features

- **Automated Logging**: Just import Tracemate in your `main.py` and it will automatically set up logging for all your functions.
- **High Performance**: Designed for minimal performance overhead.
- **Asynchronous Support**: Full support for asynchronous Python applications.
- **Simple Integration**: Easy to integrate into existing projects without modifying your codebase.

---

## :package: Installation

To install Tracemate, you can use pip:

```bash
pip install tracemate
```

---

## :hammer_and_wrench: Usage

Here's how to get started:

Use this in your main.py (or equivalent) file to autonomously add logging and obtain logger and console objects from a centralized location. You can use setup_logging from multiple modules and it works fine.

```python
from tracemate import setup_logging, apply_logger_to_all_functions

backend_logger, ui_logger, console = setup_logging()
apply_logger_to_all_functions(backend_logger)
```

For a more comprehensive guide, please refer to the [Documentation](#-documentation).

---

## 📖 Documentation

Detailed documentation is available on our [Wiki](https://github.com/alexfigueroa-solutions/Tracemate/wiki).

---

## :handshake: Contributing

Contributions, issues, and feature requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get started.

---

## :memo: License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

## :telephone_receiver: Contact

Created by [@alexfigueroa-solutions](https://github.com/alexfigueroa-solutions) - feel free to reach out!
