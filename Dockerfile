FROM python:3.14

COPY --from=ghcr.io/astral-sh/uv:0.12.21 /uv /uvx /usr/local/bin/

# Add, and run as, non-root user.
RUN mkdir /src
RUN adduser --disabled-password --gecos "" --shell /bin/bash mitodl

# Install Python packages
ENV  \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy \
  UV_PYTHON_DOWNLOADS=never \
  UV_PROJECT_ENVIRONMENT="/opt/venv" \
  VIRTUAL_ENV="/opt/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY pyproject.toml uv.lock /src/
RUN chown -R mitodl:mitodl /src
RUN mkdir ${VIRTUAL_ENV} && chown -R mitodl:mitodl ${VIRTUAL_ENV}

USER mitodl
WORKDIR /src
RUN uv venv --relocatable ${VIRTUAL_ENV}
RUN uv sync --locked --no-dev --no-install-project

# Add project
USER root
COPY . /src
WORKDIR /src
RUN chown -R mitodl:mitodl /src

RUN apt-get clean && apt-get purge

USER mitodl
RUN uv sync --locked --no-dev
