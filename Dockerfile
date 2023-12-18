FROM python:3.11-alpine3.19

ENV APP /dz4web

WORKDIR  $APP

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000 3000

ENTRYPOINT [ "python", "main.py"]

