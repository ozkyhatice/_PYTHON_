import tkinter as tk
from gui import *
def main():
    root = tk.Tk()
    root.configure(background="#444444")
    root.geometry("1000x800+100+100")
    root.title(("     "*25)+"Endeksleme ve Arama")
    app = App(root)
    root.mainloop()
    
main()