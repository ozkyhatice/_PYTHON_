from cProfile import label
from distutils.spawn import spawn
from msilib.schema import ListBox
from pyparsing import col
from xlrd import open_workbook
import tkinter as tk
import dbm
import pickle 
from tkinter import Label, StringVar, messagebox
from fonksiyonlar import topMatches,transformPrefs,getRecommendations,getRecommendedItems,sim_pearson,sim_cosine,sim_jaccard,sim_distance,calculateSimilarItems
import math

class App():

    def __init__(self,parent):
        self.parent=parent
        
        frame_kullanici_girdi = tk.Frame(self.parent,relief=tk.GROOVE, border=10, width=200)
        frame_kullanici_girdi.pack(fill=tk.Y, expand=True)
        self.db_baslat()
        self.initGirdi(frame_kullanici_girdi)
        self.urun_ekle()
        


    def db_baslat(self):
        self.db_urun=dbm.open("test.db","c")
    def initGirdi(self,frame):
        
        self.listbox_kategori=tk.Listbox(frame,bg = "white",height=16,width=40)
        #excel dosyası okunuyor:
        book = open_workbook("Degerlendirmeler.xls")
        sheet = book.sheet_by_index(0)
        self.kategoriler=[]
        self.diger_kullanıcılar={}
        self.sozluk_rating={}
        for row in range(1, sheet.nrows):     #MP-3.docx dosyasından alıntı
            user = sheet.cell(row, 0).value
            product = sheet.cell(row, 1).value
            rating = float(sheet.cell(row, 2).value)
            self.sozluk_rating[product]=rating
            self.diger_kullanıcılar[user]=self.sozluk_rating
            if product not in self.kategoriler:
                self.kategoriler.append(product)
            
        for kategori in self.kategoriler:
            self.listbox_kategori.insert(tk.END,kategori)
        self.listbox_kategori.grid(row=0,column=0,columnspan=1)


        self.puan_var=tk.DoubleVar()
        self.entry_puan=tk.Entry(frame,textvariable=self.puan_var)
        self.entry_puan.grid(row=0, column=1,columnspan=1)


        self.buton=tk.Button(frame,text="Ekle",command=self.urun_ekle)
        self.buton.grid(row=0, column=4,padx=10)


        self.urunler_listbox = tk.Listbox(frame, bg = "white",exportselection=0,height=5,width=40)
        self.urunler_listbox.grid(row=0, column=6)


        self.adet_var=tk.IntVar()
        self.entry_oneri_adedi=tk.Entry(frame,textvariable=self.adet_var)
        self.entry_oneri_adedi.grid(row=8,column=1)

        label_adet = tk.Label(frame, text='Toplam Oneri Adedi:')
        label_adet.grid(row=8,column=0)
        
        label_ayarlar=tk.Label(frame,text="<<<< Ayarlar >>>>",fg="blue",bg="grey",font="Times 22 bold")
        label_ayarlar.grid(row=8,column=6)

        label_model=tk.Label(frame,text="Oneri Modeli:",fg="blue",font="Times 12 bold")
        label_model.grid(row=9,column=6)


        modeller=[("Kullanici Bazli","Kullanici Bazli"),("Urun Bazli","Urun Bazli")]
        self.v=tk.StringVar()
        for model,val in modeller:
            self.rbutton1=tk.Radiobutton(frame,text=model,value=val,variable=self.v).grid(column=6)
            print(self.v.get())
        
        label_benzerlik=tk.Label(frame,text="Benzerlik Olcutu:",fg="blue",font="Times 12 bold")
        label_benzerlik.grid(row=12,column=6)

        olcutler=[("Euclidan","Euclidan"),("Pearson","Pearson"),("Jaccard","Jaccard")]
        self.v2=StringVar()
        for olcut,val in olcutler:
            self.rbuton=tk.Radiobutton(frame,text=olcut,value=val,variable=self.v2).grid(column=6)

        oneri_butonu=tk.Button(frame,text="Oneri Al",command=self.onerial)
        oneri_butonu.grid(row=18,column=0,columnspan=1)
        self.oneri_listbox = tk.Listbox(frame, bg = "white",exportselection=0,width=60)
        self.oneri_listbox.grid(row=19, column=0)

        benzer_mus_butonu=tk.Button(frame,text="Benzer Musterileri Listele",command=self.kullanicibazlial)
        benzer_mus_butonu.grid(row=18,column=6,columnspan=1)
        self.benzer_mus_listbox = tk.Listbox(frame, bg = "white",exportselection=0,width=60)
        self.benzer_mus_listbox.grid(row=19, column=6)





    def urun_ekle(self):
        for i in self.db_urun:
                    urunstringi2="{} --->  {}".format(bytes.decode(i),bytes.decode(self.db_urun[i]))
                    self.urunler_listbox.insert(tk.END,urunstringi2)
        self.urunler_listbox.delete(0,tk.END)
        
        self.sozluk_degerlendirmelerim={}
        puan=self.entry_puan.get()
        if (not self.listbox_kategori.curselection()):
            pass
        else:
            if 0<=float(puan)<=10:
                self.db_urun[self.listbox_kategori.get(self.listbox_kategori.curselection())]=self.entry_puan.get()

        for i in self.db_urun:
                    urunstringi2="{} --->  {}".format(bytes.decode(i),bytes.decode(self.db_urun[i]))
                    self.urunler_listbox.insert(tk.END,urunstringi2)        
                

        
        for i in self.db_urun:
            self.sozluk_degerlendirmelerim[bytes.decode(i)]=float(bytes.decode(self.db_urun[i]))
            self.diger_kullanıcılar["kullanici"]=self.sozluk_degerlendirmelerim    
        print(self.sozluk_degerlendirmelerim)


    def onerial(self):
        self.oneri_listbox.delete(0,tk.END)
        if self.v.get()=="Kullanici Bazli":
            messagebox.showerror(title="Hata",message="<<<Benzer Musterileri Listele>>> Butonuna Basmalısınız!")
            return
        elif self.v.get()=="Urun Bazli":
            self.oneri_listbox.insert(0,"Skor --> Oneri")
            #benzer oneri listboxa return degerler aktarilacak
            for i,k in self.urunbazliarama():
                
                oneristringi="  {}   -->  {}".format(i,k)
                self.oneri_listbox.insert(tk.END,oneristringi)
            
    def kullanicibazlial(self):
        self.benzer_mus_listbox.delete(0,tk.END)
        if self.v.get()=="Urun Bazli":
            messagebox.showerror(title="Hata",message="<<<Oneri Al>>> Butonuna Basmalısınız!")
            return
        elif self.v.get()=="Kullanici Bazli":
            self.benzer_mus_listbox.insert(0,"Benzerlik --> Kisi")
            #benzer oneri listboxa return degerler aktarilacak
            for i,k in self.kullanicibazliarama():
                
                oneristringi="  {}   -->  {}".format(i,k)
                self.benzer_mus_listbox.insert(tk.END,oneristringi)
        
        
            



    def urunbazliarama(self):
        if self.v2.get()=="Pearson":
            
            return topMatches(self.diger_kullanıcılar,"kullanici",float(self.entry_oneri_adedi.get()),sim_pearson)
        elif self.v2.get()=="Euclidan":
            return topMatches(self.diger_kullanıcılar,"kullanici",float(self.entry_oneri_adedi.get()),sim_distance)
        elif self.v2.get()=="Jaccard":
            return topMatches(self.diger_kullanıcılar,"kullanici",float(self.entry_oneri_adedi.get()),sim_jaccard)
        
        

        
        
    def kullanicibazliarama(self):
        itemsim=calculateSimilarItems(self.diger_kullanıcılar)  
        return getRecommendedItems(self.diger_kullanıcılar,itemsim,"kullanici")
        
        
        
      
        



