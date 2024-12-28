import tkinter as tk
import gui

# GUI
root = tk.Tk()
root.title("GovnoChatClient")
root.geometry('')
root.resizable(False, False)
root.geometry('')

gui.GUI(root)

root.mainloop()
