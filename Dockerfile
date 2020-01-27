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

COPY ./migrations/ /app/migrations/
COPY ./application/ /app/application/
RUN flask db migrate

HEALTHCHECK CMD wget -q -O /dev/null http://0.0.0.0:$PORT/ || exit 1

CMD flask run --host $HOST --port $PORT

