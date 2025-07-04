import numpy as np
import sounddevice as sd

class PinkNoise:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.num_rows = 16
        self.num_columns = 1
        self.array = np.zeros((self.num_rows, self.num_columns))
        self.running_sum = np.zeros((self.num_columns,))
        self.rand = np.random.RandomState()
        self.mask = 0

    def _pink_noise(self, frames):
        output = np.zeros((frames, self.num_columns))
        for i in range(frames):
            k = 0
            self.mask += 1
            if self.mask >= (1 << self.num_rows):
                self.mask = 0
            while k < self.num_rows and ((self.mask >> k) & 1) == 0:
                k += 1
            if k < self.num_rows:
                self.array[k, :] = self.rand.uniform(-1, 1, (self.num_columns,))
            self.running_sum = np.sum(self.array, axis=0)
            output[i, :] = self.running_sum
        output = output / self.num_rows
        return output

    def play(self):
        print("Playing pink noise. Press Ctrl+C to stop.")
        try:
            def callback(outdata, frames, time, status):
                if status:
                    print(status)
                outdata[:] = self._pink_noise(frames)
            with sd.OutputStream(channels=1, callback=callback, samplerate=self.sample_rate):
                while True:
                    sd.sleep(1000)
        except KeyboardInterrupt:
            print("\nStopped.")
