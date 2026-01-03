FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Copy and set permissions for prestart script
COPY prestart.sh /app/prestart.sh
RUN chmod +x /app/prestart.sh

# Run migrations then start gunicorn (using sh instead of bash)
CMD ["/bin/sh", "-c", "/app/prestart.sh && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"]
