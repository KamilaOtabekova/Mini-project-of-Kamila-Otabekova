
# *Mini-project-of-Kamila-Otabekova*

The purpose of this project to create a web page which will display my Webster university schedule by choosing Fall and Spring terms by using docker, python and html.

***Steps followed to create.***

## 1. *I installed as was required Docker and started PostgreSQL session in terminal:*

***Then I pulled the latest PostgreSQL Docker image using following command:***

```bash
docker pull postgres:latest
```

***After that I created a docker container for the PostgreSQL database using my name as database name by:***

```bash
docker run --name kamilaschedule-db -e POSTGRES_USER=kamila -e POSTGRES_PASSWORD=kamila_pass -d -p 5432:5432 postgres:latest
```

***Then I verified that the container is running by:***

```bash
docker ps
```

***Using following command I gained access to my running PostgreSQL container by:***

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

***Verification of creation table by:***
```sql
select * from WebsterSchedule;
```

***Webster's Schedule data insertion to it's table:***

```sql

INSERT INTO WebsterSchedule (crs_sec, hrs, title, instructor, campus, building, room, days, time, date_range, term, type) VALUES
('COSC 2110 3T', 3.0, 'Computer Languages', 'Sanjar Bekov', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '115 ', '--T----', '02:00p-04:20p', '08/19/2024 12/13/2024', 'Fall', 'Lecture'),
('COSC 2610 2T', 3.0, 'Operating Systems', 'Sokhibjamol Boeva', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '114 ', '--T----', '04:30p-06:50p', '08/19/2024 12/13/2024', 'Fall', 'Lecture'),
('COSC 3410 1T', 3.0, 'Computer and Information Security', 'Islombek Isroilov', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '108 ', '----R---', '04:30p 06:50p', '08/19/2024 12/13/2024', 'Fall', 'Lecture'),
('INTL 1500 1U', 3.0, 'The World System Since 1500', 'Badarch', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '409 ', '--M----', '11:30a-01:50p', '08/19/2024 12/13/2024', 'Fall', 'Lecture'),
('SUST 1000 1U', 3.0, 'Introduction to Sustanability', 'Mokhistara Mukhammadyunusova', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '108 ', '----R---', '02:00p 04:20p', '08/19/2024 12/13/2024', 'Fall', 'Lecture'),
('EDEX 3001 3S', 1.0, 'Chess for Beginners', 'Jonathan Singler', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', 'Web+', '---W----', '07:00p 08:30p', '08/19/2024 10/11/2024', 'Spring', 'WebNet+'),
('COSC 2810 3T', 3.0, 'Systems Analysis and Design', 'Artikov', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '115 ', '-M-----', '03:30p 06:20p', '01/15/2024 05/10/2024', 'Spring', 'Lecture'),
('COSC 1570 2T', 3.0, 'Mathematics for Computer', 'Nacional', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '307 ', '-M-----', '12:30p 03:20p', '01/15/2024 05/10/2024', 'Spring', 'Lecture'),
('POLT 1070 3U', 3.0, 'Introduction to Political', 'Sonila', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '229 ', '----R--', '12:30p 03:20p', '01/15/2024 05/10/2024', 'Spring', 'Lecture'),
('INTL 1050 2U', 3.0, 'Introduction to INTL', 'Yuldasheva', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '110 ', '----R--', '09:30a 12:20p', '01/15/2024 05/10/2024', 'Spring', 'Lecture');

```
***Verification of insertion in table by:***
```sql
select * from WebsterSchedule;
```
## 2.1 *After creation we should leave container by:*
```sql
\q
```
## 3. *Installation of Python and Flask Dependencies*

***To create and activate virtual environment I used:***

```python
python -m venv venv
```
```sql
venv\Scripts\activate
```

***Installation of Flask and pg8000 for database connection by:***

```bash
pip install flask pg8000
```

## 4. *Creation of Flask Application - app.py*

