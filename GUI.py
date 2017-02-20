from Tkinter import *
"""
Tk, Label, Button

"""

class tetrisGUI:


    def __init__(self, master):
        

        self.master = master
        master.title("Tetris GUI")


        master.minsize(width=400, height=400)
        self.label = Label(master, text="Tetris!", bg = "grey")
        self.label.pack()

        self.message_button = Button(master, text="Play!", fg = "red", bg = "blue", command=self.message)
        self.message_button.pack(side=BOTTOM)

        self.close_button = Button(master, text="Close", command=root.destroy)
        self.close_button.pack(side=BOTTOM)

    def message(self):
        print("Start game!")
        
root = Tk()
root.configure(background='grey')
my_gui = tetrisGUI(root)
root.mainloop()
