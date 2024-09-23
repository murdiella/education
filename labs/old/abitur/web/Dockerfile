FROM python:3.9.1-buster as base
WORKDIR /usr/src
RUN apt -yq update
RUN apt -yq upgrade


FROM base as builder
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN python -m venv /venv
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin


FROM base as final
COPY --from=builder /venv /venv
RUN apt -yq update
COPY web/apps apps
COPY web/settings settings
COPY web/manage.py manage.py
COPY web/entrypoint.sh entrypoint.sh
COPY web/entrypoint.load_fixtures.sh entrypoint.load_fixtures.sh
RUN mkdir static
CMD ["/bin/sh", "entrypoint.sh"]
