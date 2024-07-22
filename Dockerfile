FROM python:3.12-slim

WORKDIR /app

COPY . /app/
RUN apt-get update && apt-get install -y curl && apt-get clean
RUN pip install -r requirements.txt

CMD python src/bot.py