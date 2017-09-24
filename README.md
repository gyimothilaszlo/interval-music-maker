# Music Maker for Interval Running
Adds countdowns to your interval training musics.

## Getting started
You should have Python 3 installed with the following packages:
pydub
tkinter

Use the pip tool to install pydub or tkinter:
```
pip install pydub
pip install tkinter
```

You can download Python from here:
https://www.python.org/downloads/release/python-362/

Pip is a command line tool that makes installing python modules really easy. The most convenient method for installing it is to use the get-pip.py script.
https://pip.pypa.io/en/stable/installing/

You should also create a "music/" folder with your songs that you would like to include in your interval training session. You can include songs in ".wav" or ".mp3" formats.
## Usage
To start the application, enter
```
python intervalMusicMaker.py
```
This command should open a GUI, where you can set an interval training plan. The structuring of the interval training is based on the interval training proposed by Jack Daniels in his book called Running Formula. You can set the number of repetitions for each duration, i.e. the number of repetitions you intend to do with the given duration. The recovery factor sets the time for recovery period simply by multiplying the corresponding work-length with this constant (e.g. 0.5 means you rest half as long as you do your interval-speed running). When you are done, press the "Create Music" button. The program calculates the required length of the music, and concatenates the songs in your "music/" folder randomly, adds countbacks ("10-5-4-3-2-1-RUN!, 10-5-4-3-2-1-relax!) to the generated music, and exports it as "interval.mp3".
<img src = "https://github.com/gyimothilaszlo/interval-music-maker/blob/master/gui_ex.JPG" width = "200">

Have a good interval session!

## Authors

* **Laszlo Gyimothi** - (https://github.com/gyimothilaszlo)
