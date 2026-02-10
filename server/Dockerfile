FROM python:3.14-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

# Labels of the project
LABEL authors="yiconglisprojects"

# System dependencies
# RUN executes the command
# && is the logical AND operator
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# WORKDIR sets the work directory
WORKDIR = "/server"

# Install Python dependencies
# requirements.txt lists the dependencies the project will rely on
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy entire project
COPY . .

# Expose port
EXPOSE 8000

# Start gunicorn for deployment
CMD ["gunicorn", "server.wsgi:application", "--bind", "0:0:0:0:8000"]