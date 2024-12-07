
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
    semester VARCHAR(50)
);
```
--- Insert data to table---
```
INSERT INTO StudentSchedule (course_name, instructor, campus, building, room, days, time, date_range, semester) VALUES
('Computer Languages', 'Bekov, San', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '115', '--T----', '02:00p 04:20p', '08/19/2024 12/13/2024', 'Fall'),
('Operating Systems', 'Boeva, Sok', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '114', '--T----', '04:30p 06:50p', '08/19/2024 12/13/2024', 'Fall'),
('Computer and Information', 'Isroilov', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '114', '--R----', '04:30p 06:50p', '08/19/2024 12/13/2024', 'Fall'),
('The World System Since 1500', 'Badarch', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '409', '--M----', '11:30a 01:50p', '08/19/2024 12/13/2024', 'Fall'),
('Introduction to Sustainability', 'Mukhammady', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '108', '--R----', '02:00p 04:20p', '08/19/2024 12/13/2024','Fall'),
('Chess for Beginners', 'Singler, J', 'Webster Univ Tashkent, Uzbekistan', 'WebNet+', 'N/A', '--W----', '07:00p 08:30p', '08/19/2024 10/11/2024', 'Fall'),
('Computer Networks', 'Smith, J', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '103', '--M----', '09:00a 11:00a', '01/15/2025 05/15/2025', 'Spring'),
('Artificial Intelligence', 'Doe, J', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '105', '--T----', '12:00p 02:00p', '01/15/2025 05/15/2025', 'Spring'),
('Database Design', 'Ali, S', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '107', '--R----', '03:00p 05:00p', '01/15/2025 05/15/2025','Spring'),
('Global Politics', 'Lee, A', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '202', '--W----', '10:00a 12:00p', '01/15/2025 05/15/2025', 'Spring'),
('Machine Learning', 'Khuzhaev, M', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '109', '--T----', '01:30p 03:30p', '01/15/2025 05/15/2025', 'Spring');

```
 ##Create Flask Application - app.py

```
import pg8000
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        semester = request.form["semester"]
        return render_template("timetable.html", semester=semester)

    return render_template("index.html")


@app.route("/timetable", methods=["GET"])
def timetable():
    semester = request.args.get("semester")

    if not semester:
        semester = request.form.get("semester")

    conn = pg8000.connect(user="student", password="student_pass", host="localhost", port=5432, database="postgres")
    cur = conn.cursor()

    query = "SELECT * FROM StudentSchedule WHERE semester = %s;"
    cur.execute(query, (semester,))
    rows = cur.fetchall()

    if rows:
        return render_template("timetable.html", semester=semester, data=rows, message="")
    else:
        return render_template("timetable.html", semester=semester, data=[], message="No data found for this semester.")


if __name__ == "__main__":
    app.run(debug=True)
```
## Index HTML
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>University Timetable</title>
</head>
<body>
    <h1>Welcome to the University Timetable</h1>
    <h2>Select a Semester to View the Schedule</h2>
    <form method="POST">
        <label for="semester">Choose Semester:</label>
        <select id="semester" name="semester" required>
            <option value="Fall">Fall</option>
            <option value="Spring">Spring</option>
        </select><br><br>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
```
##timetable html

```

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Schedule for Semester: {{ semester }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border: 1px solid #ccc;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        a {
            text-decoration: none;
            color: #007BFF;
        }
    </style>
</head>
<body>
    <h1>Student Schedule for Semester: {{ semester }}</h1>
    {% if data %}
    <table border="1">
        <thead>
            <tr>
                <th>Course Name</th>
                <th>Instructor</th>
                <th>Days</th>
                <th>Time</th>
                <th>Room</th>
            </tr>
        </thead>
        <tbody>
            {% for row in data %}
            <tr>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[6] }}</td>
                <td>{{ row[7] }}</td>
                <td>{{ row[8] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>{{ message }}</p>
    {% endif %}
    <br>
    <a href="/">Go Back</a>
</body>
</html>
```

