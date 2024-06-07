FROM python:3.10-slim

COPY --chown=1000:1000 . /day_counts

ARG counts_USER="counts_user"
ARG counts_GROUP="counts_user"
ARG HOME_DIR="/home/${counts_USER}"
ARG UID=1000
ARG GID=1000
ENV counts_USER=${counts_USER}
ENV HOME_DIR=${HOME_DIR}

RUN apt-get update
RUN apt-get upgrade -y
RUN pip install --upgrade pip poetry
WORKDIR "/day_counts"
RUN poetry install --no-interaction --no-ansi 

ENTRYPOINT [ "poetry", "run" ] 