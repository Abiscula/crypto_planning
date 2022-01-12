import tkinter as tk
from tkinter import ttk
from tab1_crypto_db import Tab1
from tab2_coin_chest import Tab2

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.nb = None
        self.bcoin_total = None
        self.bcoin_heroes = None
        self.app_config()
        
    def app_config(self):

        style = ttk.Style()

        style.theme_create( "my_theme", parent="alt", settings={
                "TNotebook": {"configure": {"tabmargins": [2, 3, 2, 0], "background": "gray17", "bordercolor": "#e3a462" } },
                "TNotebook.Tab": {
                    "configure": {"padding": [5, 1], "background": "#e3a462", "foreground": "#000", "font": "Helvetica 11"},
                    "map":       {"background": [("selected", "#8b0909")], "foreground": [("selected", "#fefefe")],
                                "expand": [("selected", [1, 1, 1, 0])] } } } )

        style.theme_use("my_theme")
        
        self.iconbitmap('./assets/icon.ico')
        self.geometry("500x600")
        self.title('Bomb Crypto')
        self.nb = ttk.Notebook(self)
        self.nb.place(x=0, y=0, width=500, height=600)
        
        self.create_tabs()
        
    def create_tabs(self):
        tb1 = tk.Frame(self.nb)
        self.nb.add(tb1, text="Database")
        Tab1(tb1)
        
        tb2 = tk.Frame(self.nb)
        self.nb.add(tb2, text="Coin chest")
        Tab2(tb2)
    
        
if __name__ == '__main__':
    app = App()
    app.mainloop()