```python
from flask import Flask, render_template, request, redirect, url_for
import pg8000

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def entry():
    if request.method == "POST":
        user_name = request.form["name"]
        return redirect(url_for("index", name=user_name))
    return render_template("entry.html")

@app.route("/index/<name>", methods=["GET", "POST"])
def index(name):
    if request.method == "POST":
       
        term = request.form["term"]
        return redirect(url_for("timetable", term=term))

    return render_template("index.html", name=name)

@app.route("/timetable", methods=["GET"])
def timetable():
    term = request.args.get('term')
    if not term:
        return "term not provided", 400

    conn = pg8000.connect(
        user="kamila",
        password="kamila_pass",
        host="localhost", 
        port=5432, 
        database="postgres"
    )

    cur = conn.cursor()
    query = "SELECT * FROM WebsterSchedule WHERE term = %s;"
    cur.execute(query, (term,))
    rows = cur.fetchall()

    if rows:
        return render_template("timetable.html", term=term, data=rows, message="")
    else:
        return render_template("timetable.html", term=term, data=[], message="No data found for this term.")


if __name__ == "__main__":
    app.run(debug=True)
```

## 5. *HTML created codes for Flask App*

***entry.html***

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=2.0">
  <title>Welcome to Webster University</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body class="entry-page">
  <main>
    <h1>Welcome to Webster Schedule!</h1>
    <form method="POST">
      <label for="name">Hi! What is your name?</label>
      <input type="text" id="name" name="name" required placeholder="Enter your name">
      <button type="submit">Submit</button>
    </form>
  </main>
</body>
</html>

```
***index.html***

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Webster University Schedule</title>
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
      <h1>Webster University Student Schedule</h1>
      <h2>{{name}}, choose your term!</h2>
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

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Student's Schedule for Term {{ term }}</title>
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
      <h1>Student's, Schedule for term: {{ term }}</h1>
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
            <td>{{ row[0] }}</td> 
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td> 
            <td>{{ row[3] }}</td>
            <td>{{ row[4] }}</td> 
            <td>{{ row[5] }}</td>
            <td>{{ row[6] }}</td>
            <td>{{ row[7] }}</td> 
            <td>{{ row[8] }}</td> 
            <td>{{ row[9] }}</td>
            <td>{{ row[10] }}</td> 
            <td>{{ row[11] }}</td> 
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
## 5.1. *Then we should locate these entry, index and timetable html codes in file named:*

```sql

templates

```
## 6. *Usage of CSS for styles*

***styles.css***

```css
body.entry-page {
  display: grid;
  justify-items: center;
  align-items: center;
  height: 100vh;
  background-color: #2b303a;
  background-image: url('footer-image-webster-1600x1114_2.jpg');
  background-size: cover;
  background-position: center center;
  background-attachment: fixed;
  margin: 0;
  padding: 0;
}

body.entry-page main {
  display: grid;
  gap: 10px;
  width: 100%;
  max-width: 400px;
  padding: 32px;
  background: #232738;
  border-radius: 10px;
  text-align: center;
}

body.entry-page h1 {
  font-family: "Montserrat", serif;
  font-size: 36px;
  font-weight: 600;
  color: #d64933;
  margin-bottom: 20px;
  text-align: center;
}

body.entry-page input[type="text"] {
  width: 90%;
  height: 50px;
  padding: 0 16px;
  font-size: 18px;
  border-radius: 8px;
  border: 1px solid #d64933;
  color:  #32394f;
  background-color: #eee5e9;
  transition: border 0.3s ease;
}

body.entry-page input[type="text"]:focus {
  border-color: #32394f;
  outline: #d64933;
}

body.entry-page button {
  width: 100%;
  height: 48px;
  background: #d64933;
  color: #2b303a;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #d64933;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

body.entry-page button:hover {
  background-color: #32394f;
  border: 1px solid #d64933;
}

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
## 6.1. *Locate code in file named:*
```sql
static
```
## 7. *Run Flask Application*

***Location to my direction of app.py in file named: final by:***

```sql
cd "C:\Users\hpenv\Desktop\final"
```
***After locate, run app.py by:***
```python
python app.py
```
## 8. *(optional) If you want to stop container, use:*

```sql
docker stop kamilaschedule-db
```
