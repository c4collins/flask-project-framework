FROM python:3.7

ARG name="Project Framework"
ARG version=0.1
ARG maintainer=connor@connomation.ca

LABEL maintainer=$maintainer version=$version name=$name

ENV HOST="0.0.0.0"
ENV PORT=5000
ENV FLASK_APP="application"

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

HEALTHCHECK CMD wget -q -O /dev/null http://0.0.0.0:$PORT/ || exit 1

COPY ./.env /app/.env
COPY ./settings/ /app/settings/
COPY ./application/ /app/application/

CMD flask run --host $HOST --port $PORT

