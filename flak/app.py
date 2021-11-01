from flask import Flask, Blueprint, json, render_template, request, jsonify, redirect, url_for
from flask import render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

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

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Nome' in request.form and 'password' in request.form:
        # Create variables for easy access
        Nome = request.form['Nome']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cliente WHERE Nome = %s AND password = %s', (Nome, password,))
        # Fetch one record and return result
        cliente = cursor.fetchone()
        # If account exists in accounts table in out database
        if cliente:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['Nome'] = cliente['Nome']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template("login.html",msg=msg)
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Nome' in request.form and 'password' in request.form and 'Email' in request.form:
        # Create variables for easy access
        Nome = request.form['Nome']
        password = request.form['password']
        Email = request.form['Email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cliente WHERE Nome = %s', (Nome,))
        cliente = cursor.fetchone()
        cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor2.execute('SELECT * FROM cliente WHERE Email = %s', (Email,))
        cliente2 = cursor2.fetchone()
        # If account exists show error and validation checks
        if cliente and cliente2:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', Nome):
            msg = 'Username must contain only characters and numbers!'
        elif not Nome or not password or not Email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            idCliente = cursor.execute('SELECT MAX(idCliente) FROM cliente')+1
            cursor.execute('INSERT INTO cliente VALUES (%s, %s, %s,NULL,NULL, %s)', (idCliente, Email, Nome, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template("Register.html",msg=msg)

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
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('chart.html', Nome=session['Nome'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/profile")
def profile():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cliente WHERE Nome = %s', (session['Nome'],))
        cliente = cursor.fetchone()
        # User is loggedin show them the home page
        return render_template('profile.html', cliente=cliente)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


       
  
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