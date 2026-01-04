FROM python:3.14-slim AS builder

ARG VERSION=1.0
ENV APP_HOME=/app \
    PYTHONUNBUFFERED=1

WORKDIR ${APP_HOME}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/health

ENTRYPOINT ["python"]
CMD ["app.py"]