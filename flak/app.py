from flask import Flask, Blueprint, json, render_template, request, jsonify, redirect, url_for
from flask import render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Wake4ever'
app.config['MYSQL_DB'] = 'wake'

# Intialize MySQL
mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("index.html", name="welcome to wake")

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template("profile.html",msg=msg)
    


@app.route("/json")
def get_json():
    return jsonify({'name': 'tim', 'coolness': 10})

@app.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

@app.route("/go-to-home")
def go_to_home():
    return redirect(url_for("home"))

@app.route("/aboutUs")
def about_us():
    return render_template("aboutUs.html")

@app.route("/chart")
def chart():
    return render_template("chart.html")

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)