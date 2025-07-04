import argparse
from white_noise import WhiteNoise
from pink_noise import PinkNoise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Noise generator")
    parser.add_argument("type", choices=["white", "pink"], help="Type of noise to play")
    args = parser.parse_args()

    if args.type == "white":
        WhiteNoise().play()
    elif args.type == "pink":
        PinkNoise().play()
import argparse
import sounddevice as sd
import numpy as np

SAMPLE_RATE = 44100  # Hertz

class WhiteNoise:
    def callback(self, outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = np.random.uniform(-1, 1, (frames, 1))

class PinkNoise:
    def __init__(self):
        self.num_rows = 16
        self.num_columns = 1
        self.array = np.zeros((self.num_rows, self.num_columns))
        self.running_sum = np.zeros((self.num_columns,))
        self.rand = np.random.RandomState()
        self.mask = 0
    def pink_noise(self, frames):
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
    def callback(self, outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = self.pink_noise(frames)

def main():
    parser = argparse.ArgumentParser(description="Play white or pink noise until stopped.")
    parser.add_argument('type', choices=['white', 'pink'], help='Type of noise to play')
    args = parser.parse_args()
    if args.type == 'white':
        noise = WhiteNoise()
    else:
        noise = PinkNoise()
    print(f"Playing {args.type} noise. Press Ctrl+C to stop.")
    try:
        with sd.OutputStream(channels=1, callback=noise.callback, samplerate=SAMPLE_RATE):
            while True:
                sd.sleep(1000)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
