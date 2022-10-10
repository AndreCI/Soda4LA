import threading
import time
import tkinter
from collections import deque
from tkinter import ttk

import matplotlib as mpl
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import pi
from numpy.fft import fft


class GraphicalView(ttk.Frame):
    """
        Display a graph showing notes. supposed to use a moving red bar to reduce time redrawing canvas, but for some
        reason it is slower than redrawing notes. maybe after moving to pyqt5 it should be revisited.
        for now, the canvas is sliding and it works.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.verticalRes = 128
        self.horizontalRes = 1000
        self.updateFrequency = 100  # ms before redrawing
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

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)  # A tk.DrawingArea.
        self.canvas.draw()

        self.movingGraphThread = threading.Thread(target=self.moving_canvas, daemon=True)
        self.movingGraphThread.start()

        # pack_toolbar=False will make it easier to use a layout manager later on.
        # toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        # toolbar.update()

        # self.canvas.mpl_connect(
        #    "key_press_event", lambda event: print(f"you pressed {event.key}"))
        # self.canvas.mpl_connect("key_press_event", key_press_handler)

        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    def get_spec(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()

        dt = 10e-3
        self.time_var = np.arange(0, 20, dt)
        fscale = self.time_var / max(self.time_var)
        y = np.cos(2 * pi * 1e6 * self.time_var * fscale) + \
            (np.cos(2 * pi * 2e6 * self.time_var * fscale) * np.cos(2 * pi * 2e6 * self.time_var * fscale))
        # y *= np.hanning(len(y))
        yy = np.concatenate((y, ([0] * 10 * len(y))))

        # FFT of this
        Fs = 1 / dt  # sampling rate, Fs = 500MHz = 1/2ns
        n = len(yy)  # length of the signal
        k = np.arange(n)
        T = n / Fs
        frq = k / T  # two sides frequency range
        frq = frq[range(int(n / 2))]  # one side frequency range
        Y = fft(yy) / n  # fft computing and normalization
        Y = Y[range(int(n / 2))] / max(Y[range(int(n / 2))])

        first, Fs = self.get_data()
        print(first)
        first = first * 1
        print(first)
        print(len(first))
        # for i , f in enumerate(first):
        #     print("{}  {}".format(int(i/Fss), f))

        Pxx, freqs, bins, im = ax.specgram(first, Fs=Fs, NFFT=128, noverlap=0, scale_by_freq=False, mode="psd",
                                           scale="linear")
        self.line = im
        # self.line, = ax.plot(self.tself.time_var, 2 * np.sin(2 * np.pi * self.tself.time_var))
        # self.line, = plt.plot(self.tself.time_var, 2 * np.sin(2 * np.pi * self.tself.time_var))
        # ax = plt.axis
        # fig = plt.figure
        ax.set_xlabel("time [s]")
        ax.set_ylabel("f(t)")
        return fig

    def draw_notes(self):
        data = np.zeros((self.verticalRes, self.horizontalRes))
        past_notes = []
        self.parent.ctrl.graphSemaphore.acquire()
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
            self.parent.ctrl.playingEvent.wait()  # wait if we are stopped
            self.parent.ctrl.pausedEvent.wait()  # wait if we are paused
            self.draw_notes()
            time.sleep(self.updateFrequency / 1000)

    def moving_bar(self):
        """legacy, unused"""
        while (True):
            if (self.parent.ctrl.playing):
                self.movingBarPos += self.timeStep
                if (self.movingBarPos >= self.horizontalRes):
                    self.movingBarPos = 0  # int(0.2 * self.hresolution)
                    self.draw_notes()
                self.movingBar.set_data([self.movingBarPos, self.movingBarPos], [0, 1])
                self.canvas.draw()
            time.sleep(self.updateFrequency / 1000)

    def setup(self, max_notes, time_window=10000, update_freq=100):
        self.timeWindow = time_window
        self.updateFrequency = update_freq
        step = self.horizontalRes / (self.timeWindow / 1000)
        self.timeStep = (self.updateFrequency) * step
        self.maxNotes = max_notes
        data = np.zeros((self.verticalRes, self.horizontalRes))
        self.line.set_array(data)
        self.canvas.draw()

    def reset(self):
        self.futureNotes.clear()
        data = np.zeros((self.verticalRes, self.horizontalRes))
        self.line.set_array(data)
        self.canvas.draw()
