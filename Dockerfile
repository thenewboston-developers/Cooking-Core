# Use an official Python runtime as the base image
FROM python:3.10.4-buster

# Set the working directory in the container
WORKDIR /opt/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .
ENV COOKING_CORE_SETTING_IN_DOCKER true

RUN set -xe \
    && apt-get update \
    && apt-get install build-essential \
    && pip install pip==23.0 virtualenvwrapper poetry==1.3.2

COPY ["poetry.lock", "pyproject.toml", "./"]
RUN poetry run pip install pip==23.0

# We install dev dependencies to be able to run unittests inside the container
# TODO(dmu) LOW: Once Docker Hub supports stages builds move dev dependencies to the next stage
RUN poetry install --no-root

COPY ["README.md", "Makefile", "./"]
COPY cooking_core cooking_core

# Expose the Django development server port (adjust if needed)
EXPOSE 8000

#COPY scripts/dockerized-core-run.sh ./run.sh
#RUN chmod a+x run.sh

COPY ./scripts/dockerized-core-run.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

# Start the Django development server using Daphne
ENTRYPOINT ["/entrypoint.sh"]
