from email import message
from pyexpat.errors import messages
from flask import Flask, render_template, redirect, url_for, request, make_response
import sqlite3
import random
import string
from sympy import *

app = Flask(__name__)

token = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(30))

def validate(username, password):
    completion = False
    con = sqlite3.connect('C:\\Users\\david\\OneDrive\\Materie ITIS\\anno 21-22\\tpsit\\integrali\\db.db')
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
            #user = request.cookies.get('username')
            resp=make_response(redirect(url_for('integral')))
            resp.set_cookie("username",username)
            return resp
    return render_template('login.html', error=error)

@app.route(f'/integral',methods=['GET', 'POST'])
def integral():
    error = None
    if request.method == 'POST':
        x=Symbol('x')
        fx = request.form['fx']
        e1 = request.form['e1']
        e2 = request.form['e2']
        gx = request.form['gx']
        error=f"intDef: {integrate(fx,(x,e1,e2))} - intInd: {integrate(gx,x)} + c"
        #string=f"intDef: {integrate(fx,(x,e1,e2))} - intInd: {integrate(gx,x)} + c"
        #return redirect(url_for("op",messages=string))

    return render_template('integral.html', error=error)

@app.route(f"/op")
def op():
    return request.args["messages"]

if __name__== "__main__":
    app.run(debug=True)