#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import socket
# import png 
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myLibrary.settings')
    try:
        from django.core.management import execute_from_command_line
        # execute_from_command_line([sys.argv[0], "runserver", f"{IPAddr}:4000"])
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print(sys.argv)
    if sys.argv[1]== 'runserver':
        execute_from_command_line([sys.argv[0], "runserver", f"{IPAddr}:4000"])
    else:
        execute_from_command_line(sys.argv)
    # print(pyqrcode.create(f"{IPAddr}:4000"))


if __name__ == '__main__':
    main()
