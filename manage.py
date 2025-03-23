#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import socket
# import pyqrcode  # Import pyqrcode for QR code generation

# Get system's IP address
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myLibrary.settings')
    try:
        from django.core.management import execute_from_command_line
        
        if sys.argv[1] == 'runserver':
            print(f"Starting server at http://{IPAddr}:4000/")
            # qr = pyqrcode.create(f"http://{IPAddr}:4000")
            # print(qr.terminal(quiet_zone=1))  # Display QR code in terminal
            execute_from_command_line([sys.argv[0], "runserver", f"{IPAddr}:4000"])
            
            # Allow external access
            # execute_from_command_line([sys.argv[0], "runserver", "0.0.0.0:4000"])

            # Generate and print QR code
        else:
            execute_from_command_line(sys.argv)

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

if __name__ == "__main__":
    main()
