import os
import subprocess
from os.path import isfile, join
from random import shuffle
from time import sleep
from tkinter import *
from pydub import *
from pydub.utils import mediainfo
from printutils import *
from AudioMerger import *
from GUI import *

class IntervalMusicCreator:
	ofsetSeconds = 10
	chunkSizeSec = 300
	filename = "interval.mp3"
	def __init__ (self, worklengths, worklengthRepeats, recovFactor, path = "music/"):
		self.worklengthRepeats = worklengthRepeats
		self.worklengths = worklengths
		self.recoveryFactor = recovFactor
		self.musicpath = path
		self.recoverylengths = [self.recoveryFactor * i for i in self.worklengths]

	def run(self):
		self.calculateStartEndTimes()
		self.calculateChunkSplitTimes()
		self.createMusicList()
		self.createAllChunks()
		self.mergeChunks()
		self.removeChunks()

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

	def calculateChunkSplitTimes(self):
		self.chunkSplitTimes = []
		lastSplitTime = 0
		self.guardbandSec = 2
		for et in self.endTimes:
			if (et - lastSplitTime) > self.chunkSizeSec:
				lastSplitTime = et + self.guardbandSec
				self.chunkSplitTimes.append(lastSplitTime)
		self.chunkNum = len(self.chunkSplitTimes) + 1

	def createMusicList(self):
		self.musicChangeTimes = [0]
		musicfileNames = [join(self.musicpath,f) for f in listdir(self.musicpath) if (f.endswith('.mp3') or f.endswith('.wav'))]
		if (len(musicfileNames) == 0):
			print("Error: no music files found in the " + self.musicpath + " folder")
			return
		shuffle(musicfileNames)
		musicIdx, musicNum, musiclength = 0, 0, 0
		self.musicList = []
		while musiclength < self.totalTime:
			length = float(mediainfo(musicfileNames[musicIdx])["duration"])
			self.musicList.append(musicfileNames[musicIdx])
			musiclength += length
			musicNum += 1
			musicIdx = musicNum % len(musicfileNames)

	def createAllChunks(self):
		self.music = AudioSegment.empty()
		musicIdx = 0
		self.progress = 0
		self.logProgress(0)
		for i in range(self.chunkNum):
			self.finalChunk = (i == len(self.chunkSplitTimes))
			if self.finalChunk:
				self.chunklength = self.endTimes[-1] + self.guardbandSec
			else:
				self.chunklength = self.chunkSplitTimes[i]

			while len(self.music) < self.chunklength * 1000:
				self.music += AudioSegment.from_file(self.musicList[musicIdx])
				musicIdx += 1

			if self.finalChunk:
				chunk = self.music
			else:
				chunk = self.music[:self.chunklength * 1000]
				self.music = self.music[self.chunklength * 1000:]

			self.logProgress(0.2)
			self.createSingleChunk(chunk, i)
			self.logProgress(0.2)
			self.updateTimes()

		self.createChunkTxt()

	def createSingleChunk(self, chunk, seqnum):
			am = AudioMerger(chunk)
			starts = list(s for s in self.startTimes if s < self.chunklength)
			ends = list(s for s in self.endTimes if s < self.chunklength)
			for s in starts:
				am.addCountBack(s, True)
				self.logProgress(0.3 / len(starts))
			for e in ends:
				self.logProgress(0.3 / len(ends))
				am.addCountBack(e, False)

			if self.finalChunk:
				am.addCompleted(ends[-1] + 1)
			am.music.export(self.musicpath + "chunk" + str(seqnum) + ".mp3", bitrate = "320k", format="mp3")

	def updateTimes(self):
			self.chunkSplitTimes = [ct - self.chunklength for ct in self.chunkSplitTimes]
			self.startTimes = [st - self.chunklength for st in self.startTimes if st > self.chunklength]
			self.endTimes = [et - self.chunklength for et in self.endTimes if et > self.chunklength]

	def createChunkTxt(self):
			file = open("chunks.txt", "w")
			for i in range(self.chunkNum):
				file.write("file '" + self.musicpath + "chunk" + str(i) + ".mp3'\n")
			file.close()

	def mergeChunks(self):
		try:
			os.remove(self.filename)
		except OSError:
			pass
		subprocess.call(['ffmpeg', '-loglevel', 'panic', '-f', 'concat', '-i', 'chunks.txt', '-c', 'copy', self.filename])

	def removeChunks(self):
		for i in range(self.chunkNum):
			os.remove(self.musicpath + "chunk" + str(i) + ".mp3")
		os.remove("chunks.txt")

	def logProgress(self, prog):
		self.progress += prog
		printProgressBar(self.progress, self.chunkNum, prefix = 'Progress:', suffix = 'Complete', length=50)


worklengths = [300, 180, 120, 90, 60, 30]
root = Tk()
gui = GUI(root, worklengths)
root.mainloop()

worklengthRepeats = gui.repeats
recovFactor = gui.recoveryFactor
printWorkout(worklengths, worklengthRepeats, recovFactor)

imc = IntervalMusicCreator(worklengths, worklengthRepeats, recovFactor)
imc.run()
