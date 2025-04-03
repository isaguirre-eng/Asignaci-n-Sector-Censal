from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB = "registros.db"

def init_db():
    if not os.path.exists(DB):
        with sqlite3.connect(DB) as conn:
            conn.execute(
                "CREATE TABLE registros (sector TEXT, nombre TEXT, dui TEXT, x REAL, y REAL)"
            )

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sector = request.form["sector"]
        nombre = request.form["nombre"]
        dui = request.form["dui"]
        x = request.form["x"]
        y = request.form["y"]
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO registros VALUES (?, ?, ?, ?, ?)", (sector, nombre, dui, x, y))
        return redirect("/")

    with sqlite3.connect(DB) as conn:
        registros = conn.execute("SELECT * FROM registros").fetchall()

    return render_template("index.html", registros=registros)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)