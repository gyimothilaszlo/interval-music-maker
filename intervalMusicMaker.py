from os import listdir
from random import shuffle
from os.path import isfile, join
from tkinter import *
from pydub import *
from AudioMerger import *


class GUI:
	colors = ["#7f6012","#997316","#b28719", "#cc9a1d","#e5ad21","#ffc125"]
	bgcolor = "AntiqueWhite2"
	def __init__(self, master, worklengths):
		self.repeats=[]
		self.recoveryFactor = 0.5
		self.entryfields=[]
		self.master = master
		self.master.configure(background=self.bgcolor)
		
		Label(text="Interval Music Maker", font=("Helvetica", 16), bg =self.bgcolor).grid(row=0,columnspan=2, padx = 5, pady = 5)
		Label(text="Work lengths", font=("Verdana", 13), relief=RIDGE,bg ="azure2", width = 15).grid(row=1,column=0)
		Label(text="Repeats", font=("Verdana", 13), relief=RIDGE,bg ="azure3", width=10).grid(row=1,column=1)
		r = 2	
		for wl, col in zip(worklengths, self.colors):
			Label(text=str(wl) + " sec", bg=col,  font=("Verdana", 13), relief=RIDGE,width=15).grid(row=r,column=0)
			e=Entry(relief=SUNKEN,width=10, font=("Courier New", 13))
			e.grid(row=r,column=1)
			self.entryfields.append(e)
			r = r + 1
		Label(text="recovery factor", bg="saddle brown",  font=("Verdana", 13), relief=RIDGE,width=15).grid(row=r,column=0)
		self.recovEntryField=Entry(relief=SUNKEN,width=10, font=("Courier New", 13))
		self.recovEntryField.grid(row=r, column=1, pady = 10)
		self.recovEntryField.insert(0, "0.5")
		r = r + 1
		Button(text="Create Music", height=1, width=14, fg="white", bg="RoyalBlue4", justify=CENTER, font=("Verdana", 13), command=self.callback).grid(row=r, columnspan = 2, padx=5, pady=5)

	def callback(self):
		self.repeats=[int(e.get()) if (len(e.get()) and e.get().isdigit()) else 0 for e in self.entryfields]
		if (self.recovEntryField.get().replace('.','',1).isdigit()):
			self.recoveryFactor = float(self.recovEntryField.get())
		if  (sum(self.repeats) > 0):
			self.master.destroy()
	
class IntervalMusicCreator:
	ofsetSeconds = 10
	def __init__ (self, worklengths, worklengthRepeats, recovFactor, path = "music/"):
		self.worklengthRepeats = worklengthRepeats
		self.worklengths = worklengths
		self.recoveryFactor = recovFactor
		self.musicpath = path
		
		self.recoverylengths = [self.recoveryFactor * i for i in self.worklengths]

	def run(self):
		self.calculateStartEndTimes()
		self.createBgMusic()
		self.createIntervalMusic()
	def calculateStartEndTimes(self):		
		self.startTimes = [self.ofsetSeconds]
		self.endTimes = []
		for i in range(len(self.worklengths)):
			j = 0
			while j < self.worklengthRepeats[i]:
				self.endTimes.append(self.startTimes[-1] + self.worklengths[i])
				self.startTimes.append(self.endTimes[-1] + self.recoverylengths[i])
				j += 1
		self.startTimes.pop()
		self.totalTime = self.endTimes[-1]
	def createBgMusic(self):
		musicfiles = [f for f in listdir(self.musicpath) if (f.endswith('.mp3') or f.endswith('.wav'))]
		if (len(musicfiles) == 0):
			print("Error: no music files found in the " + self.musicpath + " folder")
			return

		shuffle(musicfiles)
		self.music = AudioSegment.empty()
		musicIdx, musicNum, musiclength = 0, 0, 0
		while musiclength < self.totalTime:
			self.music += AudioSegment.from_file(join(self.musicpath,musicfiles[musicIdx]))
			musiclength = len(self.music) / 1000
			musicNum = musicNum + 1
			musicIdx = musicNum % len(musicfiles)

		print("total music length: ", str(int(musiclength // 60)) + " minutes, " + str(round(musiclength % 60)) + " seconds")
		print("number of songs: ", musicNum)
	def createIntervalMusic(self):
		am = AudioMerger(self.music)
		for start, end in zip(self.startTimes, self.endTimes):
			am.addCountBack(start, True)
			am.addCountBack(end, False)
		am.exportMusic("interval")
		

worklengths = [300, 180, 120, 90, 60, 30]
root = Tk()
gui = GUI(root, worklengths)
root.mainloop()

worklengthRepeats = gui.repeats
recovFactor = gui.recoveryFactor
print("submitted: ", worklengthRepeats)
print("recoveryFactor: ", recovFactor)

imc = IntervalMusicCreator(worklengths, worklengthRepeats, recovFactor)
imc.run()
