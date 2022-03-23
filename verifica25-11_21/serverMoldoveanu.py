import threading as thr
import socket as sck
import sqlite3 #libreria per sqlite


#ci sono molte print di test per vedere se tutto funzionasse durante i test
"""
messaggi in arrivo:
(query)$(val1)$(val2)       #val2 c'è solo nella query indicizzata 2 perché devo passargli il nome che il numero del frammento

messaggio di invio:
invio direttamente o la tupla o il valore o la lista che ricevo in risposta alla query

----
inviare i nomi dei file come sono segnati nel DB
"""

class Client_Manager(thr.Thread):
    def __init__(self,connection,address):
        thr.Thread.__init__(self) #super di Java
        self.connection=connection
        self.address=address
        self.running=True
    
    def run(self):
        while self.running:
            msg=self.connection.recv(4096).decode() #aspetta di ricevere un messaggio (nome del comando) dal client
            msg = msg.split("$")
            conn = sqlite3.connect("file.db") #crea una "connessione" col database
            cur = conn.cursor()
            #con le if e le elif seguenti vedo qual è la query e poi le eseguo in base ai valori ricevuti
            #ogni if seguente contiene delle sendall che servono per inviare al client corrispondente la risposta della query
            if int(msg[0]) == 0:
                cur.execute(f'SELECT * FROM files WHERE nome like "%{msg[1]}%"')
                tab0 = cur.fetchall() [0]
                #print(tab0)
                if msg[1] in tab0:
                    #print("si")
                    self.connection.sendall("Presente".encode())
                else:               #ho cercato di controllare se la tupla è vuota (in caso di chiamata di un file nome diverso da quelli esistenti) facendo not tab0 e anche con la funzione len, ma non funzionava
                    #print("no")
                    self.connection.sendall("NON presente".encode())
            elif int(msg[0]) == 1:
                cur.execute(f'SELECT tot_frammenti FROM files WHERE nome like "%{msg[1]}%"')
                tab1 = cur.fetchall() [0] [0]
                self.connection.sendall(f"Frammenti totali: {tab1}".encode())
                #print(tab1)
            elif int(msg[0]) == 2:
                cur.execute(f'SELECT host FROM files inner join frammenti on (frammenti.id_file = files.id_file) WHERE nome like "%{msg[1]}%" and n_frammento = {msg[2]}')
                tab2 = cur.fetchall() [0] [0]
                self.connection.sendall(f"L'host in base al nome del file e al numero dell frammento: {tab2}".encode())
                #print(tab2)
            elif int(msg[0]) == 3:
                cur.execute(f'SELECT host FROM files inner join frammenti on (frammenti.id_file = files.id_file) WHERE nome like "%{msg[1]}%"')
                tab3 = []
                tab3 = cur.fetchall()
                self.connection.sendall(f"Gli host in base al nome del file: {tab3}".encode())
                #print(tab3)

            cur.close()


            

def main():
    
    s=sck.socket(sck.AF_INET,sck.SOCK_STREAM) #prepara il socket per la trasmissione tcp 
    s.bind(("localhost",6000))
    s.listen() #si mette in ascolto per un client che si connette

    while True:
        
        connection, address=s.accept() #accetta la connessione
        client=Client_Manager(connection,address) #crea il thread per gestire il client
        #print(address)
        client.start() #avvia il thread client

if __name__=="__main__":
    main()