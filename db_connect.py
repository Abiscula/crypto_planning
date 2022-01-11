import psycopg2
import pandas as pd
from config import hostname, database, username, pwd, port_id
from datetime import date

class CryptoController:
    def __init__(self, bcoin_total, heroes):
        self.conn = None
        self.cur = None
        self.bcoin_earning = None
        self.day = None
        self.bcoin_avg = None
        self.date = date.today()
        self.bcoin_total = float(bcoin_total)
        self.heroes = int(heroes)
        self.db_conect()
        

    def db_conect(self):
        self.conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id
        )
        self.db_create_table()
        
        
    def db_create_table(self):
        self.cur  = self.conn.cursor()
        self.cur.execute(''' CREATE TABLE IF NOT EXISTS bombcrypto (
                                day     INTEGER PRIMARY KEY,
                                date    DATE NOT NULL,
                                bcoin_total   DOUBLE PRECISION NOT NULL,
                                bcoin_earning DOUBLE PRECISION NOT NULL,
                                bcoin_avg   DOUBLE PRECISION DEFAULT 0,
                                heroes  INTEGER NOT NULL) ''')
        self.conn.commit()
        
        self.play_day()
    
    
    def play_day(self):
        self.cur.execute('SELECT MAX(day) FROM bombcrypto')
        day = self.cur.fetchone()[0]
        if day == None:
            self.day = 1
        else:
            self.day = day + 1
        
        self.bcoin_today()
        
        
    def bcoin_today(self):
        self.cur.execute('SELECT * FROM bombcrypto')
        data = self.cur.fetchall()
        df = pd.DataFrame(data)
        tamanho = df.shape[0]
        if tamanho > 0:
            self.cur.execute(f'SELECT bcoin_total FROM bombcrypto WHERE day = {tamanho}')
            bcoin_last_day =  self.cur.fetchone()[0]
            self.bcoin_earning = self.bcoin_total - bcoin_last_day
        elif tamanho == 0:
            self.bcoin_earning = self.bcoin_total
            
        self.bcoin_media()
        
        
    def bcoin_media(self):
        self.cur.execute('SELECT AVG(bcoin_earning) FROM bombcrypto')
        avg = self.cur.fetchone()
        if avg != None:
            self.bcoin_avg = avg
        
        self.db_insert()
        
    def db_insert(self):
        script = 'INSERT INTO bombcrypto (day, date, bcoin_total, bcoin_earning, bcoin_avg, heroes) VALUES (%s, %s, %s, %s, %s, %s)'
        values = (self.day, self.date, self.bcoin_total, self.bcoin_earning, self.bcoin_avg, self.heroes)
        
        self.cur.execute(script, values)
        self.conn.commit()
        
        self.db_disconnect()
    
    
    def db_disconnect(self):
             
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
            

