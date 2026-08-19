from flask import Flask, render_template, request, redirect
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL database configuration
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO students (name, email, course)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, email, course))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")


@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (student_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)