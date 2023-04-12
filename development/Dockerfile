
ARG PYTHON_VER
FROM python:${PYTHON_VER}-alpine


ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apk --no-cache upgrade && \
    apk add --no-cache --virtual .build-deps \
        build-base \
        musl-dev \
        openldap-dev \
        freetype-dev \
        curl  && \
    apk add --no-cache openldap-clients zsh git freetype

# I like a nice shell in my contaners
RUN mkdir -p /root/.antigen
RUN curl -L git.io/antigen > /root/.antigen/antigen.zsh
COPY development/.zshrc /root/.zshrc
# Set up ZSH as (we just need to start it, it'll initialise our setup itself)
RUN /bin/zsh /root/.zshrc


WORKDIR /source
# Copy in the source code ans install poetry
COPY . /source
RUN curl -sSL https://install.python-poetry.org | python3 -
# install the dependencies
RUN poetry install --no-interaction --no-ansi

# Now clean up the image by remving the gcc/package build dependencies
RUN apk del .build-deps
COPY development/adr_config.py /source/adr_config.py