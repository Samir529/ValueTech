# Use Python 3.11 slim/base image
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for common Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libzmq3-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, wheel to latest versions first (important for pyzmq, cryptography, etc.)
RUN python -m pip install --upgrade pip setuptools wheel

# Copy only requirements first for Docker caching
COPY requirements.txt .

# Install Python dependencies (prefer binary wheels to avoid source builds)
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port for Django
EXPOSE 8000

# Default command for Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
