# Required Configuration Settings

## ALLOWED_HOSTS

This is a list of valid fully-qualified domain names (FQDNs) and/or IP addresses that can be used to reach the ADR App service. Usually this is the same as the hostname for the ADR App server, but can also be different; for example, when using a reverse proxy serving the ADR App website under a different FQDN than the hostname of the ADR App server. To help guard against [HTTP Host header attacks](https://docs.djangoproject.com/en/stable/topics/security/#host-headers-virtual-hosting), the ADR App will not permit access to the server via any other hostnames (or IPs).

Keep in mind that by default the ADR App sets [`USE_X_FORWARDED_HOST`](https://docs.djangoproject.com/en/stable/ref/settings/#use-x-forwarded-host) to `True`, which means that if you're using a reverse proxy, the FQDN used to reach that reverse proxy needs to be in this list.

!!! note
    This parameter must always be defined as a list or tuple, even if only a single value is provided.

Example:

```python
ALLOWED_HOSTS = ['adr.example.com', '192.0.2.123']
```

!!! tip
    If there is more than one hostname in this list, you *may* also need to set [`CSRF_TRUSTED_ORIGINS`](optional-settings.md#csrf_trusted_origins) as well.

If you are not yet sure what the domain name and/or IP address of the ADR App installation will be, and are comfortable accepting the risks in doing so, you can set this to a wildcard (asterisk) to allow all host values:

```python
ALLOWED_HOSTS = ['*']
```

!!! warning
    It is not recommended to leave this value as `['*']` for production deployments. Please see the [official Django documentation on `ALLOWED_HOSTS`](https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts) for help.

---

The following Environment Variable: `ADR_ALLOWED_HOSTS` specified as a space-separated quoted string (e.g. `ADR_ALLOWED_HOSTS="localhost 127.0.0.1 example.com"`) may be used for this setting.

## DATABASES

The ADR App requires access to a PostgreSQL database service to store data. This service can run locally on the ADR App server or on a remote system. The following parameters must be defined within the `DATABASES` dictionary:

* `NAME` - Database name
* `USER` - Database username
* `PASSWORD` - Database password
* `HOST` - Name or IP address of the database server (use `localhost` if running locally)
* `PORT` - The port to use when connecting to the database. An empty string means the default port for your selected backend. (PostgreSQL: `5432`)
* `CONN_MAX_AGE` - Lifetime of a [persistent database connection](https://docs.djangoproject.com/en/stable/ref/databases/#persistent-connections), in seconds (300 is the default)

The following environment variables may also be set for each of the above values:

* `ADR_DB_NAME`
* `ADR_DB_USER`
* `ADR_DB_PASSWORD`
* `ADR_DB_HOST`
* `ADR_DB_PORT`
* `ADR_DB_TIMEOUT`

Example:

```python
DATABASES = {
    'default': {
        'NAME': 'adr_db',                           # Database name
        'USER': 'adr_db_user',                      # Database username
        'PASSWORD': 'awesomely_secure_password',    # Database password
        'HOST': 'localhost',                        # Database server
        'PORT': '',                                 # Database port (leave blank for default)
        'CONN_MAX_AGE': 300,                        # Max database connection age
    }
}
```

!!! note
    The ADR App supports all database options supported by the underlying Django framework. For a complete list of available parameters, please see [the official Django documentation on `DATABASES`](https://docs.djangoproject.com/en/stable/ref/settings/#databases).

---

## SECRET_KEY

Environment Variable: `ADR_SECRET_KEY`

This is a secret, random string used to assist in the creation new cryptographic hashes for passwords and HTTP cookies. The key defined here should not be shared outside of the configuration file. `SECRET_KEY` can be changed at any time, however be aware that doing so will invalidate all existing sessions.

`SECRET_KEY` should be at least 50 characters in length and contain a random mix of letters, digits, and symbols.

!!! note
    A unique `SECRET_KEY` is generated for you automatically when you use `adrs init` to create a new `adr_config.py`.

You may run `adrs generate_secret_key` to generate a new key at any time.

Alternatively use the following command to generate a secret even before `adrs` is runnable:
<!-- spell-checker: disable -->
```no-highlight
LC_ALL=C tr -cd '[:lower:][:digit:]!@#$%^&*(\-_=+)' < /dev/urandom | fold -w50 | head -n1
```
<!-- spell-checker: enable -->
Example output:
<!-- spell-checker: disable -->
```no-highlight
9.V$@Kxkc@@Kd@z<a/=.J-Y;rYc79<y@](9o9(L(*sS)Q+ud5P
```
<!-- spell-checker: enable -->
!!! warning
    In the case of a highly available installation with multiple web servers, `SECRET_KEY` must be identical among all servers in order to maintain a persistent user session state.
