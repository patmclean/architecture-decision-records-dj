# Gunicorn

Like most Django applications, the App runs as a [WSGI application](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) behind an HTTP server. This documentation shows how to install and configure [gunicorn](http://gunicorn.org/) (which is automatically installed with the App) for this role, however other WSGI servers are available and should work similarly well. [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) is a popular alternative.

## Configuration

The App ships with a default configuration file for gunicorn. ships with a default configuration file for gunicorn. To use it, copy `/opt/adra/config/gunicorn/prod.py` to `/opt/adra/config/prod.py`. (We make a copy of this file rather than pointing to it directly to ensure that any local changes to it do not get overwritten by a future upgrade.)

While the provided configuration should suffice for most initial installations, you may wish to edit this file to change the bound IP address and/or port number, or to make performance-related adjustments. See [the Gunicorn documentation](https://docs.gunicorn.org/en/stable/configure.html) for the available configuration parameters.

## systemd Setup

We'll use systemd to control  gunicorn and NetBox's background worker process. First, copy `config/systemd/adra.service` to the `/etc/systemd/system/` directory and reload the systemd daemon.

!!! warning "Check user & group assignment"
    The stock service configuration files packaged with NetBox assume that the service will run with the `adra` user and group names. If these differ on your installation, be sure to update the service files accordingly.

```no-highlight
sudo cp -v /config/adra.service /etc/systemd/system/
sudo systemctl daemon-reload
```

Then, start the `adra` service and enable it to initiate at boot time:

```no-highlight
sudo systemctl start adra
sudo systemctl enable adra
```

You can use the command `systemctl status adra` to verify that the WSGI service is running:

```no-highlight
systemctl status adra
```

You should see output similar to the following:

```no-highlight
● adra.service - NetBox WSGI Service
     Loaded: loaded (/etc/systemd/system/adra.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2021-08-30 04:02:36 UTC; 14h ago
       Docs: https://docs.netbox.dev/
   Main PID: 1140492 (gunicorn)
      Tasks: 19 (limit: 4683)
     Memory: 666.2M
     CGroup: /system.slice/adra.service
             ├─1140492 /opt/adra/bin/python3 /opt/adra/bin/gunicorn --pid /va>
             ├─1140513 /opt/adra/bin/python3 /opt/adra/bin/gunicorn --pid /va>
             ├─1140514 /opt/adra/bin/python3 /opt/adra/bin/gunicorn --pid /va>
...
```

!!! note
    If the service fails to start, issue the command `journalctl -eu adra` to check for log messages that may indicate the problem.

Once you've verified that the WSGI workers are up and running, move on to HTTP server setup.
