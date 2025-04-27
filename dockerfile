# Dockerfile
FROM python:3.9-slim

# Set timezone to IST
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the init.sql file into the container
COPY docker-entrypoint-initdb.d/init.sql /app/init.sql

# Copy the rest of the application code
COPY . .

# Ensure Flask logs are printed to the terminal
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Command to run the application
CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 app:app"]