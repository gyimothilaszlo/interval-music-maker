from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from math import *

sound = AudioSegment.from_file('music/darude.mp3')

ratio = 180 / 136
faster_sound = sound.speedup(playback_speed=ratio)
faster_sound.export("music/estspedup.mp3", format="mp3")
# shift the pitch up by half an octave (speed will increase proportionally)

new_sample_rate = int(sound.frame_rate * ratio)

# keep the same samples but tell the computer they ought to be played at the 
# new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
chipmunk_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

# now we just convert it to a common sample rate (44.1k - standard audio CD) to 
# make sure it works in regular audio players. Other than potentially losing audio quality (if
# you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
chipmunk_ready_to_export = chipmunk_sound.set_frame_rate(44100)

chipmunk_ready_to_export.export("music/spedup.mp3", format="mp3")