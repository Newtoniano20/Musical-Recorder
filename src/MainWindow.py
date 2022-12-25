import threading

from PyQt5 import QtWidgets, QtCore, QtGui
from .MicrophoneHandler import MicrophoneHandler
from .Plot import *
import time
import numpy as np
import json
from .LogsHandler import *

logger = init()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        start_time = time.time()
        super(MainWindow, self).__init__(*args, **kwargs)
        # Constant Variables:
        self.CHUNK = 2048*3
        self.RATE = 48000

        self.max_value_index = 0
        self.max_frequency = 0

        self.stop = False

        # Creating Both Widgets and their distribution
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.graphWidget = MplCanvas(self, width=5, height=4, dpi=100)
        self.buttonWidget = QtWidgets.QWidget()

        # Init Mic:
        self.mic = MicrophoneHandler(chunk=self.CHUNK, rate=self.RATE)

        # Plot Widget:
        self.xdata = np.arange(self.CHUNK)
        self.y = self.mic.read_stream()
        logger.info("Opening Plot Window")
        time.sleep(2)

        # Button Widget
        self.note_box = QtWidgets.QLabel(self.buttonWidget)
        self.note_box.setText("Mic not detected")
        self.note_box.setFont(QtGui.QFont('Arial font', 20))
        self.note_box.setAlignment(QtCore.Qt.AlignCenter)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.note_box)
        self.buttonWidget.setLayout(vbox)

        # Add both widgets to the splitter
        splitter.addWidget(self.buttonWidget)
        splitter.addWidget(self.graphWidget)

        # Styling
        css_file = QtCore.QFile("./src/main.css")
        css_file.open(QtCore.QFile.ReadOnly)
        css = QtCore.QTextStream(css_file).readAll()
        self.setStyleSheet(css)

        self.setCentralWidget(splitter)

        # Setting up notes:
        with open('./src/notes.json') as f:
            self.notes = json.load(f)
            self.freq = []
            for key, value in self.notes.items():
                self.freq.append(float(key))
            # logger.info(f"Imported Notes from file: {notes}")
        logger.info(f"Initialization Finished in {time.time() - start_time}")

        self.update_thread = threading.Thread(target=self.update, args=[])
        self.update_thread.start()

    def closeEvent(self, event):
        logger.info("Shutting Down signal received")
        self.stop = True
        self.update_thread.join()
        event.accept()

    def update(self):
        self.mic.database_init()
        while not self.stop:
            # start_time = time.time()

            self.y = self.mic.read_stream()
            # logger.info(f"Read Data from Microphone")

            self.xdata, self.y = self.mic.fourier(self.y)
            # logger.info(f"Fourier Transform Applied")

            self.max_value_index = np.argmax(self.y)
            self.max_frequency = self.xdata[self.max_value_index]
            self.graphWidget.axes.cla()  # Clear the canvas.
            self.graphWidget.axes.plot(self.xdata, self.y, 'r')
            # logger.info(f"Plot Configured and Ready")

            # Trigger the canvas to update and redraw.
            self.graphWidget.draw()
            # logger.info(f"Plot Drawn")
            self.mic.save_state(self.max_frequency)
            if self.max_frequency > self.freq[-1]:
                logger.warning(f"Max frequency exceeded")
                self.note_box.setText(str(self.max_frequency) + "hz")
                time.sleep(0.05)
            else:
                n = 0
                past_freq = 0
                next_freq = self.freq[1]
                for key, value in self.notes.items():
                    # print(f"key : {key} / value: {value}")
                    upper = (next_freq + float(key))/2
                    bottom = (past_freq + float(key))/2
                    if bottom < self.max_frequency < upper:
                        # logger.info(f"Executed  with upper:{upper} & bottom {bottom}")
                        self.note_box.setText(value)
                        break
                    n += 1
                    try:
                        next_freq = self.freq[n+1]
                        past_freq = float(key)
                    except IndexError:
                        pass
                # logger.info(f"Time Spent Update Function: {time.time() - start_time}")
                time.sleep(0.05)
        self.mic.close()
