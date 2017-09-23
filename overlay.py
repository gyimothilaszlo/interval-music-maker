from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from math import *

sound1 = AudioSegment.from_file('music/darude.mp3')
sound2 = AudioSegment.from_file('music/180bpm.mp3')
sound2 = sound2.apply_gain(+12)

played_togther = sound1.overlay(sound2)
played_togther.export("music/mixed.mp3", format="mp3")