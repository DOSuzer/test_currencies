FROM python:3.10

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./currency/ .

EXPOSE 8000
