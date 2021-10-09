import numpy as np
import argparse
import sounddevice as sd
import datetime
import math
import sys
import queue
import calendar
import time

np.set_printoptions(threshold=sys.maxsize)


# Calibration function
def calibration(channelNumber, sampleRate):
    mySignal = sd.rec(int(5 * sampleRate), samplerate=sampleRate,
                      mapping=[channelNumber], dtype='float32', blocking=True)
    RMS = rms_flat(mySignal)
    return 1 / RMS


def rms_flat(a):  # from matplotlib.mlab
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return np.sqrt(np.mean(np.absolute(a) ** 2))


q = queue.Queue()


def audio_callback(indata, frames, time, status):
    q.put(indata.copy())


CF = calibration(1, 44100)


def getDB():
    with sd.InputStream(callback=audio_callback, blocksize=10000, samplerate=44100, dtype='float32'):
        data = q.get() / CF
        original = 20 * np.log10(rms_flat(data) / 2e-5)  # referencing 2e-5 Pa
        return '{:+.2f} dB'.format(original)
