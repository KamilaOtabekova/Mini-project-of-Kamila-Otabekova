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
        # Retrieve the term selected by the user
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
