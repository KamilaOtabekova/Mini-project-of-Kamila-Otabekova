
# *Mini-project-of-Kamila-Otabekova*

The purpose of this project to create a web application which will display Webster University's student schedule by using docker, python and html.

****Steps followed to create.****

## 1. **I installed as was required Docker and started PostgreSQL session in terminal:**

***Then I pulled the latest PostgreSQL Docker image using following command:***

```bash
docker pull postgres:latest
```

***After that I created a docker container for the PostgreSQL database using my name as database name:***

```bash
docker run --name kamilaschedule-db -e POSTGRES_USER=kamila -e POSTGRES_PASSWORD=kamila_pass -d -p 5432:5432 postgres:latest
```

***Then I verified that the container is running:***

```bash
docker ps
```

***Using following command I gained access to my running PostgreSQL container:***

```bash
docker exec -it kamilaschedule-db psql -U kamila
```

## 2. *Then I set up the PostgreSQL Database as was asked and tables*

***Inside the container I connected to the PostgreSQL database through command:***

```bash
\c postgres
```
***Creation of Webster Schedule:***

```sql

CREATE TABLE WebsterSchedule (
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
    term VARCHAR(10),
    type VARCHAR(50)
);

```

***Webster's Schedule data insertion to it's table:***

```sql

INSERT INTO WebsterSchedule (crs_sec, hrs, title, instructor, campus, building, room, days, time, date_range, term, type) VALUES
('COSC 2110 3T', 3.0, 'Computer Languages', 'Sanjar Bekov', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '115 ', '--T----', '02:00p-04:20p', '08/19/2024 12/13/2024', 'Fall', 'Lecture'),
('COSC 2610 2T', 3.0, 'Operating Systems', 'Sokhibjamol Boeva', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '114 ', '--T----', '04:30p-06:50p', '08/19/2024 12/13/2024', 'Fall', 'Lecture'),
('COSC 3410 1T', 3.0, 'Computer and Information Security', 'Islombek Isroilov', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '108 ', '----R---', '04:30p 06:50p', '08/19/2024 12/13/2024', 'Fall', 'Lecture'),
('INTL 1500 1U', 3.0, 'The World System Since 1500', 'Badarch', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '409 ', '--M----', '11:30a-01:50p', '08/19/2024 12/13/2024', 'Fall', 'Lecture'),
('SUST 1000 1U', 3.0, 'Introduction to Sustanability', 'Mokhistara Mukhammadyunusova', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '108 ', '----R---', '02:00p 04:20p', '08/19/2024 12/13/2024', 'Fall', 'Lecture'),
('EDEX 3001 3S', 1.0, 'Chess for Beginners', 'Jonathan Singler', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '    ', '---W----', '07:00p 08:30p', '08/19/2024 10/11/2024', 'Spring', 'WebNet+'),
('COSC 2810 3T', 3.0, 'Systems Analysis and Design', 'Artikov', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '115 ', '-M-----', '03:30p 06:20p', '01/15/2024 05/10/2024', 'Spring', 'Lecture'),
('COSC 1570 2T', 3.0, 'Mathematics for Computer', 'Nacional', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '307 ', '-M-----', '12:30p 03:20p', '01/15/2024 05/10/2024', 'Spring', 'Lecture'),
('POLT 1070 3U', 3.0, 'Introduction to Political', 'Sonila', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '229 ', '----R--', '12:30p 03:20p', '01/15/2024 05/10/2024', 'Spring', 'Lecture'),
('INTL 1050 2U', 3.0, 'Introduction ', 'Yuldasheva INTL', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '110 ', '----R--', '09:30a 12:20p', '01/15/2024 05/10/2024', 'Spring', 'Lecture');

```
## 3. *Installion of Python and Flask Dependencies*

***To create and activate virtual environment I used:***

```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```

***Install Flask and pg8000 for database connection***

```bash
pip install flask pg8000
```
\q

## 4. *Creation of Flask Application - app.py*

```python

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

## 5. *HTML Templates for Flask*

***Index.html***

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>University Timetable</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='styles.css') }}"
    />
  </head>
  <body>
    <main>
      <h1>University Timetable</h1>

      <form action="/timetable" method="GET">
        <label for="term">Select term:</label>
        <select name="term" id="term">
          <option value="Spring">Spring</option>
          <option value="Fall">Fall</option>
        </select>
        <button type="submit">Submit</button>
      </form>
    </main>
  </body>
</html>

```
***timetable.html***

