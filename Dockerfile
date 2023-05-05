FROM python:3.11.2-slim as builder

RUN apt-get update && apt-get install -y build-essential python3-dev libpq-dev

WORKDIR /myapp
COPY . /myapp/

RUN pip install -r requirements.txt

CMD ["bash", "start.sh"]
