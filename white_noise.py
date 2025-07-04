import numpy as np
import sounddevice as sd

class WhiteNoise:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def play(self):
        print("Playing white noise. Press Ctrl+C to stop.")
        try:
            def callback(outdata, frames, time, status):
                if status:
                    print(status)
                outdata[:] = np.random.uniform(-1, 1, (frames, 1))
            with sd.OutputStream(channels=1, callback=callback, samplerate=self.sample_rate):
                while True:
                    sd.sleep(1000)
        except KeyboardInterrupt:
            print("\nStopped.")
