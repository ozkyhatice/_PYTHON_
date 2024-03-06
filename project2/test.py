from ExpenseManage import App
from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd 
import json
def main():
      
    root = tk.Tk()
    root.title("Harcama Raporu")
    root.geometry("500x500+300+300")
    App(root)
    root.mainloop()

main()