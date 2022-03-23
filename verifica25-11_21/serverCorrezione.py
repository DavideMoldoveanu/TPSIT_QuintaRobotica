import socket as sck
import threading as thr
from query import Db_Connection


#lista per contenere i client
lstClient = []

#porta di connessione con i client
PORT = 5001


class Client_Manager(thr.Thread):
    '''
    gestisce in multithread i vari client connessi
    '''

    def __init__(self, conn, ip):
        thr.Thread.__init__(self)
        self.conn = conn
        self.ip = ip
        self.running = True
        

    def run(self):
        '''
        in base al comando ricevuto
        effettua una query al db e rispedisce al
        client la risposta
        '''

        db = Db_Connection('./file.db')
        
        #dizionario di funzioni per contenere le query
        commands = {
            'fileIn' : db.fileIn,
            'numFrag': db.numFrag,
            'findFrag' : db.findFrag,
            'findHosts': db.findHosts
        }

        #esegue finche' il client non si sconnette
        while self.running:
            data, _ = self.conn.recvfrom(PORT)
            com = data.decode().split(';')

            #interrompe il ciclo se il client se si sconnette
            if 'exit' in com:
                self.running = False
                print('client removed')
                break
            
            #tenta di eseguire le query del client, se possibile
            try:
                if 'findFrag' in com:
                    self.conn.sendall(commands[com[0]](com[1],com[2]).encode())    
                else:
                    self.conn.sendall(commands[com[0]](com[1]).encode())
            except Exception:
                self.conn.sendall(f'invalid command'.encode())
        
        #se il ciclo finisce chiude il database
        db.close()



class Accettazione(thr.Thread):
    '''
    Salva e inizializza i nuovi client che si connettono
    '''
    def __init__(self, s):
        thr.Thread.__init__(self)
        self.s = s
    
    def run(self):
        while True:
            conn, addr = self.s.accept()
            client = Client_Manager(conn, addr[0])
            print(f'new client connected: {addr[0]}')
            lstClient.append(client) 
            client.start()



def main():
    #inizializzazione del socket
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(('127.0.0.1', PORT))
    s.listen()

    #apre l'accettazione per i client
    acc = Accettazione(s)
    acc.start()
    
    #se un client si sconnette uccide il thread
    while True:
        for c in lstClient:
            if not c.running:
                c.join()
                lstClient.remove(c)



if __name__ == "__main__":
    main()