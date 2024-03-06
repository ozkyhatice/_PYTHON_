from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd 
import json

class App(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self , parent)
        self.parent = parent
        
        self.initUI()

    def initUI(self):
        
        self.lb = Listbox(self, selectmode="single")
        self.lb.pack(fill=tk.BOTH, expand=True)

        self.buton1 = tk.Button(self, text="Aktar", command = self.harcama_listesi_fonk)
        self.buton2= tk.Button(self, text="Secili Sil", command = self.secileni_sil_fonk)
        self.buton3= tk.Button(self, text="Hepsini Sil", command = self.hepsini_sil_fonk)
        self.buton1.pack(side="left")
        self.buton2.pack(side="left")
        self.buton3.pack(side="left")
        self.pack(fill=tk.BOTH, expand=True)

    def elemanekle(self):
        name= fd.askopenfilename()
        file = open(name, 'r')
        self.urunler = json.load(file)
        self.harcama_listesi_fonk=[]
        for satir in self.urunler:
            self.harcama_listesi_fonk+=[[satir['isim'], satir['aciklama'],satir['marka'],satir['marka'], float(satir['fiyat']), satir['kategori'],int(satir['stok'])]]
            
        self.lb = Listbox(self.parent, selectmode="single")
        for indeks, urun in enumerate(self.harcama_listesi_fonk):
            print(indeks,",", urun)
            self.lb.insert(indeks, urun)


    def harcama_listesi_fonk(self):
        self.elemanekle()
        self.lb.pack(expand=True)
        self.pack(fill=tk.BOTH, expand=True)


        
    def secileni_sil_fonk(self):
        secili = self.lb.curselection()[0]
        try:
            self.harcama_listesi_fonk.pop(secili)
        except KeyError as a:
            print(a)
        self.lb.delete(secili)

    def hepsini_sil_fonk(self):
        self.lb.delete(0, tk.END)
        self.harcama_listesi_fonk.clear()

