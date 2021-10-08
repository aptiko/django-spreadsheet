import os
import sys

import django
from django.core import management

os.environ[
    "DJANGO_SETTINGS_MODULE"
] = "tests.testdjangoproject.testdjangoproject.settings"
sys.path.append("tests/testdjangoproject")
django.setup()
management.call_command("migrate")
