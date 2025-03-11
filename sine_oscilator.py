import numpy as np
from audio_node import AudioNode
from config import SAMPLE_RATE


def sine_oscilator(frequency: float) -> AudioNode:
    frames = yield np.array([])
    phase = 0.0
    phase_increment = (2.0 * np.pi * frequency) / SAMPLE_RATE

    while True:
        samples = np.sin(phase + np.arange(frames) * phase_increment)
        phase = (phase + frames * phase_increment) % (2.0 * np.pi)
        frames = yield samples
