# Musical Recorder
#### Video Demo:  <URL HERE>
#### Description: 
This app will allow you to record yourself, but instead of saving everything your mic picks up as a normal recorder, it will only save the most prevalent frequency at a given time.

##### How to use it?
First of all you'll need a few python libraries that you should install, starting with PyQt5, used for the GUI. Install it by using
```
pip install PyQt5
```
Then, numpy, pyaudio and scipy should also be installed, which we'll use to record the audio with a microphone and convert it to pure frequencies.
```
pip install numpy pyaudio scipy
```
Finally, to save the recordings to our database, we'll use sqlite3 and scamp to replay those frequencies as musical notes.
```
pip install sqlite3 scamp
```

Now that we are ready to go, run the main.py file.
```
python main.py
```
This will open a terminal with some logging data and a GUI will pop up. This GUI will show two things:
1. The most prevalent frequency converted into a musical note with standard musical notation on your left.
2. A graph of all the frequencies that your mic is picking up.

While the GUI is opened, automatically all data will be saved into a table in our 'state.db' file with the following parameters:
```
+-----+------------+------------------+------------------+------------------+
| id  | frequency  |      power       |      noise       |    timestamp     |
+-----+------------+------------------+------------------+------------------+
| 1   | 125.0      | 90.9259719488391 | 7872.25835162099 | 1672083282.57073 |
| 2   | 507.8125   | 201.674539803027 | 18621.8431360341 | 1672083282.71883 |
| 3   | 148.4375   | 17.2443224080769 | 3557.32964678488 | 1672083282.82582 |
| 4   | 148.4375   | 4.44928782792174 | 3725.5177227318  | 1672083282.93092 |
| 5   | 531.25     | 6.69418054196415 | 4217.22099278236 | 1672083283.03401 |
| 6   | 460.9375   | 123.609397019073 | 9206.91488114472 | 1672083283.13023 |
```
- The frequency parameter is measured in hz and is the most prevalent frequency at that given time.
- The power parameter is measured in db and is the amplitude of that frequency.
- Noise doesn't have a measurement unit, it's a quantitative measurement of how many frequencies where present at a time. 
- The timestamp is what's called Epoch. Basically how much time has passed since January 1st 1970. We'll use that as our time measurement

This will be inside a table with a name containing the time when the GUI was opened.

After we have recorded some data, we can analyze it in different ways. I've written four scripts in the './scripts' folder, but many more could be created.

- Starting with 'amplitude_over_time.py', this script will plot our power parameter in our table against the timestamp of each row.
- Then, both 'frequencies_over_time.py' and 'noise_over_time.py' will do mostly the same, but instead of plotting power over time, they'll plot frequency over time and noise over time respectively.
- Lastly and the most interesting one is 'music_playback'. This script will use a python library called scamp which with a midi number can play any note on any instrument you want. As we have frequencies not midi numbers, we must convert them. This was done taking advantage of the order as shown inside the script.


#### What if I want to add or remove something?
This code was built with expandability in mind, so if for example you want to add a new note, you only need to add it to the './src/notes.json' folder, where all notes and frequencies are stored for this project.
The same goes for everything else, there is a way of changing every parameter without redesigning the code.

