#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.db import connections
from django.db.utils import OperationalError

def check_db_connection():
    db_conn = connections['default']
    try:
        db_conn.cursor()
        print("Database connection OK")
    except OperationalError:
        print("Database connection failed")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egyptian_National_ID_Validator.settings')
    try:
        check_db_connection()
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
