from pydub import *

class AudioMerger:
	voice_tags = ["one", "two", "three", "four", "five", "ten", "RUN", "relax", "completed"]

	def __init__(self, music):
		self.music = music
		self.additionalGain = 8
		self.voices={}
		for voice in self.voice_tags:
			sound = AudioSegment.from_file('voices/' + voice + '.wav')
			sound += self.additionalGain
			self.voices[voice] = sound

	def addCountBack(self, startTime, isRun = True):
		for i in range(1, 6):
			voice = self.voices[self.voice_tags[i - 1]]
			self.music = self.music.overlay(voice, position = (startTime - i) * 1000)
		self.music = self.music.overlay(self.voices["ten"], position = (startTime - 10) * 1000)

		if isRun:
			voice = self.voices["RUN"]
		else:
			voice = self.voices["relax"]
		self.music = self.music.overlay(voice, position = startTime * 1000)

	def addCompleted(self, startTimeSec):
		self.music = self.music.overlay(self.voices["completed"], position = (startTimeSec * 1000))

	def exportMusic(self, fname):
		self.music.export(fname + ".mp3", format="mp3")
