import psycopg2
import pandas as pd
from config import hostname, database, username, pwd, port_id
from datetime import date
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

class Tab1(Tk):
    def __init__(self, tb1):
        self.tab = tb1
        self.app_style()
        
    def app_style(self):
        self.tab.config(bg='gray17')
        my_img = ImageTk.PhotoImage(Image.open('./assets/img.png'))
        my_label = Label(self.tab, image=my_img)
        my_label.image = my_img
        self.label(my_label)    
        
    
    def label(self, my_label):
        Label(self.tab, text="Clique no botão para inserir os dados no db", 
        bg='gray17', fg='#e49a4c',  font = ('Helvetica 15')).pack(pady=(20, 15), anchor= "center")
        
        my_label.pack(pady=(10, 25))
        self.inputs()
        
    def inputs(self):
        Label(self.tab, text="BCOIN", bg='gray17', fg='#e49a4c',  font=('Helvetica 10')).pack(anchor= "center")
        self.bcoin_total = Entry(self.tab, bg='#eee9ce', font=('Helvetica 12'), width=10)
        self.bcoin_total.pack(pady=(3, 25), anchor= "center")

        Label(self.tab, text="HEROES", bg='gray17', fg='#e49a4c',  font=('Helvetica 10')).pack(anchor= "center")
        self.heroes = Entry(self.tab, bg='#eee9ce', font=('Helvetica 12'), width=10)
        self.heroes.pack(pady=(3, 25), anchor= "center")
        self.submit()
        
    def submit(self):
        button = Button(self.tab, text="Inserir Dados", background="#8b0909", fg="#fefefe", font=('Helvetica 11'), 
                        command=self.dbclass_start, height = 1, width = 13)
        button.pack(pady = 25, anchor = "center")
        
        
    def dbclass_start(self): 
        messagebox.showinfo('Success', 'data entered successfully!')
        CryptoController(self.bcoin_total.get(), self.heroes.get())
        self.bcoin_total.delete(0, END) #input clear
        self.heroes.delete(0, END) #input clear    


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
        self.cur.execute('SELECT bcoin_earning FROM bombcrypto')
        avg = self.cur.fetchall()
        if avg != None:
            df = pd.DataFrame(avg, columns=['bcoin_earning'])
            self.bcoin_avg = df['bcoin_earning'].mean()
        
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
            

