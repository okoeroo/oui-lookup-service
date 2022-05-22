# syntax=docker/dockerfile:1

FROM python:3.10-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ieee-oui-integrated.txt ieee-oui-integrated.txt
COPY config.ini config.ini
COPY oui_json_lookup.py oui_json_lookup.py

EXPOSE 8000

CMD ["/usr/local/bin/uvicorn","oui_json_lookup:app","--host", "0.0.0.0","--port", "8000","--reload"]
