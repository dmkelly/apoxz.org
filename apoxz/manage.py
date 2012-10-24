#!/usr/bin/env python
import os
import sys

# Required to allow this Django app to be run via upstart
sys.path.append("/var/www/apoxz.org/")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apoxz.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
