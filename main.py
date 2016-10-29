#!/bin/bash

from noise import Noise
import sys
import math
import random
import pygame
import wave

# take an array and make it behave like a ringbuffer / stream
class Ring():
    def __init__(self, array):
        self.array = array
        self.array_len = len(array)
        self.pos = 0
    def read(self):
        if self.pos < self.array_len:
            tmp = self.array[self.pos]
            self.pos = self.pos + 1
            return tmp
        else:
            # EOF
            self.pos = 0
            return self.array[self.pos]

VOLUME = 1000 * 1000 * 100 / 2
class MyNoise(Noise):

    def handle_stream_error_input(self, e):
        # At some point it would be nice to move error handling into the noise engine.
        if e.errno == -9981:
            print("ERROR: Input Overflow, ignoring...")
        elif e.errno == -9988:
            print("ERROR: Input Closed, attempting to reopen...")
            self.open_input()
        else:
            #print("Unknown IOError %s %s" % (e.errno, e.strerror))
            raise e

    def handle_stream_error_output(self, e):
        if e.errno == -9988:
            print("ERROR: Output Closed, attempting to reopen...")
            self.open_input()
        else:
            #print("Unknown IOError %s %s" % (e.errno, e.strerror))
            raise e

    def update(self):
        
        print("tick")

        def white_noise(n):

            self.delta += 0.001

            if self.keys[pygame.K_r]:
                self.delta = 0
            
            if self.keys[pygame.K_g]:
                self.delta += 0.01

            x = (random.random() * 4) * VOLUME * (10 + (math.cos(self.delta/100)) * 10)

            if self.keys[pygame.K_z]:
                x = x * (2+math.cos(self.delta / 100))

            if self.keys[pygame.K_x]:
                x = x + (VOLUME * (1+math.sin(self.delta / 20)) * 100)
                x = x * (x % 2)

            if self.keys[pygame.K_c]:

                if self.keys[pygame.K_f]:
                    self.delta -= 0.1
                else:
                    self.delta += ((random.random()) / 100000000)

                x = x + (math.cos(self.delta % 100) * 100 * math.tan(self.delta / 10000)) * VOLUME * 10

            if self.keys[pygame.K_v]:
                x = x * 2

            if self.keys[pygame.K_b]:
                x = x + ( (1+math.cos(self.delta + (n / 100))) + n * 200)

            return (n + (x/2))/10000

        def vocoder(n):
            x = n
            if self.keys[pygame.K_n]:
                x = x * 2
            return x

        def sample(n):
            x = n
            s = killer.read()
            if self.keys[pygame.K_s]:
                x = s
            if self.keys[pygame.K_a]:
                x = x * 2
            return (n * 0.5) + x

        data = None
        mic  = None

        data = map(lambda x: (white_noise(x)), range(0, self.SIZE))

        try:
            mic = self.decode(self.input.read(self.SIZE))

            if self.keys[pygame.K_m]:
                data = mic
                data = map(vocoder, data)

            #sys.stdout.write( b' '.join(map(str, map(ord, data))) )
        except IOError as e:
            self.handle_stream_error_input(e)
            return

        #if data is None:
        #    data = map(white_noise, range(0,len(mic)))
        #else:
        #    data = map(lambda x: (white_noise(x)), data)

        data = map(sample, data)
        data = map(lambda x: abs(int(x) % self.unpack_max), data)
        data = self.encode(data)

        try:
            self.output.write(data)
        except IOError as e:
            self.handle_stream_error_output(e)
            return

n = MyNoise()
killer = Ring(n.decode(n.readwave("./converted/beep.wav")["data"]))
n.dump()
n.run()
n.end()

