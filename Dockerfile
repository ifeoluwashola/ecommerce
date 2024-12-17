FROM python:3-alpine AS builder

WORKDIR /app

RUN apk add --no-cache gcc libffi-dev musl-dev py3-virtualenv

COPY requirements.txt . 

RUN python -m venv venv && \
    venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3-alpine

WORKDIR /app

RUN apk add --no-cache libffi && \
    addgroup -g 1000 appuser && \
    adduser -u 1000 -G appuser -h /home/appuser -D appuser

COPY --from=builder /app/venv /app/venv
COPY --chown=appuser:appuser api/ ./api/
COPY --chown=appuser:appuser main.py .
COPY .env .

USER appuser

EXPOSE 8000

CMD ["venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
