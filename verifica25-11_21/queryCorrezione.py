'''
Andrea Tomatis

Verifica 25/11/2021

database lib
'''

import sqlite3
from sqlite3 import Error



class Db_Connection():
    '''
    Classe per interfacciarsi con il database. Contiene diverse funzioni per 
    le query e la chiusura della connessione con il db.
    '''
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection(db_file)
        self.cur = self.conn.cursor()
        
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn
        
    def fileIn(self, fn):
        '''
        scopre se un file e' nel db
        '''
        self.cur.execute(f'SELECT nome FROM files')
        file_names = self.cur.fetchall()
        for line in file_names:
            if fn in line: return 'Yes'
        return 'No'

    def numFrag(self, fn):
        '''
        restituisce il numero di frammenti di un file
        '''
        self.cur.execute(f'SELECT files.nome, count(*) FROM files join frammenti on (frammenti.id_file = files.id_file) GROUP by files.nome')
        data = self.cur.fetchall()
        for line in data:
            if fn in line[0]: return str(line[1])
        return 'No such file'
    
    def findFrag(self, fn, frag_num):
        '''
        restituisce l'ip dell'host avente un dato frammento
        di un dato file
        '''
        self.cur.execute(f'SELECT frammenti.host FROM frammenti join files on files.id_file = frammenti.id_file WHERE files.nome = "{fn}" AND frammenti.id_frammento = {frag_num}')
        host = self.cur.fetchall()
        return host[0][0]
        
    def findHosts(self, fn):
        '''
        Restituisce tutti gli ho che contengono
        frammenti di un dato file
        '''
        self.cur.execute(f'SELECT frammenti.host FROM frammenti join files on files.id_file = frammenti.id_file WHERE files.nome = "{fn}"')
        host = self.cur.fetchall()
        return ','.join(h[0] for h in host)
    

    def close(self):
        '''chiude la connessione con il db'''
        self.cur.close()
        self.conn.close()