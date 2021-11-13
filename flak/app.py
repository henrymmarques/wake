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
app.config['MYSQL_PASSWORD'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'Wake4ever'
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
            print(session['url'])
            if session['url']=='shop':
                return redirect(url_for("shop"))
            # Redirect to home page
            return redirect(url_for("home"))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
   
    return render_template("login_test.html",msg=msg)
    

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
        cliente = cursor.fetchall()
        # If account exists show error and validation checks
        if cliente:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', Nome):
            msg = 'Username must contain only characters and numbers!'
        elif not Nome or not password or not Email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
           # clientess= cursor2.execute('SELECT * FROM cliente')
            #print(clientess)
            #idCliente = cursor2.execute('SELECT MAX(idCliente) FROM cliente')
            #print(idCliente)
            #idCliente=clientess+1
            cursor2.execute('INSERT INTO cliente VALUES (NULL, %s, %s,%s,NULL, NULL)', ( Email, Nome,password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template("Register_test.html",msg=msg)


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


@app.route('/shop', methods=['GET', 'POST'])
def shop():
     session['url']='shop'
     if request.method == 'POST' and 'genero' in request.form and 'altura' in request.form and 'peso' in request.form:
        # Create variables for easy access
        session['url']='false'
        genero = request.form['genero']
        altura = request.form['altura']
        peso = request.form['peso']
        session['genero'] = genero
        return redirect(url_for('shop2'))
     return render_template("FormPessoal.html")

@app.route('/shop2')
def shop2():
    #if session['genero']== 'Male':
    return render_template("FormRoupa.html") 

if __name__ == '__main__':
    app.run(debug=True, port=8000)