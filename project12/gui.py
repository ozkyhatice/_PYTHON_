
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as tkst
from mp5fonk import *
from mp5fonk import crawler,printshelve
class App():
    
    def __init__(self,parent):
        
        self.parent=parent
        self.frame1=tk.Frame(self.parent,relief=tk.GROOVE,border=10)
        self.frame1.pack()
        self.frame2=tk.Frame(self.parent,relief=tk.GROOVE,border=10)
        self.frame2.pack(pady=10)
        self.frame3=tk.Frame(self.parent,relief=tk.GROOVE)
        self.frame3.pack(pady=10)
        self.frame4=tk.Frame(self.parent,relief=tk.GROOVE,border=10)
        self.frame4.pack(pady=10)
        self.Textbox = tkst.ScrolledText(self.frame4)
        self.Textbox.pack(side=tk.BOTTOM,pady=10)        
        self.endeksbutonu()
        self.kelimegir()
        self.arama_gui()
        
    def endeksbutonu(self):
        self.buton=tk.Button(self.frame1,text="Emeklemeyi Baslat",command=self.emekleme).pack(pady=10)
    def emekleme(self):
        crawler_=crawler(dbtables)
        crawler_.createindextables()
        crawler_.crawl(pagelist,2)

        self.Textbox.insert(tk.END,"Tarama ve Endeksleme Tamamlandi")
    def kelimegir(self):
        self.label1=tk.Label(self.frame2,text="Arama yapilacak kelime(ler)i girin:").grid(row=0)
        self.Textbox2 = tkst.ScrolledText(self.frame2,width=100,height=2)
        self.Textbox2.grid(row=1)
        
        
    def arama_gui(self):
        val1=IntVar()
        val2=IntVar()
        val3=IntVar()
        self.cbuton=tk.Checkbutton(self.frame3,text="Kelime Frekansi",variable=val1,onvalue=1,offvalue=0).pack(pady=10)
        self.cbuton=tk.Checkbutton(self.frame3,text="Inbound Link",variable=val2,onvalue=1,offvalue=0).pack(pady=10)
        self.cbuton=tk.Checkbutton(self.frame3,text="PageRank",variable=val3,onvalue=1,offvalue=0).pack(pady=10)
        self.abuton=tk.Button(self.frame3,text="Ara",command=self.arama).pack(ipadx=50,padx=5)
        
    def arama(self):
        mysearchengine = searcher(dbtables)
        self.Textbox.delete(tk.END)
        #print(type(self.Textbox2.get(0.0,tk.END)))

        mysearchengine = searcher(dbtables)
        self.Textbox.delete(tk.END)
        print(type(self.Textbox2.get(0.0,tk.END)))
        try:
            
            x=self.Textbox2.get(0.0,tk.END)
            y=mysearchengine.query(x)
            
            self.Textbox.insert(tk.END,y)
            mysearchengine.close()            
        except AttributeError:
            messagebox.showerror(title="Hata",message="Lutfen arama yapilacak kelime(ler)i girin!")
        except IndexError:
            messagebox.showerror(title="Hata",message="Lutfen arama yapilacak kelime(ler)i girin!")
        except TclError:
            pass

