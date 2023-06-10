from flask import Flask, render_template, request, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import Flask, request, jsonify, render_template,session
# import openai
# import inspect
# import pinecone
# import numpy as np
from inferenceModel_embedded import main_model

from getpass import getpass

app = Flask(__name__)
# openai.api_key = "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"
# app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'
#db = SQLAlchemy(app)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
'''
cursor.execute(create_table_query)

conn.commit()
    

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login():
    
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()
    print("if")
    print(request)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))

        result = cursor.fetchone()
        print(result)
        cursor.close()
        if result is not None:
            username = request.form['username']
            session['username'] = username
            return render_template('chat.html')
        else:
            return render_template('login.html',error="username or password incorrect")

    return render_template('login.html')

id_val = "example_id"
@app.route('/chat', methods=['POST'])
def chat():
    
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()
    data = request.get_json()
    username = session['username']
    message = data['message']
    response=main_model(message)
    query = "SELECT tokens FROM users WHERE username =?"
    cursor.execute(query,(username,))
    number_of_token = cursor.fetchone()
    number_of_token=int(number_of_token[0])
    print(number_of_token)
    if number_of_token<=0:
        return jsonify({'response': "آپ کے پاس دستیاب میسج ٹوکن ختم ہو گئے ہیں۔"})

    else:
        number_of_token-=1
        query = "update users set tokens=? WHERE username =?"
        cursor.execute(query,(number_of_token,username))
        conn.commit()

    return jsonify({'response': response})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        tokens=10

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        check_query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(check_query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('signup.html', message='Username already exists.')

        cursor.execute("INSERT INTO users (username, password,tokens) VALUES (?,?,?)", (username, password,tokens))
        conn.commit()
        return redirect('/')

    return render_template('signup.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

if __name__ == '__main__':
    app.run(debug=True)

