#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    sys.path.append(os.environ['PYTHONPATH'])
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_shop.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
