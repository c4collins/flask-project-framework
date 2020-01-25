FROM python:3.8

ARG name="Project Framework"
ARG FLASK_ENV=development
ARG PORT=5000
ARG HOST=0.0.0.0
ARG version=0.1
ARG maintainer="connor@connomation.ca"

HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost:$port/ || exit 1

LABEL maintainer=$maintainer version=$version

EXPOSE $port
ENV FLASK_ENV=$FLASK_ENV
ENV FLASK_APP=application
ENV PORT=$PORT

RUN apt-get update -y \
    && apt-get -y install apt-utils \
    && apt-get install -y pipenv

COPY Pipfile Pipfile.lock /app/

WORKDIR /app

RUN pipenv install
RUN pipenv shell

COPY . /app

CMD ["flask", "run", "--host=$HOST", "--port=$PORT"]