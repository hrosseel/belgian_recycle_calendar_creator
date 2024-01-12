FROM python:3.11.5-slim-bullseye

LABEL project="Belgian Recycle Calendar Creator"
LABEL author="Hannes Rosseel"

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]