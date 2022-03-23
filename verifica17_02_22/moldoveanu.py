import semaforo
from flask import Flask, render_template, redirect, url_for, request, make_response
import sqlite3
from datetime import datetime

app = Flask(__name__)

s = semaforo.semaforo()


@app.route('/test')
def test():                     #il test mi serve solo per vedere sulla web app che le modifiche o attivazioni/spegnimenti sono state fatte correttamente
    return request.args["messages"]     #il messaggio viene passato


@app.route('/semaforo', methods=['GET', 'POST'])
def semaforo():
    error = None

    con = None
    con = sqlite3.connect('C:\\Users\\david\\OneDrive\\Materie ITIS\\anno 21-22\\tpsit\\verifica17_02\\db.db')
    cur = con.cursor()

    if request.method == 'POST':
        stato = request.form['stato']        #chiedo subito lo stato così vedo se il semaforo va attivato o se va spento o se solamente vanno cambiati i tempi delle luci

        if stato == "":                     #se è vuoto significa che bisogna solamente cambiare i tempi
            tV = int(request.form['timeV']) #tempo verde
            tR = int(request.form['timeR']) #tempo rosso
            tG = int(request.form['timeG']) #tempo giallo

            s.rosso(tR)
            s.verde(tV)
            s.giallo(tG)

            string = "TEMPI MODIFICATI"
            return redirect(url_for("test",messages=string))
        
        elif stato == "ATTIVO":             #se viene inserito "ATTIVO" il tempo non cambia ma viene salvato l'ora e il tempo su db
            now = datetime.now()
            dataOra = now.strftime("%d/%m/%Y %H:%M:%S")
            cur.execute(f"INSERT INTO SEMAFORO (stato,dataOra) VALUES ('{stato}','{dataOra}')")
            cur.execute("commit")

            string = "SEMAFORO ATTIVATO"
            return redirect(url_for("test",messages=string))

        else:                               #se viene inserito "SPENTO" o altro il software spegne il semaforo e lo scrive sul db
            #sequenza con semaforo spento. I tempi devono essere
            #modificabili dalla pagina di configurazione!
            for _ in range(3):
                s.giallo(1)
                s.luci_spente(1)
            now = datetime.now()
            dataOra = now.strftime("%d/%m/%Y %H:%M:%S")
            cur.execute(f"INSERT INTO SEMAFORO (stato,dataOra) VALUES ('{stato}','{dataOra}')")
            cur.execute("commit")

            string = "SEMAFORO SPENTO"
            return redirect(url_for("test",messages=string))


    con.close()

    return render_template('semaforo.html', error=error)


def validate(username, password):       #controllo delle credenziali di login
    completion = False
    con = sqlite3.connect('C:\\Users\\david\\OneDrive\\Materie ITIS\\anno 21-22\\tpsit\\verifica17_02\\db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:            #controllo se il username è presente nel db
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:    #se c'è username controllo se la password è presente
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):     #controllo password
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
            resp=make_response(redirect(url_for('semaforo')))
            resp.set_cookie("username",username)
            resp1 = request.cookies.get('username')
            print(resp1)
            return resp
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
