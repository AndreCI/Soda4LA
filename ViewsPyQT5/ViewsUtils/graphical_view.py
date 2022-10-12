import random
import threading
import time
from collections import deque

import numpy as np
import matplotlib as mpl
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    NavigationToolbar2QT as NavigationToolbar)

class GraphView():
    def __init__(self):
        self.GraphFrame = QFrame()
        self.GraphFrame.setObjectName(u"GraphFrame")
        self.GraphFrame.setFrameShape(QFrame.Panel)
        self.GraphFrame.setFrameShadow(QFrame.Raised)
        self.layout = QtWidgets.QVBoxLayout(self.GraphFrame)

        self.verticalRes = 128
        self.horizontalRes = 1000
        self.updateFrequency = 1000  # ms before redrawing
        self.timeWindow = 10000
        self.lookBackward = 0.2  # % of graph dedicated to past notes
        self.movingBarPos = int(self.lookBackward * self.horizontalRes)
        self.futureNotes = deque(maxlen=1000)
        self.maxNotes = None
        self.line = None
        self.timeStep = None

        self.colormap = mpl.colormaps['viridis'].resampled(128)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot()
        data = np.zeros((self.verticalRes, self.horizontalRes))
        self.line = self.ax.pcolormesh(data, cmap=self.colormap, rasterized=True, vmin=0, vmax=100)
        self.colorbar = self.figure.colorbar(self.line, ax=self.ax)
        self.ax.set_ylabel("value")
        self.ax.set_xlabel("time (seconds)")
        self.ax.set_xticklabels(np.arange(-2, 9, 2))
        self.movingBar = self.ax.axvline(x=self.movingBarPos, color="darkred")
        self.colorbar.ax.set_xlabel("volume")

        self.figure.subplots_adjust(
            top=0.98,
            #bottom=0.0,
            left=0.07,
            right=1.08,
            #hspace=0.2,
            #wspace=0.2
        )

        dynamic_canvas = FigureCanvas(self.figure)  # A tk.DrawingArea.
        dynamic_canvas.setMinimumSize(QSize(720, 300))

        self.layout.addWidget(dynamic_canvas)

        self.movingGraphThread = threading.Thread(target=self.moving_canvas, daemon=True)
        self.movingGraphThread.start()

    def draw_notes(self):
        data = np.ones((self.verticalRes, self.horizontalRes)) * random.randint(0,100) *  0

        self.line.set_array(data)
        self.line.figure.canvas.draw()

    def draw_notes__(self):
        data = np.zeros((self.verticalRes, self.horizontalRes))
        past_notes = []
        #self.parent.ctrl.graphSemaphore.acquire()
        for note in self.futureNotes:
            # time is seconds telling when the note will be played
            start_time = note.tfactor * self.parent.model.timeSettings.musicDuration - self.parent.ctrl.get_music_time() + 2
            note_timing = self.parent.ctrl.view.get_relative_note_timing(self.parent.ctrl.model.get_absolute_note_timing(note.tfactor))
            if (0 < start_time <= self.timeWindow / 1000 and note_timing > -2000):
                end_pos = min(int(self.horizontalRes * (start_time * 1000 + note.duration) / self.timeWindow), self.horizontalRes)
                start_pos = int(self.horizontalRes * (start_time * 1000) / self.timeWindow)
                max_vertical_pos = max(0, note.value + 1)
                min_vertical_pos = min(127, note.value - 1)
                gain = int(note.velocity * float(self.parent.model.tracks[note.channel].gain) / 128)
                data[min_vertical_pos:max_vertical_pos, start_pos:end_pos] = gain
            if (start_time < 0 or note_timing < -2000):
                past_notes.append(note)
        for note in past_notes:
            self.futureNotes.remove(note)
        self.parent.ctrl.graphSemaphore.release()
        self.line.set_array(data)
        self.canvas.draw()

    def moving_canvas(self):
        while (True):
            #self.parent.ctrl.playingEvent.wait()  # wait if we are stopped
            #self.parent.ctrl.pausedEvent.wait()  # wait if we are paused
            self.draw_notes()
            time.sleep(self.updateFrequency / 1000)
