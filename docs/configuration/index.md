# Configuration

This section describes how to get started with configuring the ADR App.

## Initializing the Configuration

An initial configuration can be created by executing `adrs init`. This will generate a new configuration with all of the default settings provided for you, and will also generate a unique [`SECRET_KEY`](required-settings.md#secret_key).

By default (if you haven't set [`ADR_ROOT`](#the-adr-app-root-directory) to some other value), the file will be created at `$HOME/.adr/adr_config.py`:

```no-highlight
adrs init
```

Example output:

```no-highlight
Configuration file created at '/opt/adr/adr_config.py'
```

!!! tip
    The [Installation Docs](../admin/install.md#choose-your-ADR_ROOT) example sets `ADR_ROOT` to `/opt/adr`, so `adr_config.py` would be found at `/opt/adr/adr_config.py`.

You may specify a different location for the configuration as the argument to `init`:

```no-highlight
adrs init /tmp/custom_config.py
```

```no-highlight
Configuration file created at '/tmp/custom_config.py'
```

!!! note
    Throughout the documentation, the configuration file will be referred to by name as `adr_config.py`. If you use a custom file name, you must use that instead.

## Specifying your Configuration

If you place your configuration in the default location at `$HOME/.adr/adr_config.py`, you may utilize the `adrs` command and it will use that location automatically.

If you do not wish to utilize the default location, you have two options:

### Environment variable

You may also set the `ADR_CONFIG` environment variable to the location of your configuration file so that you don't have to keep providing the `--config` argument. If set, this overrides the default location.

```no-highlight
export ADR_CONFIG=/etc/adr_config.py
adrs shell
```

## The ADR App Root Directory

By default, the ADR App will always read or store files in `~/.adr` to allow for installation without requiring superuser (root) permissions.

The `ADR_ROOT` configuration setting specifies where these files will be stored on your file system. You may customize this location by setting the `ADR_ROOT` environment variable. For example:

```no-highlight
export ADR_ROOT=/opt/adr
```

This setting is also used in the [ ADR App deployment guide](../admin/install.md) to make the `adrs` command easier to find and use.

!!! note
    The `--config` argument and the `adr_config` environment variable will always take precedence over `ADR_ROOT` for the purpose of telling ADR App where your `adr_config.py` can be found.

!!! warning
    Do not override `ADR_ROOT` in your `adr_config.py`. It will not work as expected. If you need to customize this setting, please always set the `ADR_ROOT` environment variable.

## Configuration Parameters

While the ADR App has many configuration settings, only a few of them must be defined at the time of installation. These configuration parameters may be set in `adr_config.py` or by default many of them may also be set by environment variables. Please see the following links for more information:

* [Required settings](required-settings.md)
* [LDAP Authentication](ldap.md)

## Changing the Configuration

Configuration settings may be changed at any time. However, the WSGI service (e.g. uWSGI) must be restarted before the changes will take effect. For example, if you're running the ADR App using `systemd:`

```no-highlight
sudo systemctl restart adr.service
```

## Advanced Configuration

### Troubleshooting the Configuration

To facilitate troubleshooting and debugging of settings, try inspecting the settings from a shell.

First get a shell and load the Django settings:

```no-highlight
adrs shell
```

Output:

```no-highlight
Python 3.10.6 (main, Mar 10 2023, 10:55:28) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

Inspect the `SETTINGS_PATH` variable. Does it match the configuration you're expecting to be loading?

```no-highlight
>>> settings.SETTINGS_PATH
'/home/example/.adr/adr_config.py'
```

If not, double check that you haven't set the `adr_config` environment variable, or if you did, that the path defined there is the correct one.

```no-highlight
echo $adr_config
```
