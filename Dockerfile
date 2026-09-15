FROM python:3.12-slim

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app.py .

USER 10001:10001
EXPOSE 8000
CMD ["python", "app.py", "--host", "0.0.0.0"]
