# Building Your Development Environment

## Quickstart Guide

The development environment can be used in two ways:

1. __(Recommended)__ All services, including the Django App, are spun up using Docker containers and a volume mount so you can develop locally.
2. With a local Poetry environment if you wish to develop outside of Docker, with the caveat of using external services provided by Docker for the PostgreSQL database service.

This is a quick reference guide if you're already familiar with the development environment provided, which you can read more about later in this document.

### Invoke

The [Invoke](http://www.pyinvoke.org/) library is used to provide some helper commands based on the environment. There are a few configuration parameters which can be passed to Invoke to override the default configuration:

- `project_name`: the default docker compose project name (default: `wmf`)
- `python_ver`: the version of Python to use as a base for any built docker containers (default: 3.8)
- `local`: a boolean flag indicating if invoke tasks should be run on the host or inside the docker containers (default: False, commands will be run in docker containers)
- `compose_dir`: the full path to a directory containing the project compose files
- `compose_files`: a list of compose files applied in order (see [Multiple Compose files](https://docs.docker.com/compose/extends/#multiple-compose-files) for more information)

Using __Invoke__ these configuration options can be overridden using [several methods](https://docs.pyinvoke.org/en/stable/concepts/configuration.html). Perhaps the simplest is setting an environment variable `INVOKE_WMF_VARIABLE_NAME` where `VARIABLE_NAME` is the variable you are trying to override. The only exception is `compose_files`, because it is a list it must be overridden in a YAML file. There is an example `invoke.yml` (`invoke.example.yml`) in this directory which can be used as a starting point.

### Docker Development Environment

!!! tip
    This is the recommended option for development.

This project is managed by [Python Poetry](https://python-poetry.org/) and has a few requirements to setup your development environment:

1. Install Poetry, see the [Poetry Documentation](https://python-poetry.org/docs/#installation) for your operating system.
2. Install Docker, see the [Docker documentation](https://docs.docker.com/get-docker/) for your operating system.

Once you have Poetry and Docker installed you can run the following commands (in the root of the repository) to install all other development dependencies in an isolated Python virtual environment:

```shell
poetry shell
poetry install
cp development/creds.example.env development/creds.env
invoke build
invoke start
```

The Django app can now be accessed at [http://localhost:8080](http://localhost:8080) and the live documentation at [http://localhost:8001](http://localhost:8001).

To either stop or destroy the development environment use the following options.

- __invoke stop__ - Stop the containers, but keep all underlying systems intact
- __invoke destroy__ - Stop and remove all containers, volumes, etc. (This results in data loss due to the volume being deleted)

### Local Poetry Development Environment

- Create an `invoke.yml` file with the following contents at the root of the repo and edit as necessary

Run the following commands:

```shell
poetry shell
poetry install
export $(cat development/dev.env | xargs)
export $(cat development/creds.env | xargs)
invoke start && sleep 5
python manage.py migrate
```

You can now run `python manage.py` commands as you would from the [Django documentation](https://docs.djangoproject.com) for example to start the development server:

```shell
python manage.py runserver 0.0.0.0:8080 --insecure
```

The Django app can now be accessed at [http://localhost:8080](http://localhost:8080).

It is typically recommended to launch the __runserver__ command in a separate shell so you can keep developing and manage the webserver separately.

### Updating the Documentation

Documentation dependencies are pinned to exact versions to ensure consistent results. For the development environment, they are defined in the `pyproject.toml` file.

### CLI Helper Commands

The project features a CLI helper based on [Invoke](https://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories:

- `dev environment`
- `utility`
- `testing`

Each command can be executed with `invoke <command>`. All commands support the arguments `--python-ver` if you want to manually define the version of Python to use. Each command also has its own help `invoke <command> --help`

#### Local Development Environment

```shell
  build            Build all docker images.
  debug            Start the app and its dependencies in debug mode.
  destroy          Destroy all containers and volumes.
  restart          Restart the app and its dependencies in detached mode.
  start            Start the app and its dependencies in detached mode.
  stop             Stop the app and its dependencies.
```

#### Utility

```shell
  cli              Launch a bash shell inside the running the app container.
  create-user      Create a new user in django (default: admin), will prompt for password.
  makemigrations   Run Make Migration in Django.
  migrate   Run Migrations in Django.
```

#### Testing

```shell
  bandit           Run bandit to validate basic static code security analysis.
  black            Run black to check that Python files adhere to its style standards.
  flake8           Run flake8 to check that Python files adhere to its style standards.
  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.
  pylint           Run pylint code analysis.
  tests            Run all tests for this plugin.
  unittest         Run Django unit tests for the plugin.
```

## Project Overview

This project provides the ability to develop and manage the app server locally (with supporting services being *Dockerised*) or by using only Docker containers to manage the app. The main difference between the two environments is the ability to debug and use __pdb__ when developing locally. Debugging with __pdb__ within the Docker container is more complicated, but can still be accomplished by either entering into the container (via `docker exec`) or attaching your IDE to the container and running the the app service manually within the container.

The upside to having the app service handled by Docker rather than locally is that you do not have to manage the app server. The [Docker logs](#docker-logs) provide the majority of the information you will need to help troubleshoot, while getting started quickly and not requiring you to perform several manual steps and remembering to have the app server running in a separate terminal while you develop.

!!! note
 The local environment still uses Docker containers for the supporting services (Postgres, Redis, and RQ Worker), but the Django App server is handled locally by you, the developer.

Follow the directions below for the specific development environment that you choose.

## Poetry

Poetry is used in lieu of the "virtualenv" commands and is leveraged in both environments. The virtual environment will provide all of the Python packages required to manage the development environment such as __Invoke__. See the [Local Development Environment](#local-poetry-development-environment) section to see how to install the app if you're going to be developing locally (i.e. not using the Docker container).

The `pyproject.toml` file outlines all of the relevant dependencies for the project:

- `tool.poetry.dependencies` - the main list of dependencies.
- `tool.poetry.dev-dependencies` - development dependencies, to facilitate linting, testing, and documentation building.

The `poetry shell` command is used to create and enable a virtual environment managed by Poetry, so all commands ran going forward are executed within the virtual environment. This is similar to running the `source venv/bin/activate` command with virtualenvs. To install project dependencies in the virtual environment, you should run `poetry install` - this will install __both__ project and development dependencies.

For more details about Poetry and its commands please check out its [online documentation](https://python-poetry.org/docs/).

## Full Docker Development Environment

This project is set up with a number of __Invoke__ tasks consumed as simple CLI commands to get developing fast. You'll use a few `invoke` commands to get your environment up and running.

### Copy the credentials file for the app

First, you need to create the `development/creds.env` file - it stores a bunch of private information such as passwords and tokens for your local the app install. You can make a copy of the `development/creds.example.env` and modify it to suit you.

```shell
cp development/creds.example.env development/creds.env
```

### Building the Docker Image

The first thing you need to do is build the necessary Docker image for the app that installs the specific `python_ver`. The image is used for django and the docs used by Docker Compose.

```bash
➜ invoke build
... <omitted for brevity>
#19 exporting to image
#19 exporting layers
#19 exporting layers 2.5s done
#19 writing image sha256:5e1e326448501f8769f575ff0b61240c6fd09ca8b5a1291b969833b459f5c881 done
#19 naming to docker.io/library/adrs:py3.10
#19 naming to docker.io/library/adrs:py3.10 done
#19 DONE 2.5s
```

### Starting the Development Environment

Next, you need to start up your Docker containers.

```bash
➜ invoke start
Starting NSE ADR in detached mode...
Running docker-compose command "up --detach"
Network adrs_default  Creating
Network adrs_default  Created
Volume "adrs_postgres_data"  Creating
Volume "adrs_postgres_data"  Created
Container adrs-docs  Creating
Container adrs-db  Creating
Container adrs-ad  Creating
Container adrs-db  Created
Container adrs-api  Creating
Container adrs-docs  Created
Container adrs-ad  Created
Container adrs-api  Created
Container adrs-ad  Starting
Container adrs-db  Starting
Container adrs-docs  Starting
Container adrs-db  Started
Container adrs-api  Starting
Container adrs-ad  Started
Container adrs-docs  Started
Container adrs-api  Started
```

This will start all of the Docker containers used for hosting the app. You should see the following containers running after `invoke start` is finished.

```bash
➜ docker ps
____CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS          PORTS                                       NAMES
ff72cd6641e2   adrs:py3.10                                   "python manage.py ru…"   39 seconds ago   Up 35 seconds   0.0.0.0:8080->8080/tcp    adrs-api
b230d54faa75   adrs:py3.10                                   "mkdocs serve -v -a …"   39 seconds ago   Up 38 seconds   0.0.0.0:8001->8080/tcp    adrs-docs
b2e7b28ddc39   active-directory-it:develop                       "java -jar ldap-serv…"   39 seconds ago   Up 38 seconds   389/tcp                   adrs-ad
cf1b7b9c8f44   postgres:14-alpine                                "docker-entrypoint.s…"   39 seconds ago   Up 38 seconds   0.0.0.0:56269->5432/tcp   adrs-db
```

Once the containers are fully up, you should be able to open up a web browser, and view:

- The app homepage at [http://localhost:8080](http://localhost:8080)
- A live version of the documentation at [http://localhost:8001](http://localhost:8001)

!!! note
    Sometimes the containers take a minute or two, to fully spin up. If the page doesn't load right away, wait a minute and try again.

### Creating a Superuser

If you need to create a superuser, run the follow commands.

```bash
➜ invoke createsuperuser
Running docker-compose command "ps --services --filter status=running"
Running docker-compose command "run --entrypoint 'python manage.py createsuperuser --username admin' adrs-api"
Email address: email@example.com
Password (again):
Superuser created successfully.
```

### Invoke - Stopping the Development Environment

The last command to know for now is `invoke stop`.

```bash
➜ invoke stop
Stopping Dev Env...
Running docker-compose command "down"
Container adrs-docs  Stopping
Container adrs-ad  Stopping
Container adrs-api  Stopping
Container adrs-ad  Stopping
Container adrs-api  Stopping
Container adrs-docs  Stopping
Container adrs-api  Stopped
Container adrs-api  Removing
Container adrs-api  Removed
Container adrs-db  Stopping
Container adrs-db  Stopping
Container adrs-db  Stopped
Container adrs-db  Removing
Container adrs-db  Removed
Container adrs-ad  Stopped
Container adrs-ad  Removing
Container adrs-ad  Removed
Container adrs-docs  Stopped
Container adrs-docs  Removing
Container adrs-docs  Removed
Network adrs_default  Removing
Network adrs_default  Removed
```

This will safely shut down all of your running Docker containers for this project. When you are ready to spin containers back up, it is as simple as running `invoke start` again [as seen previously](#starting-the-development-environment).

!!! warning
 If you're wanting to reset the database and configuration settings, you can use the `invoke destroy` command, but __you will lose any data stored in those containers__, so make sure that is what you want to do.

### Real-Time Updates? How Cool

Your environment should now be fully setup, all necessary Docker containers are created and running, and you're logged into the app in your web browser. Now what?

Now you can start developing  in the project folder!

The magic here is the root directory is mounted inside your Docker containers when built and ran, so __any__ changes made to the files in here are directly updated to the app plugin code running in Docker. This means that as you modify the code in your plugin folder, the changes will be instantly updated in the app.

!!! warning
 There are a few exceptions to this, as outlined in the section [To Rebuild or Not To Rebuild](#to-rebuild-or-not-to-rebuild).

The back-end Django process is setup to automatically reload itself (it only takes a couple of seconds) every time a file is updated (saved). So for example, if you were to update one of the files like `models.py`, then save it, the changes will be visible right away in the web browser!

!!! info
    You may get connection refused while Django reloads, but it should be refreshed fairly quickly.

### Docker Logs

When trying to debug an issue, one helpful thing you can look at are the logs within the Docker containers.

```bash
➜ docker logs <name of container> -f
```

!!! note
    The `-f` tag will keep the logs open, and output them in realtime as they are generated.

So for example, our plugin is named `wmf`, the command would most likely be `docker logs adrs-api -f`. You can find the name of all running containers via `docker ps`.

If you want to view the logs specific to the worker container, simply use the name of that container instead.

## To Rebuild or Not to Rebuild

Most of the time, you will not need to rebuild your images. Simply running `invoke start` and `invoke stop` is enough to keep your environment going.

However there are a couple of instances when you will want to.

### Updating Environment Variables

To add environment variables to your containers, thus allowing the app to use them, you will update/add them in the `development/development.env` file. However, doing so is considered updating the underlying container shell, instead of Django (which auto restarts itself on changes).

To get new environment variables to take effect, you will need stop any running images, rebuild the images, then restart them. This can easily be done with 3 commands:

```bash
➜ invoke stop
➜ invoke build
➜ invoke start
```

Once completed, the new/updated environment variables should now be live.

### Installing Additional Python Packages

If you want your plugin to leverage another Python package, you can easily add them into your Docker environment.

```bash
➜ poetry shell
➜ poetry add <package_name>
```

Once the dependencies are resolved, stop the existing containers, rebuild the Docker image, and then start all containers again.

```bash
➜ invoke stop
➜ invoke build
➜ invoke start
```

### Updating Python Version

To update the Python version, you can update it within `tasks.py`.

```python
namespace = Collection("wmf")
namespace.configure(
    {
        "wmf": {
            ...
            "python_ver": "3.7",
     ...
        }
    }
)
```

## Other Miscellaneous Commands To Know

### Python Shell

To drop into a shell (in the Django Docker container) run:

```bash
➜ invoke cli
```

### Tests

To run tests against your code, you can run all of the tests with:

```bash
➜ invoke tests
```

To run an individual test, you can run any or all of the following:

```bash
➜ invoke unittest
➜ invoke bandit
➜ invoke black
➜ invoke flake8
➜ invoke pydocstyle
➜ invoke pylint
```
