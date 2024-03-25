FROM python:3.11-slim

# install git
RUN apt update && \
  apt install -y git
RUN apt clean

# install pipenv
RUN pip install --upgrade pip && \
  pip install pipenv

WORKDIR /workspace

# install dependencies
COPY Pipfile ./
RUN pipenv install --dev
