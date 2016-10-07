import pyaudio
import wave
import sys
import math
import pygame
import random
import time

# initialize joysticks
pygame.init()
pygame.joystick.init()
j = pygame.joystick.Joystick(0) 
j.init()

# initialize audio
p = pyaudio.PyAudio()

FORMAT   = 8
CHANNELS = 2
RATE     = 44100

# buffer size
SIZE = 1024

# open an audio stream
stream = p.open(
    format   = FORMAT,
    channels = CHANNELS,
    rate     = RATE,
    output   = True
)

t = 0
def gen():
    buf = bytearray(SIZE)
    
    for i in range(0, SIZE):
        global t

        t = t + 1

        if (i % 64) == 0:
            pygame.event.pump()

        f1 = math.fabs(j.get_axis(1)/10) * 10
        f2 = math.fabs(j.get_axis(3)/10) * 10

        n = int( (( f2 * (math.sin((10*t*f1*f2)/1000)+1) * 100)) % 256 )
        buf[i] = chr(n)

    print( ''.join(map(lambda b: "%0x" % b, buf)) )

    return buffer(buf)

while True:
    data = gen()
    stream.write(data)
    time.sleep(0.001)

stream.stop_stream()
stream.close()
p.terminate()
