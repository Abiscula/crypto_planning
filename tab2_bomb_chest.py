from tkinter import *
from PIL import ImageTk, Image

class Tab2(Tk):
    def __init__(self, tb2):
        self.tab = tb2
        self.crystal_input = 0
        self.gold_input = 0
        self.metal_input = 0
        self.wood_input = 0
        self.app_style()
        
    def app_style(self):
        self.tab.config(bg='gray17')
        my_img = ImageTk.PhotoImage(Image.open('./assets/img2.png'))
        
        my_label = Label(self.tab, image=my_img)
        my_label.image = my_img
        self.label(my_label)    
        
    
    def label(self, my_label):
        Label(self.tab, text="Calcular ouro do mapa", 
        bg='gray17', fg='#e49a4c',  font = ('Helvetica 15')).pack(pady=(20, 5), anchor= "center")
        
        my_label.pack(pady=(10, 10))
        
        self.chests_images()
        
    def chests_images(self):
        crystal = ImageTk.PhotoImage(Image.open('./assets/chestCrystal.png'))
        crystal_label = Label(self.tab, image=crystal, bg='gray17')
        crystal_label.image = crystal
        crystal_label.place(x=80, y=420)
        
        gold = ImageTk.PhotoImage(Image.open('./assets/chestGold.png'))
        gold_label = Label(self.tab, image=gold, bg='gray17')
        gold_label.image = gold
        gold_label.place(x=80, y=470)
        
        metal = ImageTk.PhotoImage(Image.open('./assets/chestMetal.png'))
        metal_label = Label(self.tab, image=metal, bg='gray17')
        metal_label.image = metal
        metal_label.place(x=180, y=420)
        
        wood = ImageTk.PhotoImage(Image.open('./assets/chestWood.png'))
        wood_label = Label(self.tab, image=wood, bg='gray17')
        wood_label.image = wood
        wood_label.place(x=180, y=470)
        
        self.chests_inputs()
    
    def chests_inputs(self):
        
        self.crystal_input = Entry(self.tab, bg='#eee9ce', width=3, font=('Helvetica 14'))
        self.crystal_input.insert(END, 0) #definindo valor padrão
        self.crystal_input.place(x=120, y=424)
        
        self.gold_input = Entry(self.tab, bg='#eee9ce', width=3, font=('Helvetica 14'))
        self.gold_input.insert(END, 0)
        self.gold_input.place(x=120, y=474)
        
        self.metal_input = Entry(self.tab, bg='#eee9ce', width=3, font=('Helvetica 14'))
        self.metal_input.insert(END, 0)
        self.metal_input.place(x=220, y=424)

        self.wood_input = Entry(self.tab, bg='#eee9ce', width=3, font=('Helvetica 14'))
        self.wood_input.insert(END, 0)
        self.wood_input.place(x=220, y=474)

        self.submit()
        

    def submit(self):
        button = Button(self.tab, text="Calcular", background="#8b0909", fg="#fefefe", font=('Helvetica 12'), 
                        command=self.earning_farmed, height = 3, width = 12)
        button.place(x=290, y=430)
        
    def earning_farmed(self):
        crystal = int(self.crystal_input.get()) * 0.325
        gold = int(self.gold_input.get()) * 0.1625
        metal = int(self.metal_input.get()) * 0.0325
        wood = int(self.wood_input.get()) * 0.01425
        total_earning = crystal + gold + metal + wood
        
        output = Label(self.tab, bg='#eee9ce', width=10, font=('Helvetica 13'), text=round(total_earning, 3))
        output.place(x=128, y=525)
        
        #Clean and insert default value on inputs after submit
        self.crystal_input.delete(0, END)
        self.crystal_input.insert(END, 0)
        
        self.gold_input.delete(0, END)
        self.gold_input.insert(END, 0)
        
        self.metal_input.delete(0, END)
        self.metal_input.insert(END, 0)
        
        self.wood_input.delete(0, END)
        self.wood_input.insert(END, 0)
        
        
        
        
        