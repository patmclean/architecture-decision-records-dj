# Deploying the ADR App: Web Service and Workers

## Services Overview

Like most Django applications, the ADR App runs as a [WSGI application](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) behind an HTTP server.

The ADR App comes pre-installed with [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) to use as the WSGI server, however other WSGI servers are available and should work similarly well. [Gunicorn](http://gunicorn.org/) is a popular alternative.

This document will guide you through setting up uWSGI and establishing the ADR App web service to run on system startup.

### Web Service

The ADR App includes an `adrs start` management command that directly invokes uWSGI. This command behaves exactly as uWSGI does, but allows us to maintain a single entrypoint into the ADR App application.

```no-highlight
adrs start --help
```

## Configuration

As the `adr` user, copy and paste the following into `$ADR_ROOT/uwsgi.ini`:
<!-- spell-checker: disable -->
```ini
[uwsgi]
; The IP address (typically localhost) and port that the WSGI process should listen on
socket = 127.0.0.1:8001

; Fail to start if any parameter in the configuration file isn’t explicitly understood by uWSGI
strict = true

; Enable master process to gracefully re-spawn and pre-fork workers
master = true

; Allow Python app-generated threads to run
enable-threads = true

;Try to remove all of the generated file/sockets during shutdown
vacuum = true

; Do not use multiple interpreters, allowing only the ADR App to run
single-interpreter = true

; Shutdown when receiving SIGTERM (default is respawn)
die-on-term = true

; Prevents uWSGI from starting if it is unable load the ADR App (usually due to errors)
need-app = true

; By default, uWSGI has rather verbose logging that can be noisy
disable-logging = true

; Assert that critical 4xx and 5xx errors are still logged
log-4xx = true
log-5xx = true

; Enable HTTP 1.1 keepalive support
http-keepalive = 1

;
; Advanced settings (disabled by default)
; Customize these for your environment if and only if you need them.
; Ref: https://uwsgi-docs.readthedocs.io/en/latest/Options.html
;

; Number of uWSGI workers to spawn. This should typically be 2n+1, where n is the number of CPU cores present.
; processes = 5

; If using subdirectory hosting e.g. example.com/the ADR App, you must uncomment this line. Otherwise you'll get double paths e.g. example.com/the ADR App/the ADR App/.
; Ref: https://uwsgi-docs.readthedocs.io/en/latest/Changelog-2.0.11.html#fixpathinfo-routing-action
; route-run = fixpathinfo:

; If hosted behind a load balancer uncomment these lines, the harakiri timeout should be greater than your load balancer timeout.
; Ref: https://uwsgi-docs.readthedocs.io/en/latest/HTTP.html?highlight=keepalive#http-keep-alive
; harakiri = 65
; add-header = Connection: Keep-Alive
; http-keepalive = 1
```
<!-- spell-checker: enable -->
This configuration should suffice for most initial installations, you may wish to edit this file to change the bound IP
address and/or port number, or to make performance-related adjustments. See [uWSGI
documentation](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html) for the available configuration parameters.

!!! note
    <!-- spell-checker: disable-next-line -->
    If you are deploying uWSGI behind a load balancer be sure to configure the harakiri timeout and keep alive appropriately.

## Setup systemd

We'll use `systemd` to control the application's uWSGI process.

!!! warning
    The following steps must be performed with _root_ permissions.

### The ADR App Service

Create the `systemd` unit file for the ADR App web service. Copy and paste the following into `/etc/systemd/system/adr.service`:
<!-- spell-checker: disable -->
```ini
[Unit]
Description=ADR App WSGI Service
Documentation=https://docs.psmware.io/architecture-decision-records-app-dj
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment="ADR_ROOT=/opt/adr"

User=adr
Group=adr
PIDFile=/var/tmp/adr.pid
WorkingDirectory=/opt/adr

ExecStart=/opt/adr/bin/adrs start --pidfile /var/tmp/adr.pid --ini /opt/adr/uwsgi.ini
ExecStop=/opt/adr/bin/adrs start --stop /var/tmp/adr.pid
ExecReload=/opt/adr/bin/adrs start --reload /var/tmp/adr.pid

Restart=on-failure
RestartSec=30
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
<!-- spell-checker: enable -->
### Configure systemd

Because we just added new service files, you'll need to reload the systemd daemon:

```no-highlight
sudo systemctl daemon-reload
```

Then, start the `adr.service` service and enable it to initiate at boot time:

```no-highlight
sudo systemctl enable --now adr.service
```

### Verify the service

You can use the command `systemctl status adr.service` to verify that the WSGI service is running:
<!-- spell-checker: disable -->
```no-highlight
adr.service - ADR App WSGI Service
     Loaded: loaded (/etc/systemd/system/adr.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2023-04-12 19:10:27 UTC; 3s ago
       Docs: https://docs.psmware.io/architecture-decision-records-app-dj
   Main PID: 10400 (adrs)
      Tasks: 2 (limit: 9406)
     Memory: 36.4M
        CPU: 292ms
     CGroup: /system.slice/adr.service
             ├─10400 /opt/adr/bin/python3 /opt/adr/bin/adrs start --pidfile /var/tmp/adr.pid --ini /opt/adr/uwsgi.ini
             └─10401 /opt/adr/bin/python3 /opt/adr/bin/adrs start --pidfile /var/tmp/adr.pid --ini /opt/adr/uwsgi.ini
```
<!-- spell-checker: enable -->
!!! note
    If the ADR App service fails to start, issue the command `journalctl -eu adr` to check for log messages that may indicate the problem.

Once you've verified that the WSGI service and worker are up and running, move on to [HTTP server setup](http.md).

## Troubleshooting

### SVG images not rendered

When serving the ADR App directly from uWSGI on RedHat or CentOS there may be a problem rendering .svg images to include the ADR App logo. On the RedHat based operating systems there is no file `/etc/mime.types` by default, unfortunately, uWSGI looks for this file to serve static files (see [Serving static files with uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/StaticFiles.html#mime-types)). To work around this copy the file `/etc/mime.types` from a known good system for example an Ubuntu/Debian system or even the ADR App container to /opt/the ADR App/mime.types. Then add the following line to your `uwsgi.ini` file and restart the ADR App services:

```no-highlight
mime-file = /opt/adr/mime.types
```

Alternatively, host the ADR App behind Nginx as instructed in [HTTP server setup](http.md).
