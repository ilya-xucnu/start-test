FROM python:3.9.21-alpine3.21

RUN adduser -D appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

WORKDIR /app 

COPY --chown=appuser:appuser requirements.txt .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY --chown=appuser:appuser . .
USER appuser 
ENV PYTHONUNBUFFERED=1 

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "--timeout=30", "--log-level=info", "app:app"]
