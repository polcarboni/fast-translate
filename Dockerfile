FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get-install -y \


COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "cli.py"]
