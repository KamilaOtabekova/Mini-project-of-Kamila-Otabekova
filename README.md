
# Mini-project-of-Kamila-Otabekova

The purpose of this project to create a web application which will display Webster University's student schedule in timetable type using docker, python and html.

**Steps followed to create.**

### 1. I installed as was required Docker and started PostgreSQL session in terminal:

```
# Then I pulled the latest PostgreSQL Docker image using following command:

docker pull postgres:latest

# After that I created a docker container for the PostgreSQL database:

docker run --name websterschedule-db -e POSTGRES_USER=student -e POSTGRES_PASSWORD=student_pass -d -p 5432:5432 postgres:latest

# Then I verified that the container is running:

docker ps

# Using following command I gained access to my running PostgreSQL container:

docker exec -it websterschedule-db psql -U studentschedule

```
## 2. Then I set up the PostgreSQL Database as was asked and tables

Inside the container I connected to the PostgreSQL database through command:
```
psql -U student
```
--- Creation of Student Schedule ---
```
CREATE TABLE StudentSchedule (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(255),
    instructor VARCHAR(255),
    campus VARCHAR(255),
    building VARCHAR(255),
    room VARCHAR(50),
    days VARCHAR(50),
    time VARCHAR(50),
    date_range VARCHAR(50),
    ADD COLUMN semester VARCHAR(50);
);
```
--- Insert data to table---
```
INSERT INTO Timetable (course_name, instructor, campus, building, room, days, time, date_range, level, semester) VALUES
('Computer Languages', 'Bekov, San', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '115', '--T----', '02:00p 04:20p', '08/19/2024 12/13/2024', 1, 'Fall'),
('Operating Systems', 'Boeva, Sok', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '114', '--T----', '04:30p 06:50p', '08/19/2024 12/13/2024', 1, 'Fall'),
('Computer and Information', 'Isroilov', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '114', '--R----', '04:30p 06:50p', '08/19/2024 12/13/2024', 1, 'Fall'),
('The World System Since 1500', 'Badarch', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '409', '--M----', '11:30a 01:50p', '08/19/2024 12/13/2024', 2, 'Fall'),
('Introduction to Sustainability', 'Mukhammady', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '108', '--R----', '02:00p 04:20p', '08/19/2024 12/13/2024', 2, 'Fall'),
('Chess for Beginners', 'Singler, J', 'Webster Univ Tashkent, Uzbekistan', 'WebNet+', 'N/A', '--W----', '07:00p 08:30p', '08/19/2024 10/11/2024', 3, 'Fall'),
('Computer Networks', 'Smith, J', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '103', '--M----', '09:00a 11:00a', '01/15/2025 05/15/2025', 1, 'Spring'),
('Artificial Intelligence', 'Doe, J', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '105', '--T----', '12:00p 02:00p', '01/15/2025 05/15/2025', 2, 'Spring'),
('Database Design', 'Ali, S', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '107', '--R----', '03:00p 05:00p', '01/15/2025 05/15/2025', 2, 'Spring'),
('Global Politics', 'Lee, A', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '202', '--W----', '10:00a 12:00p', '01/15/2025 05/15/2025', 3, 'Spring'),
('Machine Learning', 'Khuzhaev, M', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '109', '--T----', '01:30p 03:30p', '01/15/2025 05/15/2025', 3, 'Spring');

```
