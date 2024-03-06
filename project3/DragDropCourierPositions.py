from tkinter import *

class App(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self , parent)
        self.parent = parent
        self.item=None
        self.initUI()
    def initUI(self):
        self.pack()
        self.canvas = Canvas(self)
        self.daire1=self.canvas.create_oval(42,42,50,50,fill="red")
        self.daire2=self.canvas.create_oval(92,92,100,100,fill="red")
        self.daire3=self.canvas.create_oval(142,142,150,150,fill="red")
        self.daire4=self.canvas.create_oval(192,192,200,200,fill="red")
        self.daire5=self.canvas.create_oval(242,242,250,250,fill="red")
        self.canvas.bind("<Button-1>",self.sol_tik)
        self.canvas.bind("<Button-3>",self.sag_tik)
        self.canvas.pack(fill=BOTH,expand=True)
        
    def sol_tik(self,event):
        print(event)
        for i in range(1):
            self.canvas.itemconfig(self.daire1,fill="red")
            self.canvas.itemconfig(self.daire2,fill="red")
            self.canvas.itemconfig(self.daire3,fill="red")
            self.canvas.itemconfig(self.daire4,fill="red")
            self.canvas.itemconfig(self.daire5,fill="red")
           
        self.item=self.canvas.find_closest(event.x,event.y)
        self.canvas.itemconfig(self.item, fill="blue")
        

    def sag_tik(self,event):
        #print(event)
        if self.item==None:
            pass
        else:

            suanki=self.canvas.coords(self.item)
            #print(suanki)
            self.canvas.itemconfig(self.item, fill="green")
            self.canvas.move(self.item,event.x-suanki[0],event.y-suanki[1])
    
        
