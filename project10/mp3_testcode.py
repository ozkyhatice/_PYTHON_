from ProductRecommendationEngineGUI import *
from func import *
from cProfile import label
from distutils.spawn import spawn
from msilib.schema import ListBox
from pyparsing import col
import tkinter as tk
import dbm
import pickle 
from tkinter import *
from func import *
import math
def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    
main()