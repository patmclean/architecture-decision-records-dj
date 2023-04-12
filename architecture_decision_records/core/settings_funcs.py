"""Helper functions to detect settings after app initialization (AKA 'dynamic settings')."""
import os
from distutils.util import strtobool
from functools import lru_cache

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def is_truthy(arg):
    """
    Convert "truthy" strings into Booleans.
    Examples:
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg
    return bool(strtobool(str(arg)))

# TODO, maybe switch secrets from a .env to a json? Which can be deployed as part of the deployment pipeline?
# with open(os.path.join(os.path.dirname(__file__), 'secrets.json'), 'r') as f:
#     secrets = json.loads(f.read())
def get_secret(setting, default):
    """Get the secret variable or return explicit exception."""
    try:
        return os.getenv(setting, default)
    except KeyError as exc:
        error_msg = f"Set the {setting} environment variable"
        raise ImproperlyConfigured(error_msg) from exc