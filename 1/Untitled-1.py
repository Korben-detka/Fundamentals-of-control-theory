from tkinter import *
import customtkinter as CTk

class App(CTk.CTk):
  def __init__(self):
    super().__init__()

if __name__ == "__main__":
  app = App()
  app.mainloop

# root = Tk()
# var = StringVar()
# label = Label (root, textvariable=var)
# b     = Button(root,text="button",command=lambda:set_label(var))
# var.set("Hey!? How are you doing?")
# label.pack()
# b.pack()
# root.mainloop()
