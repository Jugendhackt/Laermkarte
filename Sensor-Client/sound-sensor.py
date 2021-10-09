import audioop
import math
import struct
import time

import pyaudio
from numpy import log10

CHUNK = 1024
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=CHUNK)


def test_decibels():
    while 1:
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)
        decibels = 20 * log10(rms)

        print("%.2f dB" % decibels)


def get_current_decibels():
    tries = 0
    while tries < 100:
        data = stream.read(CHUNK)
        tries += 1

    rms = audioop.rms(data, 2)
    decibels = 20 * log10(rms)
    return "%.2f" % decibels


#print(get_current_decibels())
#test_decibels()