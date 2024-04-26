FROM --platform=amd64 python:3.11 as build

RUN apt-get update && apt-get install -y \
    build-essential gcc libffi-dev libpq-dev git curl

ENV VIRTUAL_ENV=/.venv PATH="/.venv/bin:$PATH"

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

COPY pyproject.toml pyproject.toml

RUN /root/.cargo/bin/uv venv /.venv && \
    /root/.cargo/bin/uv pip install -r pyproject.toml

FROM --platform=amd64 python:3.11-slim-bookworm

RUN adduser --disabled-password --gecos "" --no-create-home acc

COPY --from=build --chown=acc:acc /.venv /.venv

USER acc

CMD ["/.venv/bin/uvicorn", "uiengineer.main:app", "--host", "0.0.0.0"]
