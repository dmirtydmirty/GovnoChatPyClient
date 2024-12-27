import tkinter as tk
import gui

# GUI
root = tk.Tk()
root.title("GovnoChatClient")
root.resizable(False, False)

gui.GUI(root)

root.mainloop()
