FROM ghcr.io/astral-sh/uv:alpine

# ---- Python 3.10 via uv ----
RUN uv python install 3.10 && uv python list

WORKDIR /app
RUN mkdir -p /app/checkpoint /app/dataset /app/result /app/src

# uv-env
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH="/opt/venv/bin:/usr/local/bin:${PATH}"

# Dependences
COPY pyproject.toml /app/pyproject.toml
COPY config.yml      /app/config.yml

RUN uv venv -p 3.10 \
 && uv sync --no-dev

# source
COPY ./src /app

ENTRYPOINT ["/opt/venv/bin/python"]
CMD ["/app/main.py"]
