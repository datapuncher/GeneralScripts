#!/usr/bin/python

from tkinter import *
import tkinter as tk
from tkinter import filedialog

def take_inputs():
    prefix='ATOM   0001  C   OMG'
    chain=str_var1.get()
    residues=str.split(str_var2.get())
    rgbcode=str.split(str_var3.get())
    red=str(round(int(rgbcode[0])/256,3))
    green=str(round(int(rgbcode[1])/256,3))
    blue=str(round(int(rgbcode[2])/256,3))
    
    for i in range(len(residues)):
        output.append((prefix+chain.rjust(2)+residues[i].rjust(4)+red.rjust(12)+green.rjust(8)+blue.rjust(8)))
    return(output)

def print_text():
    result=take_inputs()
    for i in range(len(result)):
        print(result[i])
    print("\n")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as f:
            f.write(output.get("1.0", tk.END))

root = Tk()

str_var1 = StringVar(root)
str_var2 = StringVar(root)
str_var3 = StringVar(root)

root.title('RIVEM Color Code Generator')
Label(root, text='Chain :').grid(row=0)
Label(root, text='Residues :').grid(row=1)
Label(root, text='RGB code :').grid(row=2)
e1 = Entry(root, textvariable=str_var1)
e2 = Entry(root, textvariable=str_var2)
e3 = Entry(root, textvariable=str_var3)
e1.grid(row=0, column=1, columnspan = 4, pady = 2)
e2.grid(row=1, column=1, columnspan = 4, pady = 2)
e3.grid(row=2, column=1, columnspan = 4, pady = 2)

output=[]

b1 = Button(root, text='Show', command=print_text)
b2 = Button(root, text='Continue', command=lambda: [take_inputs, e1.delete(0, END), e2.delete(0, END), e3.delete(0, END)])
b3 = Button(root, text='Save', command=save_file)
b4 = Button(root, text='Quit', command=root.destroy)

b1.grid(row = 3, column = 1, sticky = E)
b2.grid(row = 3, column = 2, sticky = E)
b3.grid(row = 3, column = 3, sticky = E)
b4.grid(row = 3, column = 4, sticky = E)

save_file(output)

root.mainloop()
