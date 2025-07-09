FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean

# Set work directory
WORKDIR /app

# Copy requirement file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Run server
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean

# Set work directory
WORKDIR /app

# Copy requirement file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Run server
CMD ["gunicorn", "job_portal.wsgi:application", "--bind", "0.0.0.0:8000"]
