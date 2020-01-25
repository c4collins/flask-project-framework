FROM python:3.8

ARG name="Project Framework"
ARG version=0.1
ARG maintainer=connor@connomation.ca

ENV HOST="0.0.0.0"
ENV PORT=5000
ENV FLASK_APP="application"

HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost:$port/ || exit 1

LABEL maintainer=$maintainer version=$version name=$name

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

CMD flask run --host $HOST --port $PORT

