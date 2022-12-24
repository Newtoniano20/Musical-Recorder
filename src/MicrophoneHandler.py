import pyaudio
import numpy as np
import scipy as sp
import time
import logging

class MicrophoneHandler:
    def __init__(self, channel=1, rate=48000, chunk=2048):
        self.RATE = rate
        self.CHUNK = chunk
        self.CHANNEL = channel
        self.audio = pyaudio.PyAudio()
        self.mic = self.audio.open(format=pyaudio.paInt16, channels=channel, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

    def fourier(self, data):
        yf = sp.fft.fft(data)/self.RATE
        xf = sp.fft.fftfreq(self.CHUNK, 1 / self.RATE)
        # logging.info(f"xf: {len(xf)}, yf: {len(yf)}")
        return np.abs(xf), np.abs(yf)

    def read_stream(self):
        data = self.mic.read(self.CHUNK)
        return np.frombuffer(data, dtype=np.int16)

