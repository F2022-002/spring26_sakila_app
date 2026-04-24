FROM python:3.9.19-slim

LABEL maintainer="saimi" \
      version="1.0.0" \
      description="Optimized Flask Sakila application image"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

RUN useradd -m -u 10001 appuser && chown -R appuser:appuser /app
USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000', timeout=3)" || exit 1

CMD ["python", "app.py"]
