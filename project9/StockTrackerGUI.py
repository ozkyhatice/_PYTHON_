from tkinter import *
import tkinter as tk
import dbm
import pickle
class Urun():
    def __init__(self,isim,stok,marka,fiyat,tanim,link):
        self.isim=isim
        self.stok=stok
        self.marka=marka
        self.fiyat=fiyat
        self.tanim=tanim
        self.link=link
    def satıs(self):
        pass
    #def __str__(self):
     #   return self

class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.kimlik=0
        self.initUI()

    def initUI(self):
        self.pack()
        frame1 = tk.Frame(self.parent, borderwidth=10,relief=tk.GROOVE)
        frame1.pack(fill=tk.Y,expand=True,padx=4)


        self.lb1=Listbox(frame1,exportselection=0)
        self.lb1.grid(column=0)
        self.kategoriler=["Yiyecek","Icecek","Giyim","Elektronik","Ev"]
        for indeks,kategori in enumerate(self.kategoriler):
            self.lb1.insert(indeks,kategori)


        self.ekle_butonu=Button(frame1,text="Ekle",command=self.ekle_fonk)
        self.ekle_butonu.grid(column=7,row=1)

        self.isim_baslik1 = tk.Label(frame1, text="Isim")
        self.isim_baslik1.grid(column=1,row=0)
        self.isim_baslik2 = tk.Label(frame1, text="Marka")
        self.isim_baslik2.grid(column=2,row=0)
        self.isim_baslik3 = tk.Label(frame1, text="Tanim")
        self.isim_baslik3.grid(column=3,row=0)
        self.isim_baslik4 = tk.Label(frame1, text="Stok")
        self.isim_baslik4.grid(column=4,row=0)
        self.isim_baslik5 = tk.Label(frame1, text="Fiyat")
        self.isim_baslik5.grid(column=5,row=0)
        self.isim_baslik6 = tk.Label(frame1, text="Link")
        self.isim_baslik6.grid(column=6,row=0)

        self.var_isim = tk.StringVar()
        self.var_marka=tk.StringVar()
        self.var_tanim=tk.StringVar()
        self.var_stok=tk.IntVar()
        self.var_fiyat=DoubleVar()
        self.var_link=StringVar()


        self.eisim = tk.Entry(frame1, textvariable=self.var_isim)
        self.emarka= tk.Entry(frame1, textvariable=self.var_marka)
        self.etanim= tk.Entry(frame1, textvariable=self.var_tanim)
        self.estok= tk.Entry(frame1, textvariable=self.var_stok)
        self.efiyat= tk.Entry(frame1, textvariable=self.var_fiyat)
        self.elink= tk.Entry(frame1, textvariable=self.var_link)

        self.eisim.grid(column=1,row=1,padx=10)
        self.emarka.grid(column=2,row=1,padx=10)
        self.etanim.grid(column=3,row=1,padx=10)
        self.estok.grid(column=4,row=1,padx=10)
        self.efiyat.grid(column=5,row=1,padx=10)
        self.elink.grid(column=6,row=1,padx=10)

        frame2 = tk.Frame(self.parent, borderwidth=10,relief=tk.GROOVE)
        frame2.pack(fill=tk.Y,expand=True,padx=400)

        self.sat_butonu=Button(frame2,text="1 Adet Sat",command=self.sat_fonk)
        self.sat_butonu.pack(side=tk.RIGHT)

        self.lb2=Listbox(frame2,exportselection=0,height=10,width=159)
        self.lb2.pack(side=tk.LEFT)
        

        self.db=dbm.open("veritabanı","c")
    
    def ekle_fonk(self):
        #self.lb1.curselection -->key
        #urun -->value
        for i in self.db.keys():
            while i==self.kimlik:

                self.kimlik+=1
                self.urun=Urun(self.var_isim,self.var_stok,self.var_marka,self.var_fiyat,self.var_tanim,self.var_link)
                self.db[str(self.kimlik)]=pickle.dumps(str(self.urun))
                break
        
        
    def sat_fonk(self):
        self.urun.stok-=1
        #burada stok azalmalı
        self.db_guncelle()
    def db_guncelle(self):
        self.lb2.delete(0,tk.END)
        for key in self.db.keys():
            self.lb2.insert(int(key),print(key,pickle.loads(self.db[str(key)])))

