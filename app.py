import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from db_connect import CryptoController


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.bcoin_total = None
        self.bcoin_heroes = None
        self.app_style()
        
    def app_style(self):
        self.iconbitmap('./assets/icon.ico')
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