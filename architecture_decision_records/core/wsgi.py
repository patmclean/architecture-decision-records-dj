"""
WSGI config for core project.
"""

from django.core.wsgi import get_wsgi_application

import architecture_decision_records

# This is the Django default left here for visibility on how the architecture_decision_records pattern
# differs.
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "architecture_decision_records.core.settings")

# Instead of importing `DJANGO_SETTINGS_MODULE` we're using the custom loader
# pattern from `architecture_decision_records.core.runner` to read environment or config path for us.
architecture_decision_records.setup()

application = get_wsgi_application()
