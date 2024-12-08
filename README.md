
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

--- Creation of Student Schedule ---
```
student=# CREATE TABLE StudentSchedule (
    crs_sec VARCHAR(50),
    hrs FLOAT,
    title VARCHAR(255),
    instructor VARCHAR(255),
    campus VARCHAR(255),
    building VARCHAR(255),
    room VARCHAR(50),
    days VARCHAR(10),
    time VARCHAR(50),
    date_range VARCHAR(50),
    tm VARCHAR(10),
    type VARCHAR(50)
);
```
--- Insert data to table---
```
INSERT INTO StudentSchedule (crs_sec, hrs, title, instructor, campus, building, room, days, time, date_range, tm, type) VALUES
('COSC 2110 3T', 3.0, 'Computer Languages            ', 'Bekov, San         ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '115 ', '--T----', '02:00p 04:20p', '08/19/2024 12/13/2024', 'FA', 'Lecture  '),
('COSC 2610 2T', 3.0, 'Operating Systems            ', 'Boeva, Sok         ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '114 ', '--T----', '04:30p 06:50p', '08/19/2024 12/13/2024', 'FA', 'Lecture  '),
('COSC 3410 1T', 3.0, 'Computer and Information     ', 'Isroilov           ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '108 ', '----R---', '04:30p 06:50p', '08/19/2024 12/13/2024', 'FA', 'Lecture  '),
('INTL 1500 1U', 3.0, 'The World System Since 1500  ', 'Badarch            ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '409 ', '--M----', '11:30a 01:50p', '08/19/2024 12/13/2024', 'FA', 'Lecture  '),
('SUST 1000 1U', 3.0, 'Introduction to              ', 'Mukhammady         ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '108 ', '----R---', '02:00p 04:20p', '08/19/2024 12/13/2024', 'FA', 'Lecture  '),
('EDEX 3001 3S', 1.0, 'Chess for Beginners          ', 'Singler, J         ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '    ', '---W----', '07:00p 08:30p', '08/19/2024 10/11/2024', 'F1', 'WebNet+  '),
('COSC 2810 3T', 3.0, 'Systems Analysis and Design  ', 'Artikov, R         ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '115 ', '-M-----', '03:30p 06:20p', '01/15/2024 05/10/2024', 'SP', 'Lecture  '),
('COSC 1570 2T', 3.0, 'Mathematics for Computer     ', 'Nacional           ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '307 ', '-M-----', '12:30p 03:20p', '01/15/2024 05/10/2024', 'SP', 'Lecture  '),
('POLT 1070 3U', 3.0, 'Introduction to Political    ', 'Sonila, S.         ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '229 ', '----R--', '12:30p 03:20p', '01/15/2024 05/10/2024', 'SP', 'Lecture  '),
('INTL 1050 2U', 3.0, 'Introduction - WITHDRAWN -   ', 'Yuldasheva         ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '110 ', '----R--', '09:30a 12:20p', '01/15/2024 05/10/2024', 'SP', 'Lecture  '),
('SPCM 1040 4S', 3.0, 'Public Speaking              ', 'Shukurova          ', 'Webster Univ Tashkent, Uzbekistan                   ', 'North Hall Classrooms', '404 ', '---W---', '12:30p 03:20p', '01/15/2024 05/10/2024', 'SP', 'Lecture  ');


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

