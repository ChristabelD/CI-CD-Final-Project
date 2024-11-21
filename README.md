# Django Application with DevOps Practices

This project is a simple To-Do API built with Django, PostgreSQL, Docker, Nginx, and GitHub Actions for continuous integration and deployment. The application features user authentication, data persistence, and email notifications. It is containerized using Docker, deployed using Ansible, and includes a CI pipeline that builds and tests the application on every push to the repository.

## Learning Objectives

- Gain practical experience with Docker containerization, including multi-service applications.
- Understand the principles of Continuous Integration (CI) and Continuous Deployment (CD).
- Learn to use GitHub Actions for automated build and testing workflows.
- Develop skills in Ansible for configuration management and application deployment.
- Implement a basic web application with a database backend and email functionality.

## Project Setup

1. **Create a Django Project:**
   The Django project is a To-Do API that includes:
   - **User Authentication**: Users can register and log in to manage their tasks.
   - **Data Persistence**: Uses PostgreSQL to store task data.
   - **Email Notifications**: Sends email notifications using MailHog (for testing purposes) or SendGrid in production.

2. **Dockerization:**
   - **Django Application**: Runs with Gunicorn (WSGI server) inside a container.
   - **PostgreSQL Database**: Containerized PostgreSQL database for data persistence.
   - **Nginx**: Acts as a reverse proxy to serve the Django application.
   - **Email Server**: Uses MailHog (for development) or SendGrid (for production).

3. **Docker Compose**:
   - A `docker-compose.yml` file is used to orchestrate the services. It ensures proper networking between containers and port management.

4. **Ports**:
   - Unique ports are used for each service to avoid conflicts.
   - Django: Exposed on port `8000` inside the container.
   - Nginx: Exposed on port `80` inside the container and mapped to an external port.
   - PostgreSQL: Exposed on port `5432` inside the container.
   - MailHog: Exposed on port `8025` inside the container.

## GitHub Actions CI Pipeline

The CI pipeline is set up using GitHub Actions:

1. **Code Quality Check (Linting)**: Ensures that the code adheres to defined standards.
2. **Build Docker Images**: Each push to the repository triggers the building of Docker images for the Django application, PostgreSQL, Nginx, and MailHog.
3. **Run Tests**: Runs unit and integration tests in the CI environment to ensure the integrity of the code.
4. **Push to Docker Hub**: If the build and tests pass, the Docker images are pushed to Docker Hub for deployment.

GitHub Actions workflow is defined in the `.github/workflows/main.yml` file.

## Ansible Deployment

Ansible is used to automate the deployment process on a remote server. The Ansible playbook includes the following tasks:

- Pull the latest Docker images from Docker Hub.
- Configure the target server with the necessary username and password.
- Run the application using `docker-compose up -d` to start the services.

### Steps to deploy with Ansible:
1. Clone the repository to the target server.
2. Install necessary dependencies (Docker, Docker Compose, Ansible).
3. Run the Ansible playbook to deploy the Dockerized application.

The Ansible playbook is located in the `ansible/` directory of the project.

## Deployment Target

The application is intended to be deployed to a shared server, and access to the server will be provided through SSH credentials. The target server will have the following IP address:

- **Server IP Address**: `104.248.241.153`
- **Username & Password**: Your name (e.g., `christabeladams`).

## Prerequisites

Before you begin, make sure you have the following installed:

- **Docker**: For containerizing the application.
- **Docker Compose**: For orchestrating the services.
- **GitHub Account**: For pushing Docker images to Docker Hub and setting up CI/CD workflows.
- **Ansible**: For automating the deployment process.
- **MailHog or SendGrid**: For email functionality.

## Setting Up Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/django-devops-project.git
   cd django-devops-project
Set up the environment:

Create a .env file to store environment variables like database credentials, secret keys, etc.
Ensure your PostgreSQL database and MailHog (or SendGrid) credentials are correctly set up in the .env file.
Build the Docker containers:

bash
Copy code
docker-compose up --build
Access the application:

Django app is available at http://localhost:8000.
Nginx will reverse proxy requests to the Django app, exposed at http://localhost.
CI/CD with GitHub Actions
Once you push changes to your GitHub repository, GitHub Actions will automatically run the CI pipeline. The pipeline will:

Lint the code.
Build the Docker images.
Run the tests.
Push the Docker images to Docker Hub.
Example of GitHub Actions Workflow (.github/workflows/main.yml):
yaml
Copy code
name: CI Pipeline

on:
  push:
    branches:
      - main

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run linting
        run: |
          flake8 .

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Docker
        uses: docker/setup-buildx-action@v2
      - name: Build Docker Images
        run: |
          docker-compose build

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          docker-compose run --rm web pytest

  push:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v2
      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Push Docker Images
        run: |
          docker-compose push
Ansible Playbook Example
yaml
Copy code
- hosts: all
  become: yes
  tasks:
    - name: Pull latest Docker images from Docker Hub
      docker_image:
        name: "{{ item }}"
        source: pull
      loop:
        - todo-django
        - todo-nginx
        - postgres
        - mailhog

    - name: Start the application using docker-compose
      command: docker-compose up -d
      args:
        chdir: /path/to/project
Conclusion
By following the steps outlined in this README, you'll gain hands-on experience with Docker, CI/CD pipelines, Ansible automation, and deploying a production-grade Django application. This project combines development, DevOps, and cloud deployment skills to create a robust web application.
