FROM python:3.8

ARG name
ARG version
ARG maintainer

HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost:$port/ || exit 1

LABEL maintainer=$maintainer version=$version name=$name

EXPOSE $port
ENV FLASK_APP="application"

RUN apt-get update -y \
    && apt-get -y install apt-utils \
    && apt-get install -y pipenv

COPY Pipfile Pipfile.lock /build/
WORKDIR /build
RUN pipenv lock --requirements > requirements.txt \
    && rm Pipfil* \
    && pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD flask run --host $HOST --port $PORT

