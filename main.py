from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

mydb = mysql.connector.connect(
    host="13.233.161.181",
    user="root",
    password="1234",
    database="mydb"
)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/students')
def students():
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM students")
        students = mycursor.fetchall()
        return render_template('student.html', students=students)
    except mysql.connector.Error as error:
        app.logger.error(f"Error fetching students: {error}")
        return "Internal Server Error", 500


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        major = request.form['major']
        year = request.form['year']
        marks = request.form['marks']
        mycursor = mydb.cursor()
        sql = "INSERT INTO students (name, age, gender, major, year, marks) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, age, gender, major, year, marks)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            flash('Student added successfully!', 'success')
            return redirect('/add_student')
        except mysql.connector.Error as error:
            flash(f"Error adding student: {error}", 'error')
            return redirect('/add_student')
    else:
        return render_template('add_student.html')


if __name__ == '__main__':
    app.run(port=5000)
