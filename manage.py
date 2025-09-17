#!/usr/bin/env python
import os, sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ValueTech.settings")
    from django.core.management import execute_from_command_line

    # Automatically add SSL flags for runserver_plus
    if len(sys.argv) > 1 and sys.argv[1] == "runserver_plus":
        # Only add these if they are not already in the command
        if "--cert-file" not in sys.argv and "--key-file" not in sys.argv:
            sys.argv += ["--cert-file", "cert.crt", "--key-file", "cert.key"]

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
