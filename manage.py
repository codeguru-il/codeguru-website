#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv


def main():
    """Run administrative tasks."""

    is_running_on_azure = "WEBSITE_HOSTNAME" in os.environ

    # Local development only - read environment variables from file
    if not is_running_on_azure:
        print("Loading environment variables from .env file")
        load_dotenv(".env")

    settings_module = "website.production" if is_running_on_azure else "website.settings"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
