FROM python:3.12-slim

WORKDIR /app

COPY . /app/
RUN apt-get update && apt-get install -y curl && apt-get clean
RUN python3 -m venv .venv
RUN source ./.venv/bin/activate
RUN pip install -r requirements.txt

CMD python src/bot.py