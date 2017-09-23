from tkinter import *
from tkinter import ttk
from pydub import *

class App:

	def __init__(self, master):
		
		frame = Frame(master, width=768, height=576)
		frame.pack()
		self.button = Button(frame, text="QUIT", height=1, width=15, fg="red", command=frame.quit)		
		self.button.pack()
		self.progress = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
		self.progress.pack()
	def say_hi(self):
		print("hi!")

root = Tk()
app = App(root)
root.mainloop()
root.destroy()
