from noise import Noise
import sys
import math

class MyNoise(Noise):

    def update(self):

        try:
        
            data = self.input.read(self.SIZE)
           
            def proc(n):
                f = 200 + (math.cos(self.delta) * 200)
                r = int(f) * self.RATE * 1000
                return r

            data = self.process(data, proc)

            #sys.stdout.write( b' '.join(map(str, map(ord, data))) )

            self.output.write(data)

        except IOError as e: 

            # At some point it would be nice to move error handling into the noise engine.

            if e.errno == -9981:
                print("ERROR: Input Overflow, ignoring...")

            elif e.errno == -9988:
                print("ERROR: Input Closed, attempting to reopen...")
                self.open_input()

            else:
                print("Unknown IOError %s %s" % (e.errno, e.strerror))

            # Should leave this on while debugging, makes errors more obvious.
            # During production we'll try to survive errors as much as possible.
            n.end()
        

n = MyNoise()
n.dump()
n.run()
n.end()

