FROM shroominic/python-uv

COPY pyproject.toml pyproject.toml

RUN uv pip install -r pyproject.toml

COPY uiengineer /uiengineer

ENV PATH="/.venv/bin:$PATH"

CMD uvicorn uiengineer.main:app --host 0.0.0.0
