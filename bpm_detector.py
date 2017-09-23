from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from math import *

seg = AudioSegment.from_file("music/darude.mp3")

# reduce loudness of sounds over 120Hz (focus on bass drum, etc)
seg = seg.low_pass_filter(120.0)

# we'll call a beat: anything above average loudness
beat_loudness = seg.dBFS 

# the fastest tempo we'll allow is 240 bpm (60000ms / 240beats)
minimum_silence = int(60000 / 240.0)

nonsilent_times = detect_nonsilent(seg, minimum_silence, beat_loudness)

spaces_between_beats = []
last_t = nonsilent_times[0][0]

for peak_start, _ in nonsilent_times[1:]:
    spaces_between_beats.append(peak_start - last_t)
    last_t = peak_start

# We'll base our guess on the median space between beats
spaces_between_beats = sorted(spaces_between_beats)
space = spaces_between_beats[floor(len(spaces_between_beats) / 2)]

bpm = 60000 / space
print("bpm: ", bpm)