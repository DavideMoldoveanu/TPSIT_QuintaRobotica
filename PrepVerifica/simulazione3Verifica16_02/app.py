from flask import Flask, render_template, redirect, url_for, request, make_response
from re import U
import threading as thr
from datetime import datetime
import sqlite3
import random
import string

app = Flask(__name__)

def validate(username, password):
    completion = False
    con = None
    try:
        con = sqlite3.connect('C:\\Users\\david\\OneDrive\\Materie ITIS\\anno 21-22\\tpsit\\simulazione3Verifica16_02\\data.db')
    except:
        print("database mancante")
    
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM USERS")
    except:
        print("tabella mancante")
    rows = cur.fetchall()
    
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password



@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST': #se uguale a GET fa il return della pagina login
        username = request.form['username']
        password = request.form['password']
        
        if validate(username, password): 
            resp = make_response(redirect(url_for('social')))
            resp.set_cookie('username', username)
            print(request.cookies.get('username'))
            return resp
        
    return render_template('login.html', error=error)



@app.route(f'/social', methods=['GET', 'POST'])
def social():
    error = None
    con = None
    con = sqlite3.connect('C:\\Users\\david\\OneDrive\\Materie ITIS\\anno 21-22\\tpsit\\simulazione3Verifica16_02\\data.db')
    cur = con.cursor()

    if request.method == 'POST':
        stato = request.form['stato']

        cur.execute(f"INSERT INTO stati (utente,stato) VALUES ('{request.cookies.get('username')}','{stato}')")
        cur.execute("commit")

    try:
        cur.execute("SELECT * FROM stati")
    except:
        print("tabella mancante")

    rows = cur.fetchall()
    nrows=len(rows)-1
    print(nrows)
    if nrows>0:
        estrai = random.randint(0, nrows)
        utente = rows[estrai][1]
        statRand = rows[estrai][2]
        error = f"L'utente {utente} ha come stato {statRand}"
    else:
        error= "Sei il primo utente inserisci uno stato"
            
    con.close()
    return render_template("calcolo.html",error=error)




if __name__== "__main__":
    app.run(debug=True) 