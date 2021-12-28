import tkinter as tk

root = tk.Tk()
root.config(cursor="none")

status_menu = tk.Frame()
b1 = tk.Button(status_menu, text="Parked")
b2 = tk.Button(status_menu, text="Solved")
b3 = tk.Button(status_menu, text="Emergency")
b4 = tk.Button(status_menu, text="Found Out Order")

status_menu.pack()
b1.pack()
b2.pack()
b3.pack()
b4.pack()

root.mainloop()
