import socket as sck
import threading as thr


#costanti globali
LOCAL = ('localhost', 5001)
NO_ERR = 0



def main():
    #connessione al server
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(LOCAL)

    
    while True:
        #argomento da passare alle funzioni
        arg = None
        #comando da inviare
        com = input('insert a command: ')

        #in base al comando inserito esegue diverse operazioni
        if com in ['fileIn','findHosts','numFrag']:
            arg = input('file name: ')
        if com == 'findFrag':
            arg = input('file name: ') + ';' + input('fragment number: ')
        if com == 'exit':
            s.sendall('exit'.encode())
            break
        if com == 'man':
            print('commands:\n-fileIn\n-findHosts\n-numFrag\n-findFrag')
            continue

        #invia al server il comando con gli argomenti
        # formattazione del testo: comando;arg1[;arg2...]
        msg = com + ';' + str(arg)
        s.sendall(msg.encode())
        
        #riceve e stampa la risposta
        data, _ = s.recvfrom(LOCAL[1])
        print(data.decode())
        
    #chiude la connessione
    s.close()
    exit(NO_ERR)



if __name__ == '__main__':
    main()