import pyaudio
import numpy as np
import scipy as sp
import time
import datetime
import sqlite3 as sq
from .MainWindow import *
from scipy.signal import windows


class MicrophoneHandler:
    def __init__(self, channel=1, rate=48000, chunk=2048):

        # Audio Initialization
        self.RATE = rate
        self.CHUNK = chunk
        self.CHANNEL = channel
        self.audio = pyaudio.PyAudio()
        self.mic = self.audio.open(format=pyaudio.paInt16, channels=channel, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        self.table_name = None
        self.cursor = None
        self.db = None

    def database_init(self):
        self.db = sq.connect('state.db')
        self.cursor = self.db.cursor()
        now = datetime.datetime.now()
        self.table_name = "table_{}_{}_{}_{}_{}_{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        self.cursor.execute(f"CREATE TABLE {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, frequency FLOAT, timestamp FLOAT);")
        self.db.commit()

    def fourier(self, data):
        yf = sp.fft.fft(data)/self.RATE
        xf = sp.fft.fftfreq(self.CHUNK, 1 / self.RATE)
        # logger.info(f"xf: {len(xf)}, yf: {len(yf)}")
        return np.abs(xf), np.abs(yf)

    def read_stream(self):
        data = self.mic.read(self.CHUNK)
        return np.frombuffer(data, dtype=np.int16)

    def save_state(self, freq):
        self.cursor.execute(f'INSERT INTO {self.table_name} (frequency, timestamp) VALUES ({freq}, {time.time()})')
        self.db.commit()

    def close(self):
        self.db.close()
        self.mic.close()
