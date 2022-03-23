import socket as sck
import threading as thr
import time 


"""
messaggi in invio:
(query)$(val1)$(val2)       #val2 c'è solo nella query indicizzata 2 perché devo passargli il nome che il numero del frammento

messaggi in arrivo:
ricevo direttamente o la tupla o il valore o la lista che ricevo in risposta alla query
"""



class Recv_Manager(thr.Thread): 
    def __init__(self,socket): 
        thr.Thread.__init__(self) #super di Java 
        self.socket=socket 
        self.running=True 
    def run(self): 
        while self.running: 
            received_msg=self.socket.recv(4096).decode()        #riceve il messaggio e lo stampa subito dopo
            print(received_msg)


            
                


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(('localhost',6000))
    receiver=Recv_Manager(s)
    receiver.start()

    #creo un menù per poter gestire meglio le query
    print("0 - chiedere al server se un certo nome file è presente\n"
          "1 - chiedere al server il numero di frammenti di un file a partire dal suo nome file\n"
          "2 - chiedere al server l’IP dell’host che ospita un frammento a partire nome file e dal numero del frammento\n"
          "3 - chiedere al server tutti gli IP degli host sui quali sono salvati i frammenti di un file a partire dal nome file\n")

    while True:
        #chiedo quale query si desidera 
        #se si chiede la query indicizzata 2 entro nel if dove chiederò due input e li invierò insieme
        query = input("Inserisci il numero corrispondente alla query desiderata: ")
        if int(query) == 2:
            inp1 = input("Inserisci il nome del file: ")
            inp2 = input("Inserisci il numero del frammento: ")
            s.sendall(f"{query}${inp1}${inp2}".encode())
        else:   #per tutte le altre query
            inp = input("Inserisci l'input in base alla richiesta: ")
            s.sendall(f"{query}${inp}".encode())
        time.sleep(1)   #serve per vedere meglio la console (se non mettevo nessuno sleep le scritte si sarebbero acavallate)

if __name__=="__main__":
    main()