FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get-install -y \
 #check and finish implementation

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "cli.py"]
