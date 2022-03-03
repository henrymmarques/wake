from flask import Flask, Blueprint, json, render_template, request, jsonify, redirect, url_for
from flask import render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
import re
import roupascluster
import random




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
        password1 = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cliente WHERE Nome = %s', (Nome,))
        # Fetch one record and return result
        cliente = cursor.fetchone()
        print(cliente)
        # If account exists in accounts table in out database
        if cliente:
            if check_password_hash(cliente['Password'], password1):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['Nome'] = cliente['Nome']
                print(session['url'])
                if session['url'] == 'shop':
                    return redirect(url_for("shop"))
                # Redirect to home page
                return redirect(url_for("home"))
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
                #  Show the login form with message (if any)

    return render_template("login_test.html", msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Nome' in request.form and 'password' in request.form and 'Email' in request.form:
        # Create variables for easy access
        Nome = request.form['Nome']
        password = generate_password_hash(request.form['password'])
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
            # print(clientess)
            #idCliente = cursor2.execute('SELECT MAX(idCliente) FROM cliente')
            # print(idCliente)
            # idCliente=clientess+1
            cursor2.execute(
                'INSERT INTO cliente VALUES (NULL, %s, %s, %s, NULL, NULL, NULL, NULL, NULL)', (Email, Nome, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template("Register_test.html", msg=msg)


@app.route("/aboutUs")
def about_us():
    return render_template("aboutUs.html")

@app.route("/contact")
def contact():
    return render_template("chatbot.html")

@app.route("/forgotPassword")
def forgotPassword():
    return render_template("comingsoon.html")



@app.route("/cart")
def cart():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('cart.html', Nome=session['Nome'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cliente WHERE Nome = %s',
                       (session['Nome'],))
        cliente = cursor.fetchone()
        # User is loggedin show them the home page
       # return render_template('profile_test.html', cliente=cliente)
        if 'Nome' in request.form and 'Email' in request.form and 'Morada' in request.form:
            print('AQUIIIII')
             # Create variables for easy access
            Nome = request.form['Nome']
            #password1 = request.form['password']
            password1 = generate_password_hash(request.form['password'])
            email = request.form['Email']
            morada = request.form['Morada']
            # Check if account exists using MySQL
            cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor1.execute('UPDATE wake.cliente set Nome = %s, Email= %s, Password=%s, Morada= %s WHERE Nome= %s', (Nome, email, password1, morada, session['Nome'],))
            mysql.connection.commit()
            session['Nome']=Nome
            cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor2.execute('SELECT * FROM cliente WHERE Nome = %s', (session['Nome'],))
            cliente = cursor2.fetchone()
        # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))
    return render_template('profile_test.html', cliente=cliente)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/formteste', methods=['GET', 'POST'])
def shop1():
    return render_template("FormTamanhos.html")

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    session['url'] = 'shop'
    if request.method == 'POST' and 'genero' in request.form and 'altura' in request.form and 'peso' in request.form:
        # Create variables for easy access
        session['url'] = 'false'
        genero = request.form['genero']
        altura = request.form['altura']
        peso = request.form['peso']
        session['genero'] = genero
        return redirect(url_for('shop2'))
    return render_template("FormTamanhos.html")



@app.route('/filtro', methods=['GET', 'POST'])
def filtro():
    if request.method == 'POST' :
        return redirect(url_for('package'))
    if session['genero']=='Female':  
        return render_template("filtros_mulher.html")
    else:
        return render_template("filtros_homem.html")




#recebe o nome de cada imagem do formulario e verifica a checkbox. Para nao se fazer uma carrada de ifs
def checkboxImage(str):
    if request.form.get(str):
        return 1
    else:    
        return 0

@app.route('/shop2', methods=['GET', 'POST'])
def shop2():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT idCliente FROM cliente WHERE Nome = %s', (session['Nome'],))
    idCliente = cursor.fetchone()['idCliente']
    
    if request.method == 'POST' and session['genero']=='Male':
        alterno1 = checkboxImage("alterno1")
        alterno2 = checkboxImage("alterno2")
        alterno3 = checkboxImage("alterno3")
        classic1 = checkboxImage("classic1")
        classic2 = checkboxImage("classic2")
        classic3 = checkboxImage("classic3")
        desportivo1 = checkboxImage("desportivo1")
        desportivo2 = checkboxImage("desportivo2")
        desportivo3 = checkboxImage("desportivo3")
        flannel1 = checkboxImage("flannel1")
        flannel2 = checkboxImage("flannel2")
        flannel3 = checkboxImage("flannel3")
        streetwear1 = checkboxImage("streetwear1")
        streetwear2 = checkboxImage("streetwear2")
        streetwear3 = checkboxImage("streetwear3")
        cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        print(roupascluster.cluster_masculino(alterno1,\
                       alterno2, alterno3, classic1, classic2, classic3, desportivo1, desportivo2, desportivo3, flannel1, flannel2, flannel3, streetwear1,\
                            streetwear2, streetwear3))
        nomeEstilo=roupascluster.cluster_masculino(alterno1,\
                       alterno2, alterno3, classic1, classic2, classic3, desportivo1, desportivo2, desportivo3, flannel1, flannel2, flannel3, streetwear1,\
                            streetwear2, streetwear3)[0]
        session['nomeEstilo']=nomeEstilo
        
    #select idEstilo according to Nome_estilo from clusters
        cursor_estilo = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor_estilo.execute('SELECT idEstilo FROM estilo WHERE Nome_estilo = %s', (nomeEstilo,))
        idEstilo = cursor_estilo.fetchone()['idEstilo']
        

       
        cursor1.execute('INSERT INTO `wake`.`formulario` (`Resposta 1`, `Resposta 2`, `Resposta 3`, `Resposta 4`, `Resposta 5`, `Resposta 6`, \
             `Resposta 7`, `Resposta 8`, `Resposta 9`, `Resposta 10`, `Resposta 11`, `Resposta 12`, `Resposta 13`, `Resposta 14`, `Resposta 15`,\
                  `Cliente_idCliente`, `Estilo_idEstilo1`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (alterno1,\
                       alterno2, alterno3, classic1, classic2, classic3, desportivo1, desportivo2, desportivo3, flannel1, flannel2, flannel3, streetwear1,\
                            streetwear2, streetwear3, idCliente, idEstilo))
        mysql.connection.commit()
        return redirect(url_for('filtro'))
    elif request.method == 'POST' and session['genero']=='Female':
        boho1 = checkboxImage("boho1")
        boho2 = checkboxImage("boho2")
        casual1 = checkboxImage("casual1")
        casual2 = checkboxImage("casual2")
        casual3 = checkboxImage("casual3")
        classic1_f = checkboxImage("classic1_f")
        classic2_f = checkboxImage("classic2_f")
        classic3_f = checkboxImage("classic3_f")
        comfy1 = checkboxImage("comfy1")
        comfy2 = checkboxImage("comfy2")
        comfy3 = checkboxImage("comfy3")
        indie1 = checkboxImage("indie1")
        streetwear1_f = checkboxImage("streetwear1_f")
        streetwear2_f = checkboxImage("streetwear2_f")
        streetwear3_f = checkboxImage("streetwear3_f")
        print(roupascluster.cluster_feminino(boho1, boho2, casual1, casual2, casual3, classic1_f, classic2_f, classic3_f, comfy1, comfy2, comfy3, indie1, streetwear1_f, streetwear2_f, streetwear3_f))
        nomeEstilo = roupascluster.cluster_feminino(boho1, boho2, casual1, casual2, casual3, classic1_f, classic2_f, classic3_f, comfy1, comfy2, comfy3, indie1, streetwear1_f, streetwear2_f, streetwear3_f)[0]
    
    #guardar o estilo para ser usado no select do sql do pacote
        session['nomeEstilo']=nomeEstilo
    
    #select idEstilo according to Nome_estilo from clusters
        cursor_estilo = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor_estilo.execute('SELECT idEstilo FROM estilo WHERE Nome_estilo = %s', (nomeEstilo,))
        idEstilo = cursor_estilo.fetchone()['idEstilo']

    #insert into table formulario - answers and idEstilo
        cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor1.execute('INSERT INTO `wake`.`formulario` (`Resposta 1`, `Resposta 2`, `Resposta 3`, `Resposta 4`, `Resposta 5`, `Resposta 6`, \
             `Resposta 7`, `Resposta 8`, `Resposta 9`, `Resposta 10`, `Resposta 11`, `Resposta 12`, `Resposta 13`, `Resposta 14`, `Resposta 15`,\
                  `Cliente_idCliente`, `Estilo_idEstilo1`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (boho1,\
                       boho2, casual1, casual2, casual3, classic1_f, classic2_f, classic3_f, comfy1, comfy2, comfy3, indie1, streetwear1_f,\
                            streetwear2_f, streetwear3_f, idCliente, idEstilo,))
        mysql.connection.commit()
        return redirect(url_for('filtro'))
    return render_template('FormRoupa.html')

@app.route("/package")
def package():
    #select url aleatorio que contem o estilo da sessão
    cursor_estilo = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #cursor_estilo.execute('SELECT URL FROM roupa WHERE url like ´%/%s%´ order by rand() limit 1', (session['nomeEstilo'],))
    cursor_estilo.execute('SELECT url FROM estilo_roupa, roupa, estilo WHERE estilo_roupa.Roupa_idRoupa=roupa.idRoupa and estilo_roupa.Estilo_idEstilo=Estilo.idEstilo and roupa.genero=%s and  estilo.Nome_Estilo=%s;', (session['genero'],session['nomeEstilo'],))
    
    print('AQUIIIIIIII')
    #urlEstilo = cursor_estilo.fetchone()['url']
    urlEstilo = cursor_estilo.fetchall()
   # print(urlEstilo)
    print(session['nomeEstilo'])

    style=random.choice(urlEstilo)['url']
    
    session['urlEstilo']=style
    print(session['urlEstilo'])
    return render_template("package.html")



    

    ###############################################################
"""
import numpy as np
import pickle
import json
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# chat initialization
model = load_model("chatbot_model.h5")
intents = json.loads(open("intents.json").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))



@app.route("/contact/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
    return res


# chat functionalities
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return 
  """

if __name__ == '__main__':
    app.run(debug=True, port=5000)
