FROM python:3.9.1-buster
WORKDIR /usr/src
RUN apt -yq update
RUN apt -yq upgrade
RUN apt install -yq keyrings.alt
RUN pip install poetry
COPY pyproject.toml poetry.lock .behaverc ./
RUN python -m venv /venv
RUN poetry install -vv
COPY tests tests
CMD ["poetry", "run", "behave"]
