# Use an official Node runtime as a parent image for building the frontend
FROM node:14 AS frontend

# Set the working directory
WORKDIR /app

# Copy the frontend code
COPY frontend/package*.json ./
COPY frontend/ ./

# Install dependencies and build the frontend
RUN npm install
RUN npm run build

# Use an official Python runtime as a parent image for the backend
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the backend code
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend build output to the Django static files directory
COPY --from=frontend /app/build /app/static

# Copy the rest of the backend code
COPY backend/ /app/

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["gunicorn", "ecotrack.wsgi:application", "--bind", "0.0.0.0:8000"]
