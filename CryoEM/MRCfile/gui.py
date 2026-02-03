#!/usr/bin/python

#simple GUI

from Tkinter import *

#create the window
root=Tk()

#modify root window
root.title("Image Viewer")
root.geometry("400x200")

app=Frame(root)
app.grid()

button1=Button(app,text="Button1")
button1.grid()

button2 = Button(app)
button2.grid()
button2.configure(text="This will show text")

button3=Button(app)
button3.grid()
button3["text"]="This will also show up"

#label=Label(app,text="This is a label!")
#label.grid()

#kick off the event loop
root.mainloop()
