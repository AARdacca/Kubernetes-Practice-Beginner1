FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY RapidCompetitions/requirements.txt .

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential zlib1g-dev libffi-dev libpq-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Django project and .env file
COPY RapidCompetitions /app
COPY .env /app/.env

# Set environment variable file for Django (if you use django-environ or similar)
ENV DJANGO_READ_DOT_ENV_FILE=true

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
