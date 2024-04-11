"""
Invokes django-admin when the django module is run as a script.

Example: python -m django check
"""
from yui import core

if __name__ == "__main__":
    core.execute()
