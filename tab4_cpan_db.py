import psycopg2
import pandas as pd
from config import hostname, database, username, pwd, port_id
from datetime import date
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

class Tab4(Tk):
    def __init__(self, tb4):
        self.tab = tb4
        self.cpan_earning = None
        self.planes = None
        self.app_style()
        
    def app_style(self):
        self.tab.config(bg='gray17')
        my_img = ImageTk.PhotoImage(Image.open('./assets/plane.png'))
        my_label = Label(self.tab, image=my_img,  bg='gray17')
        my_label.image = my_img
        self.label(my_label)
    
    def label(self, my_label):
        Label(self.tab, text="Clique no botão para inserir os dados no db", 
        bg='gray17', fg='#e49a4c',  font = ('Helvetica 15')).pack(pady=(20, 15), anchor= "center")
        
        my_label.pack(pady=(10, 25))
        self.inputs()
        
    def inputs(self):
        Label(self.tab, text="CPAN", bg='gray17', fg='#e49a4c',  font=('Helvetica 10')).pack(anchor= "center")
        self.cpan_earning = Entry(self.tab, bg='#eee9ce', font=('Helvetica 12'), width=10)
        self.cpan_earning.pack(pady=(3, 25), anchor= "center")

        Label(self.tab, text="Planes", bg='gray17', fg='#e49a4c',  font=('Helvetica 10')).pack(anchor= "center")
        self.planes = Entry(self.tab, bg='#eee9ce', font=('Helvetica 12'), width=10)
        self.planes.pack(pady=(3, 25), anchor= "center")
        self.submit()
        
    def submit(self):
        button = Button(self.tab, text="Inserir Dados", background="#8b0909", fg="#fefefe", font=('Helvetica 11'), 
                        command=self.dbclass_start, height = 1, width = 13)
        button.pack(pady = 25, anchor = "center")
        
        
    def dbclass_start(self): 
        messagebox.showinfo('Success', 'data entered successfully!')
        CryptoPlanes(self.cpan_earning.get(), self.planes.get())
        self.cpan_earning.delete(0, END) #input clear
        self.planes.delete(0, END) #input clear    


class CryptoPlanes:
    def __init__(self, cpan_total, planes):
        self.conn = None
        self.cur = None
        self.cpan_earning = float(cpan_total)
        self.day = None
        self.cpan_avg = None
        self.date = date.today()
        self.cpan_total = None
        self.planes = int(planes)
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
        self.cur.execute(''' CREATE TABLE IF NOT EXISTS cryptoplanes (
                                day     INTEGER PRIMARY KEY,
                                date    DATE NOT NULL,
                                cpan_total   DOUBLE PRECISION NOT NULL,
                                cpan_earning DOUBLE PRECISION NOT NULL,
                                cpan_avg   DOUBLE PRECISION DEFAULT 0,
                                planes  INTEGER NOT NULL) ''')
        self.conn.commit()
        
        self.play_day()
    
    
    def play_day(self):
        self.cur.execute('SELECT MAX(day) FROM cryptoplanes')
        day = self.cur.fetchone()[0]
        if day == None:
            self.day = 1
        else:
            self.day = day + 1
        
        self.acumulated_cpan()
        
        
    def acumulated_cpan(self):
        if self.day > 1:
            last_day = self.day - 1
            self.cur.execute(f'SELECT cpan_total FROM cryptoplanes WHERE day = {last_day}')
            cpan_last_day =  self.cur.fetchone()[0]
            self.cpan_total = self.cpan_earning + cpan_last_day
        else:
            self.cpan_total = self.cpan_earning
            
        self.cpan_media()
        
        
    def cpan_media(self):
        self.cur.execute('SELECT cpan_earning FROM cryptoplanes')
        avg = self.cur.fetchall()
        if self.day > 1:
            average = []
            average.append(self.cpan_earning)
            for i in avg[0]:
                average.append(i)
                
            result = (sum(average)) / len(average)
            self.cpan_avg = result
        
        self.db_insert()
        
    def db_insert(self):
        script = 'INSERT INTO cryptoplanes (day, date, cpan_total, cpan_earning, cpan_avg, planes) VALUES (%s, %s, %s, %s, %s, %s)'
        values = (self.day, self.date, self.cpan_total, self.cpan_earning, self.cpan_avg, self.planes)
        
        self.cur.execute(script, values)
        self.conn.commit()
        
        self.db_disconnect()
    
    
    def db_disconnect(self):
             
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
            