# Music Maker for Interval Running
Create your own, personalized interval training music! Provided that you do time-based interval training (rather than distance-based one), this program can add countdowns to your musics at the right moments, so that you do not have to check your stopwatch all the time. The root folder includes an example output file ("example.mp3"), which can be used for the following interval workout:<br />
1 x 120 sec with 60 sec rest<br />
2 x 90 sec with 45 sec rest<br />
3 x 60 sec with 30 sec rest<br />
4 x 30 sec with 15 sec rest

## Getting started
You should have Python 3 installed with the following packages:
- pydub
- tkinter

You can download Python from here:
https://www.python.org/downloads/release/python-362/

Use the pip tool to install pydub or tkinter:
```
pip install pydub
pip install tkinter
```

Pip is a command line tool that makes installing python modules really easy. Note that pip is already installed if you're using Python 3 >=3.4 binaries downloaded from python.org, but you'll need to upgrade pip. The most convenient method for installing it is to use the get-pip.py script: https://pip.pypa.io/en/stable/installing/

Additionally - since pydub's memory handling for large audiofiles is somewhat problematic - you also need ffmpeg. You can download it from here: https://www.ffmpeg.org/download.html. I recommend using the static build corresponding to your OS. 

You should also create a "music/" folder with your songs that you would like to include in your interval training session. You can include songs in ".wav" or ".mp3" formats. These are the audio files the program concatenates during the process of creating the final music.

## Usage
To start the application, type the following command in your command prompt or terminal:
```
python intervalMusicMaker.py
```
This command should open a GUI, where you can set an interval training plan. The structuring of interval training is based on the interval training proposed by Jack Daniels in his book called Running Formula. You can set the number of repetitions for each duration, i.e. the number of repetitions you intend to do with the given duration. The recovery factor sets the time for recovery period simply by multiplying the corresponding work-length with this constant (e.g. 0.5 means you rest half as long as you do your interval-speed running). When you are done, press the "Create Music" button. The program calculates the required length of the music, and concatenates the songs in your "music/" folder randomly, adds countdowns ("10-5-4-3-2-1-RUN!", "10-5-4-3-2-1-relax!") to the generated music at the right positions, and exports it as "interval.mp3".

<img src = "https://github.com/gyimothilaszlo/interval-music-maker/blob/master/gui_ex.JPG" width = "200">

Have a good interval session!

## Remarks

The original version simply overlaid the countdown audio files on the concatenated music file at the appropriate positions. However, pydub has serious memory issues when handling large audio files, and the program crashed with MemoryError even for 20-minute-long interval musics. The workaround is to process the music by chunks, write these temporary chunks on disk, concatenate them with ffmpeg, and remove the temporary chunks. Is it cumbersome? Yes. Does it crash? Hopefully not anymore.

## Authors

* **Laszlo Gyimothi** - (https://github.com/gyimothilaszlo)
