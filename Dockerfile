FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache gcc libffi-dev musl-dev py3-virtualenv && \
    addgroup -g 1000 appuser && \
    adduser -u 1000 -G appuser -h /home/appuser -D appuser && \
    chown -R appuser:appuser /app

USER appuser

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
