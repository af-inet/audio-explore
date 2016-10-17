import pyaudio
import wave
import sys
import math
import pygame
import random
import time
import json
import struct

class Noise():

    SIZE = 128
    MAX = 4294967295
    RATE = 44100 / 2

    def update(self):
        pass

    def log(self, msg):
        print("NOISE: " + msg)

    # unpacks a string into a list of ints (string length should be divisible by 4, or something probably went wrong)
    ### pretty sure this only works for paInt32 TODO look into that 
    def decode(self, data):
        return map(lambda i: struct.unpack("I", data[i:i+4])[0], range(0, len(data), 4))

    # packs a list of ints into a string
    def encode(self, values):
        return b''.join(map(lambda i: struct.pack("I", i), values))

    # 1. Decodes a (paInt32) PCM buffer into a list of discrete samples.
    # 2. `cb` is mapped over the resulting sample list.
    # Sanity checks + rounding are performed to ensure the resulting buffer is valid.
    # 3. The result of step 2. is encoded back into a PCM buffer and returned.
    def process(self, data, cb):

        raw = self.decode(data)

        def safe_cb(n):
            
            self.delta += 0.01

            val = cb(n)

            if type(val) == float:
                val = int(val)

            if type(val) != int:
                raise TypeError("NOISE: Processer returned non-integer type: %s: %s" % (type(val), val))

            # TODO: look into why this is the MAX
            val = val % self.MAX

            return val
        
        processed = map(safe_cb, raw)

        compiled = self.encode(processed)

        return compiled

    def run(self):
        self.running = True

        while self.running:
            self.tick()
            # XXX Uncertain if sleep is useful here.
            #time.sleep(0.001)

    def tick(self):
        # XXX Uncertain if polling is useful here.
        if pygame.event.poll():
            pygame.event.pump()
        self.keys = pygame.key.get_pressed()
        self.update()
        self.ticks += 1

    # Stream of input from the default microphone device.
    def open_input(self):
        self.input = self.pa.open(
            format = pyaudio.paInt32,
            channels = 1,
            rate = self.RATE,
            input = True,
            frames_per_buffer = self.SIZE
        )

    # Streams output to the default speakers.
    def open_output(self):
        self.output = self.pa.open(
            format   = pyaudio.paInt32,
            channels = 1,
            rate     = self.RATE,
            output   = True
        )   

    def dump(self):

        device_count = self.pa.get_device_count()
        host_api_count = self.pa.get_host_api_count()
        version_text = pyaudio.get_portaudio_version_text()

        print((
            "\n# PORTAUDIO DUMP\n\n" +
            version_text       + "\n" +
            "device_count: %s" + "\n" +
            "api_count: %s"    + "\n"
            ) % 
            (device_count, host_api_count)
        )

        for i in range(0, device_count):
            info = self.pa.get_device_info_by_index(i)
            print(
                "device[%s]\n%s\n" % (i,json.dumps(info, indent=4))
            )

        for i in range(0, host_api_count):
            pass

    def __init__(self):

        # pygame.init()

        # pygame.joystick.init()
        # self.joy = pygame.joystick.Joystick(0)
        # self.joy.init()

        # wf = wave.open("beep.wav", 'rb')
        # wf.getnchannels()
        # wf.getframerate()
        # wf.getsampwidth()
        # wf.readframes()
        # wf.getnframes()
        # wf.close()
        
        # initialize a screen
        width = 400
        height = 300

        pygame.init()
        
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.update()

        # hopefully pygame's audio doesn't interfere
        pygame.mixer.quit()

        # storage for the keyboard state
        self.keys = []
        self.running = False

        self.pa = pyaudio.PyAudio()

        self.open_output()
        self.open_input()
        
        self.input.start_stream()
        self.output.start_stream()

        self.ticks = 0
        self.delta = 0

    def close(self):
        self.input.stop_stream()
        self.input.close()
        self.output.stop_stream()
        self.output.close()
        self.pa.terminate()
        pygame.display.quit()
        pygame.quit()

    def end(self):
        self.log("ending...")
        self.close()
        sys.exit(0)




