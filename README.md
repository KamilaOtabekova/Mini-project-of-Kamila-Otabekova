
# Mini-project-of-Kamila-Otabekova

The purpose of this project to create a web application which will display Webster University's student schedule in timetable type using docker, python and html.

**Steps followed to create.**

### 1. I installed as was required Docker and started PostgreSQL session in terminal:

```
#Then I pulled the latest PostgreSQL Docker image using following command:

docker pull postgres:latest

# After that I created a docker container for the PostgreSQL database:

docker run --name university-db -e POSTGRES_USER=student -e POSTGRES_PASSWORD=student_pass -d -p 5432:5432 postgres:latest

# Then I verified that the container is running:

docker ps

# Using following command I gained access to my running PostgreSQL container:

docker exec -it university-db psql -U student

```
## 2. Then I set up the PostgreSQL Database as was asked and tables

Inside the container I connected to the PostgreSQL database through command:
```
psql -U student
```
