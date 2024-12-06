# Mini-project-of-Kamila-Otabekova

The purpose of this project to create a web application which will display Webster University's student schedule in timetable type using docker, python and html.

Steps followed to create.
-------------------------
1. I installed as was required Docker and started PostgreSQL session in terminal:

# Pull the latest PostgreSQL Docker image
docker pull postgres:latest

# Create a Docker container for the PostgreSQL database
docker run --name university-db -e POSTGRES_USER=student -e POSTGRES_PASSWORD=student_pass -d -p 5432:5432 postgres:latest

# Verify the container is running
docker ps

# Access the running PostgreSQL container
docker exec -it university-db psql -U student


