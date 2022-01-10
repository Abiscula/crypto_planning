import psycopg2
import pandas as pd
from config import hostname, database, username, pwd, port_id
from datetime import date
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

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
        avg = self.cur.fetchone()[0]
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
            

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.bcoin_total = None
        self.bcoin_heroes = None
        self.app_style()
        
    def app_style(self):
        self.geometry("500x500")
        self.title('Bomb Crypto')
        self.config(bg='gray17')
        my_img = ImageTk.PhotoImage(Image.open('./assets/img.png'))
        my_label = tk.Label(self, image=my_img)
        my_label.image = my_img
        
        self.label(my_label)
        
    def label(self, my_label):
        tk.Label(self, text="Clique no botão para inserir os dados no db", 
        bg='gray17', fg='#e49a4c',  font = ('Helvetica 15')).pack(pady=10, anchor= "center")
        
        my_label.pack(pady=10)
        
        self.inputs()
        
    def inputs(self):
        tk.Label(self, text="BCOIN", bg='gray17', fg='#e49a4c',  font=('Helvetica 9')).pack(anchor= "center")
        self.bcoin_total = tk.Entry(self, bg='#eee9ce')
        self.bcoin_total.pack(pady=(2, 20), anchor= "center")

        tk.Label(self, text="HEROES", bg='gray17', fg='#e49a4c',  font=('Helvetica 9')).pack(anchor= "center")
        self.heroes = tk.Entry(self, bg='#eee9ce')
        self.heroes.pack(pady=(2, 20), anchor= "center")
        self.submit()
        
    def submit(self):
        button = tk.Button(self, text="Inserir Dados", background="#e49a4c", fg="#000", font=('Helvetica 10'), command=self.dbclass_start)
        button.pack(pady = 20, anchor = "center")
        
        
    def dbclass_start(self): 
        messagebox.showinfo('Success', 'data entered successfully!')
        CryptoController(self.bcoin_total.get(), self.heroes.get())
        self.bcoin_total.delete(0, tk.END) #input clear
        self.heroes.delete(0, tk.END) #input clear    
        

if __name__ == '__main__':
    app = App()
    app.mainloop()