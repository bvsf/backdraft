#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sigcaw.settings")

    from django.core.management import execute_from_command_line

    try:
        import envdir
        envdir.open()
    except:
        pass

    execute_from_command_line(sys.argv)
