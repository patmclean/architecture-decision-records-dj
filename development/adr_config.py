"""Base settings for the project."""
import os
import sys
import ldap

from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from django.core.exceptions import ImproperlyConfigured

from architecture_decision_records.core.settings import *  # noqa F401,F403
from architecture_decision_records.core.settings_funcs import is_truthy, get_secret


for key in [
    # "ALLOWED_HOSTS",
    "ADR_DB_NAME",
    "ADR_DB_USER",
    "ADR_DB_PASSWORD",
    "ADR_DB_HOST",
    "ADR_DB_PORT",
    "ADR_SECRET_KEY",
    "ADR_ALLOWED_HOSTS",
]:
    if not os.environ.get(key):
        raise ImproperlyConfigured(f"Required environment variable {key} is missing.")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("ADR_SECRET_KEY", "django-insecure-0w5!cas22(uo_@sz7yi33zw0b@1jd*j9!fu8u=o8w0mr+1ax1iv")

ALLOWED_HOSTS = os.getenv("ADR_ALLOWED_HOSTS", "*").split(" ")


DATABASES = {
    "default": {
        "NAME": os.getenv("ADR_DB_NAME", "adr"),  # Database name
        "USER": os.getenv("ADR_DB_USER", ""),  # Database username
        "PASSWORD": os.getenv("ADR_DB_PASSWORD", ""),  # Database password
        "HOST": os.getenv("ADR_DB_HOST", "localhost"),  # Database server
        "PORT": os.getenv("ADR_DB_PORT", ""),  # Database port (leave blank for default)
        "CONN_MAX_AGE": int(os.getenv("ADR_DB_TIMEOUT", "300")),  # Database timeout
        "ENGINE": os.getenv(
            "ADR_DB_ENGINE", "django.db.backends.postgresql"
        ),  # Database driver "postgresql"
    }
}



AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 1,
    ldap.OPT_REFERRALS: 0,
}

# This search matches users with the sAMAccountName equal to the provided username. This is required if the user's
# username is not in their DN (Active Directory).

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

# Define a group required to login.
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,dc=example,dc=ie", ldap.SCOPE_SUBTREE, "(&(objectClass=person)(sAMAccountName=%(user)s))")
AUTH_LDAP_CONNECTION_OPTIONS = { ldap.OPT_DEBUG_LEVEL: 1, ldap.OPT_REFERRALS: 0, }
# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "ou=users,dc=example,dc=ie",
    ldap.SCOPE_SUBTREE,
    "(objectClass=groupOfNames)",
)
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=app_user,ou=users,dc=example,dc=ie",
    "is_staff": "cn=app_staff,ou=users,dc=example,dc=ie",
    "is_superuser": "cn=app_admin,ou=users,dc=example,dc=ie",
}

# Added for automated group synchronisation for Tenancy
AUTH_LDAP_FIND_GROUP_PERMS = True

# Set the SERVER URI, and Bind DN and password
AUTH_LDAP_SERVER_URI = get_secret("AUTH_LDAP_SERVER_URI", "ldap://adr-dj-ad:389")
AUTH_LDAP_BIND_DN = get_secret("AUTH_LDAP_BIND_DN", "uid=administrator,ou=system")
AUTH_LDAP_BIND_PASSWORD = get_secret("AUTH_LDAP_BIND_PASSWORD", "secrets")

AUTHENTICATION_BACKENDS = (
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
)
AUTH_LDAP_CACHE_TIMEOUT = 3600
# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True
# This makes the default user a usable username
AUTH_LDAP_USER_QUERY_FIELD = "username"
# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True
# Cache distinguished names and group memberships for an hour to minimize
# LDAP traffic.
AUTH_LDAP_CACHE_TIMEOUT = 3600

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "username": "sAMAccountName",
}
