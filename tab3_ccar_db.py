import psycopg2
import pandas as pd
from config import hostname, database, username, pwd, port_id
from datetime import date
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

class Tab3(Tk):
    def __init__(self, tb3):
        self.tab = tb3
        self.ccar_earning = None
        self.cars = None
        self.app_style()
        
    def app_style(self):
        self.tab.config(bg='gray17')
        my_img = ImageTk.PhotoImage(Image.open('./assets/car.png'))
        my_label = Label(self.tab, image=my_img,  bg='gray17')
        my_label.image = my_img
        self.label(my_label)    
        
    
    def label(self, my_label):
        Label(self.tab, text="Clique no botão para inserir os dados no db", 
        bg='gray17', fg='#e49a4c',  font = ('Helvetica 15')).pack(pady=(20, 15), anchor= "center")
        
        my_label.pack(pady=(10, 25))
        self.inputs()
        
    def inputs(self):
        Label(self.tab, text="CCAR", bg='gray17', fg='#e49a4c',  font=('Helvetica 10')).pack(anchor= "center")
        self.ccar_earning = Entry(self.tab, bg='#eee9ce', font=('Helvetica 12'), width=10)
        self.ccar_earning.pack(pady=(3, 25), anchor= "center")

        Label(self.tab, text="Cars", bg='gray17', fg='#e49a4c',  font=('Helvetica 10')).pack(anchor= "center")
        self.cars = Entry(self.tab, bg='#eee9ce', font=('Helvetica 12'), width=10)
        self.cars.pack(pady=(3, 25), anchor= "center")
        self.submit()
        
    def submit(self):
        button = Button(self.tab, text="Inserir Dados", background="#8b0909", fg="#fefefe", font=('Helvetica 11'), 
                        command=self.dbclass_start, height = 1, width = 13)
        button.pack(pady = 25, anchor = "center")
        
        
    def dbclass_start(self): 
        messagebox.showinfo('Success', 'data entered successfully!')
        CryptoCars(self.ccar_earning.get(), self.cars.get())
        self.ccar_earning.delete(0, END) #input clear
        self.cars.delete(0, END) #input clear    


class CryptoCars:
    def __init__(self, ccar_total, cars):
        self.conn = None
        self.cur = None
        self.ccar_earning = float(ccar_total)
        self.day = None
        self.ccar_avg = None
        self.date = date.today()
        self.ccar_total = None
        self.cars = int(cars)
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
        self.cur.execute(''' CREATE TABLE IF NOT EXISTS cryptocars (
                                day     INTEGER PRIMARY KEY,
                                date    DATE NOT NULL,
                                ccar_total   DOUBLE PRECISION NOT NULL,
                                ccar_earning DOUBLE PRECISION NOT NULL,
                                ccar_avg   DOUBLE PRECISION DEFAULT 0,
                                cars  INTEGER NOT NULL) ''')
        self.conn.commit()
        
        self.play_day()
    
    
    def play_day(self):
        self.cur.execute('SELECT MAX(day) FROM cryptocars')
        day = self.cur.fetchone()[0]
        if day == None:
            self.day = 1
        else:
            self.day = day + 1
        
        self.acumulated_ccar()
        
        
    def acumulated_ccar(self):
        if self.day > 1:
            last_day = self.day - 1
            self.cur.execute(f'SELECT ccar_total FROM cryptocars WHERE day = {last_day}')
            ccar_last_day =  self.cur.fetchone()[0]
            self.ccar_total = self.ccar_earning + ccar_last_day
        else:
            self.ccar_total = self.ccar_earning
            
        self.ccar_media()
        
        
    def ccar_media(self):
        self.cur.execute('SELECT ccar_earning FROM cryptocars')
        avg = self.cur.fetchall()
        if self.day > 1:
            average = []
            average.append(self.ccar_earning)
            for i in avg[0]:
                average.append(i)
                
            result = (sum(average)) / len(average)
            self.ccar_avg = result
        
        self.db_insert()
        
    def db_insert(self):
        script = 'INSERT INTO cryptocars (day, date, ccar_total, ccar_earning, ccar_avg, cars) VALUES (%s, %s, %s, %s, %s, %s)'
        values = (self.day, self.date, self.ccar_total, self.ccar_earning, self.ccar_avg, self.cars)
        
        self.cur.execute(script, values)
        self.conn.commit()
        
        self.db_disconnect()
    
    
    def db_disconnect(self):
             
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
            