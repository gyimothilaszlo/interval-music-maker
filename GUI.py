from os import listdir
from random import shuffle
from tkinter import *
from pydub import *

class GUI:
	colors = ["#7f6012","#997316","#b28719", "#cc9a1d","#e5ad21","#ffc125"]
	bgcolor = "AntiqueWhite2"
	def __init__(self, master, worklengths):
		self.repeats=[]
		self.recoveryFactor = 0.5
		self.entryfields=[]
		self.master = master
		self.master.configure(background=self.bgcolor)

		Label(text = "Interval Music Maker", font=("Helvetica bold", 16), bg = self.bgcolor).grid(row = 0, columnspan = 2, padx = 5, pady = 5)
		Label(text = "Work lengths", font = ("Verdana", 13), relief = RIDGE,fg = "white", bg = "saddle brown", width = 15).grid(row = 1, column = 0)
		Label(text = "Repeats", font = ("Verdana", 13), relief = RIDGE,fg="white", bg = "saddle brown", width = 10).grid(row = 1, column = 1)
		rowIdx = 2
		for wl, col in zip(worklengths, self.colors):
			Label(text = str(wl) + " sec", bg = col,  font = ("Verdana", 13), relief = RIDGE, width = 15).grid(row = rowIdx, column = 0)
			e=Entry(relief = SUNKEN, width = 10, font = ("Courier New", 13))
			e.grid(row = rowIdx,column = 1)
			self.entryfields.append(e)
			rowIdx += 1
		Label(text = "recovery factor", fg = "white", bg = "saddle brown",  font = ("Verdana", 13), relief = RIDGE, width = 15).grid(row = rowIdx, column = 0)
		self.recovEntryField=Entry(relief = SUNKEN, width = 10, font = ("Courier New", 13))
		self.recovEntryField.grid(row = rowIdx, column = 1, pady = 10)
		self.recovEntryField.insert(0, "0.5")
		rowIdx += 1
		Button(text = "Create Music", height = 1, width = 14, fg = "white", bg = "RoyalBlue4", justify = CENTER, font = ("Verdana", 13), command = self.callback).grid(row = rowIdx, columnspan = 2, padx = 5, pady = 5)

	def callback(self):
		self.repeats=[int(e.get()) if (len(e.get()) and e.get().isdigit()) else 0 for e in self.entryfields]
		if (self.recovEntryField.get().replace('.', '', 1).isdigit()):
			self.recoveryFactor = float(self.recovEntryField.get())
		if  (sum(self.repeats) > 0 and (self.recoveryFactor > 0)):
			self.master.destroy()
