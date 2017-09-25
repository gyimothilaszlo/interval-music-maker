from os import listdir
from os.path import isfile, join
from random import shuffle
from tkinter import *
from pydub import *
from AudioMerger import *
from GUI import *

	
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
		print("songs: ", musicfiles[:min(musicNum,len(musicfiles))])
	def createIntervalMusic(self):
		am = AudioMerger(self.music)
		for start, end in zip(self.startTimes, self.endTimes):
			am.addCountBack(start, True)
			am.addCountBack(end, False)
		am.exportMusic("interval")

def printWorkout(worklengths, worklengthRepeats, recovFactor):
	print("Your workout:")
	for wl, rep in zip(worklengths, worklengthRepeats):
		for i in range(rep):
			print("Interval pace run for " + str(wl) + " seconds")
			print("Easy pace run for " + str(int(wl*recovFactor)) + " seconds")

worklengths = [300, 180, 120, 90, 60, 30]
root = Tk()
gui = GUI(root, worklengths)
root.mainloop()

worklengthRepeats = gui.repeats
recovFactor = gui.recoveryFactor
printWorkout(worklengths, worklengthRepeats, recovFactor)

imc = IntervalMusicCreator(worklengths, worklengthRepeats, recovFactor)
imc.run()
