FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/
COPY models.py /app/
COPY database_file.py /app/
COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["/app/wait-for-it.sh", "db", "--", "python", "app.py"]
