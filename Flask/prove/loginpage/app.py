from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import random
import string

app = Flask(__name__)

token = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(30))

def validate(username, password):
    completion = False
    con = sqlite3.connect('C:\\Users\\david\\OneDrive\\Materie ITIS\\anno 21-22\\tpsit\\Flask\\prove\\loginpage\\db.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)

@app.route(f'/{token}')
def secret():               #ritorna una stringa su una pagina segreta
    return "This is a secret page!"

if __name__== "__main__":
    app.run(debug=True)