# Configuring an HTTP Server

This documentation provides example configurations for [NGINX](https://www.nginx.com/resources/wiki/) though any HTTP server which supports WSGI should be compatible.

## Obtain an SSL Certificate

To enable HTTPS access to the ADR App, you'll need a valid SSL certificate. You can purchase one from a trusted commercial provider, obtain one for free from [Let's Encrypt](https://letsencrypt.org/getting-started/), or generate your own (although self-signed certificates are generally untrusted). Both the public certificate and private key files need to be installed on your ADR App server in a secure location that is readable only by the `root` user.

!!! warning
    The command below can be used to generate a self-signed certificate for testing purposes, however it is strongly recommended to use a certificate from a trusted authority in production.

Two files will be created: the public certificate (`adr.crt`) and the private key (`adr.key`). The certificate is published to the world, whereas the private key must be kept secret at all times.

!!! info
    Some Linux installations, including CentOS, have changed the location for SSL certificates from `/etc/ssl/` to `/etc/pki/tls/`. The command below may need to be changed to reflect the certificate location.

The following command will prompt you for additional details of the certificate; all of which are optional.
<!-- spell-checker: disable -->
```no-highlight
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/adr.key \
  -out /etc/ssl/certs/adr.crt
```
<!-- spell-checker: enable -->
## HTTP Server Installation

Any HTTP server of your choosing is supported. For your convenience, setup instructions for NGINX are provided here.

!!! warning
    The following steps must be performed with root permissions.

### NGINX

[NGINX](https://www.nginx.com/resources/wiki/) is a free, open source, high-performance HTTP server and reverse proxy
and is by far the most popular choice.

#### Install NGINX

Begin by installing NGINX:

On Ubuntu:

```no-highlight
sudo apt install -y nginx
```

On CentOS/RHEL:

```no-highlight
sudo dnf install -y nginx
```

#### Configure NGINX

Once NGINX is installed, copy and paste the following NGINX configuration into
`/etc/nginx/sites-available/adr.conf` for Ubuntu or `/etc/nginx/conf.d/adr.conf` for CentOS/RHEL:

!!! note
    If the file location of SSL certificates had to be changed in the [Obtain an SSL Certificate](#obtain-an-ssl-certificate) step above, then the location will need to be changed in the NGINX configuration below.
<!-- spell-checker: disable -->
```nginxconf
server {
    listen 443 ssl http2 default_server;
    listen [::]:443 ssl http2 default_server;

    server_name _;

    ssl_certificate /etc/ssl/certs/adr.crt;
    ssl_certificate_key /etc/ssl/private/adr.key;

    client_max_body_size 25m;

    location /static/ {
        alias /opt/adr/static/;
    }

    # For subdirectory hosting, you'll want to toggle this (e.g. `/adr/`).
    # Don't forget to set `FORCE_SCRIPT_NAME` in your `adr_config.py` to match.
    # location /adr/ {
    location / {
        include uwsgi_params;
        uwsgi_pass  127.0.0.1:8001;
        uwsgi_param Host $host;
        uwsgi_param X-Real-IP $remote_addr;
        uwsgi_param X-Forwarded-For $proxy_add_x_forwarded_for;
        uwsgi_param X-Forwarded-Proto $http_x_forwarded_proto;

        # If you want subdirectory hosting, uncomment this. The path must match
        # the path of this location block (e.g. `/adr`). For NGINX the path
        # MUST NOT end with a trailing "/".
        # uwsgi_param SCRIPT_NAME /adr;
    }
}

server {
    # Redirect HTTP traffic to HTTPS
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 301 https://$host$request_uri;
}
```
<!-- spell-checker: enable -->
#### Enable the ADR App

On Ubuntu:

To enable the ADR App site, you'll need to delete `/etc/nginx/sites-enabled/default` and create a symbolic link in the
`sites-enabled` directory to the configuration file you just created:
<!-- spell-checker: disable -->
```no-highlight
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/adr.conf /etc/nginx/sites-enabled/adr.conf
```
<!-- spell-checker: enable -->
On CentOS:

Run the following command to disable the default site that comes with the `nginx` package:
<!-- spell-checker: disable -->
```no-highlight
sudo sed -i 's@ default_server@@' /etc/nginx/nginx.conf
```
<!-- spell-checker: enable -->
#### Restart NGINX

Finally, restart the `nginx` service to use the new configuration.
<!-- spell-checker: disable -->
```no-highlight
sudo systemctl restart nginx
```
<!-- spell-checker: enable -->
!!! info
    If the restart fails, and you changed the default key location, check to make sure the `adr.conf` file you pasted has the updated key location. For example, CentOS requires keys to be in `/etc/pki/tls/` instead of `/etc/ssl/`.

## Confirm Permissions for ADR_ROOT

Ensure that the `ADR_ROOT` permissions are set to `755`.
If permissions need to be changed, as the `adr` user run:
<!-- spell-checker: disable -->
```no-highlight
chmod 755 $ADR_ROOT
```
<!-- spell-checker: enable -->
## Confirm Connectivity

At this point, you should be able to connect to the HTTPS service at the server name or IP address you provided. If you used a self-signed certificate, you will likely need to explicitly allow connectivity in your browser.

!!! info
    Please keep in mind that the configurations provided here are bare minimums required to get the ADR App up and running. You may want to make adjustments to better suit your production environment.

!!! warning
    Certain components of the ADR App (such as the display of rack elevation diagrams) rely on the use of embedded objects. Ensure that your HTTP server configuration does not override the `X-Frame-Options` response header set by the ADR App.

## Troubleshooting

### Unable to Connect

If you are unable to connect to the HTTP server, check that:

- NGINX is running and configured to listen on the correct port.
- Access is not being blocked by a firewall somewhere along the path. (Try connecting locally from the server itself.)

### Static Media Failure

If you get a *Static Media Failure; The following static media file failed to load: css/base.css*, verify the permissions on the `$ADR_ROOT` directory are `755`.

Example of correct permissions (at the `[root@localhost ~]#` prompt)
<!-- spell-checker: disable -->
```no-highlight
ls -l /opt/
```
<!-- spell-checker: enable -->
Example output:
<!-- spell-checker: disable -->
```no-highlight
total 4
drwxr-xr-x. 11 adr adr 4096 Apr  5 11:24 adr

```
<!-- spell-checker: enable -->
If the permissions are not correct, modify them accordingly.

Example of modifying the permissions:
<!-- spell-checker: disable -->
```no-highlight
ls -l /opt/
```
<!-- spell-checker: enable -->
Example output:
<!-- spell-checker: disable -->
```no-highlight
total 4
drwx------. 11 adr adr 4096 Apr  5 10:00 adr
```
<!-- spell-checker: enable -->
At the prompt `[adr@localhost ~]$` execute:
<!-- spell-checker: disable -->
```no-highlight
chmod 755 $ADR_ROOT
```
<!-- spell-checker: enable -->
Then to verify that the user has the permissions to the directory execute at the `[adr@localhost ~]$` prompt:
<!-- spell-checker: disable -->
```no-highlight
ls -l /opt/
```
<!-- spell-checker: enable -->
Example output shows that the user and group are both `adr` below:
<!-- spell-checker: disable -->
```no-highlight
total 4
drwxr-xr-x. 11 adr adr 4096 Apr  5 11:24 adr
```
<!-- spell-checker: enable -->
### 502 Bad Gateway

If you are able to connect but receive a 502 (bad gateway) error, check the following:

- The uWSGI worker processes are running (`systemctl status adr` should show a status of `active (running)`)
- NGINX is configured to connect to the port on which uWSGI is listening (default is `8001`).
- SELinux may be preventing the reverse proxy connection. You may need to allow HTTP network connections with the
  command `setsebool -P httpd_can_network_connect 1`. For further information, view the [SELinux
  troubleshooting](selinux-troubleshooting.md) guide.
