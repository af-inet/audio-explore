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

    SIZE = 1024 / 2
    RATE = 44100
    SAMPLE_SIZE = pyaudio.paInt16
    WIDTH = 400
    HEIGHT = 300

    def update(self):
        pass

    def log(self, msg):
        print("NOISE: " + msg)

    # unpacks a string into a list of ints (string length should be divisible by 4, or something probably went wrong)
    ### pretty sure this only works for paInt32 TODO look into that 
    def decode(self, data):
        return map(
            lambda i:
                struct.unpack(self.unpack_format, data[i:i+self.unpack_size])[0],
            range(0, len(data), self.unpack_size)
        )

    # packs a list of ints into a string
    def encode(self, values):
        def pack(n):
            try:
                return struct.pack(self.unpack_format, n)
            except Exception as e:
                raise Exception("Couldn't struct.pack: %s" % n)
        return b''.join(map(pack, values))

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

            val = val % self.unpack_max

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
            format = self.SAMPLE_SIZE,
            channels = 1,
            rate = self.RATE,
            input = True,
            frames_per_buffer = self.SIZE
        )

    # Streams output to the default speakers.
    def open_output(self):
        self.output = self.pa.open(
            format = self.SAMPLE_SIZE,
            channels = 1,
            rate = self.RATE,
            output = True
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

    def readwave(self, filename):

        wf = wave.open(filename)
        result = []

        data = wf.readframes(32)
        while data:
            result.append(data)
            data = wf.readframes(32)

        channels = wf.getnchannels()
        framerate = wf.getframerate()
        samplewidth = wf.getsampwidth()
        result = b''.join(result)

        wf.close()

        return {
            "data": result,
            "framerate": framerate,
            "samplewidth": samplewidth,
            "channels": channels
        }

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
        
        pygame.init()
        # initialize a screen
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        # surface color rect width
        pygame.display.update()
        pygame.display.set_caption("Noise")

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

        # determine an appropriate encoding / decoding scheme
        self.unpack_size = None
        self.unpack_format = None
        if self.SAMPLE_SIZE == pyaudio.paInt16:
            self.unpack_size = 2
            self.unpack_format = "H"
        elif self.SAMPLE_SIZE == pyaudio.paInt32:
            self.unpack_size = 4
            self.unpack_format = "I"
        else:
            raise Exception("Unsupported SAMPLE_SIZE: %s" % self.SAMPLE_SIZE)

        self.unpack_max = (2 ** (self.unpack_size * 8))

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




