# Use Python 3.10 or later
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the application on port 8000
EXPOSE 8000

# Run the application
CMD ["gunicorn", "todo.wsgi:application", "--bind", "0.0.0.0:8000"]

