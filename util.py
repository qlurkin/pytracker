from typing import Optional
import numpy as np
from config import SAMPLE_RATE
from tone import Tone


def up_eramp(x):
    x = x - 1.0
    return 32**x + x / 32


def down_eramp(x):
    return 32 ** (-x) - x / 32


def up_lramp(x):
    return x


def down_lramp(x):
    return -x + 1


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def get_freq(samples) -> float:
    freqs = np.fft.rfftfreq(len(samples), 1 / SAMPLE_RATE)
    sp = np.fft.rfft(samples)

    return float(freqs[np.argmax(np.abs(sp))])


def freq_to_tone(freq: float) -> Optional[Tone]:
    if freq == 0:
        return None
    n = 12 * np.log2(freq / 440)
    closest_n = round(n) + 9
    return Tone(closest_n % 12, 4 + closest_n // 12)


def float_to_hex(value: float | None, min: float, max: float) -> str:
    if value is None:
        return "--"
    if value < min:
        return "#U"
    if value > max:
        return "#O"
    v = round(255 * (value - min) / (max - min))
    return f"{v:0>2x}".upper()


if __name__ == "__main__":
    print(freq_to_tone(880))
    print(freq_to_tone(220))
    print(freq_to_tone(Tone(0, 5).frequency))
    print(float_to_hex(1, 0, 255))
    print(float_to_hex(255, 0, 255))