```

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Kamila's Schedule for Term {{ term }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='styles.css') }}"
    />
  </head>
  <body>
    <main>
      <h1>Kamila's Schedule for term: {{ term }}</h1>
      {% if data %}
      <table border="0">
        <thead>
          <tr>
            <th>Course ID</th>
            <th>Hours</th>
            <th>Name</th>
            <th>Instructor</th>
            <th>Campus</th>
            <th>Building</th>
            <th>Room</th>
            <th>Days</th>
            <th>Time</th>
            <th>Date</th>
            <th>Terms</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          {% for row in data %}
          <tr>
            <td>{{ row[0] }}</td> #Course ID
            <td>{{ row[1] }}</td> #Hours
            <td>{{ row[2] }}</td> #Name
            <td>{{ row[3] }}</td> #Prof
            <td>{{ row[4] }}</td> #Campus
            <td>{{ row[5] }}</td> #Building
            <td>{{ row[6] }}</td> #Room
            <td>{{ row[7] }}</td> #Days
            <td>{{ row[8] }}</td> #Time
            <td>{{ row[9] }}</td> #Date
            <td>{{ row[10] }}</td> #Term
            <td>{{ row[11] }}</td> #Type
          </tr>
          {% endfor %}
        </tbody>
      </table>
      {% else %}
      <p>{{ message }}</p>
      {% endif %}

      <a href="/">Go back</a>
    </main>
  </body>
</html>

```
## 5.1. *Then we should locate these two html codes in file named:*

```sql

templates

```
## 6. *Usage of CSS for styles*

```css
* {
  left: 0;
  top: 0;
  margin: 0;
  padding: 0;
  color: var(--text);
  font-family: "Montserrat", serif;
  font-optical-sizing: auto;
  font-weight: 500;
  font-style: normal;
  transition: 0.3s ease;
}

body {
  display: grid;
  width: 100%;
  height: 100%;
  justify-items: center;
  background-color: var(--bg);

  --bg: #2b303a;
  --secondary: #232736;
  --text: #eee5e9;
  --primary: #d64933;
  --stroke: #32394f;
  --destructive: #d64933;
}

main {
  display: grid;
  gap: 24px;
  grid-auto-rows: max-content;
  width: 100%;
  max-width: 1440px;
  padding: 32px;
}

h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary);
}

form {
  display: grid;
  gap: 16px;
  grid-auto-rows: max-content;
}

select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 100%;
  height: 48px;
  background-color: var(--secondary);
  padding-left: 24px;
  padding-right: 48px;
  background-image: url("data:image/svg+xml;utf8,<svg fill='white' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/><path d='M0 0h24v24H0z' fill='none'/></svg>");
  background-size: 24px;
  background-repeat: no-repeat;
  background-position: right 8px center;
  font-size: 16px;
  color: var(--text);
  border: 1px solid transparent;
  border-radius: 8px;
}

select:hover,
select:focus {
  border-color: var(--stroke);
  outline: none;
}

button,
a {
  width: 100%;
  height: 48px;
  background: var(--primary);
  color: var(--bg);
  font-size: 16px;
  border-radius: 8px;

  outline: none;
  border: 1px solid var(--primary);
}

button:hover,
a:hover {
  border: 1px solid var(--stroke);
}

a {
  display: flex;
  justify-content: center;
  align-items: center;
  text-decoration: none;
}

table {
  border-spacing: 0;
}

th,
td {
  height: 48px;
  padding: 0 16px;
  border: 1px solid var(--primary);
}

th {
  color: var(--primary);
}

table tr:first-child th:first-child {
  border-top-left-radius: 8px;
}
table tr:first-child th:last-child {
  border-top-right-radius: 8px;
}
table tr:last-child td:first-child {
  border-bottom-left-radius: 8px;
}
table tr:last-child td:last-child {
  border-bottom-right-radius: 8px;
}

```
```
```
## 6. *Run of Flask Application*

***Location to my direction of files:

```sql
cd "C:\Users\hpenv\Desktop\final"
```
```python
python app.py
```
## 7. *Accessing web browser*

**This link will appear:**
```bash
 http://127.0.0.1:5000/
```

## 8. *When we are finished, just stop container by:*

```sql
docker stop university-db
```
