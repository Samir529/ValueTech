# with gunicorn

# Use official Python 3.13.7 slim image
FROM python:3.13.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create app directory
WORKDIR /app

# Install system dependencies (needed for Pillow, cryptography, psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    musl-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip to latest versions first
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Collect static files for WhiteNoise
RUN python manage.py collectstatic --noinput

# Expose the port Gunicorn will run on
# Expose default port (optional, Render provides $PORT)
EXPOSE 8000

# Start Gunicorn server using PORT env variable provided by Render
#CMD ["gunicorn", "ValueTech.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]

# Start Gunicorn server using PORT env variable provided by Render (shell form so $PORT is expanded)
CMD gunicorn ValueTech.wsgi:application --bind 0.0.0.0:$PORT --workers 4
