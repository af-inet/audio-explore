import pyaudio
import wave
import sys
import math
import pygame
import random
import time

pygame.init()
pygame.joystick.init()

clock = pygame.time.Clock()
j = pygame.joystick.Joystick(0) 
j.init()

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])

wf = wave.open(sys.argv[1], 'rb')
p = pyaudio.PyAudio()

format = p.get_format_from_width(wf.getsampwidth())
channels = wf.getnchannels()
rate = wf.getframerate() / 4


print("format: %s\nchannels: %s\nrate: %s\n" % (format,channels,rate))

stream = p.open(
    format   = format,
    channels = channels,
    rate     = rate,
    output   = True
)

#data = wf.readframes(CHUNK)

t = 0

SIZE = 1024

def gen():
    buf = bytearray(SIZE)
    
    for i in range(0, SIZE):
        global t
        t = t + 1
        if (i % 64) == 0:
            pygame.event.pump()
        f = j.get_axis(0)
        n = int( ( (f * (math.cos(( f * (t / 10) ) * 10) * 32)) ) % 255)
        print( str(n) )
        buf[i] = chr(n)

    return buffer(buf)

while False:
    data = gen()
    stream.write(data)
    time.sleep(0.001)
    #data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()
p.terminate()
