from audio_node import AudioNode
import numpy as np
from scipy.signal import butter, lfilter, lfilter_zi

from config import SAMPLE_RATE


def butter_bandpass(lowcut, highcut, order=5):
    nyq = 0.5 * SAMPLE_RATE
    low = lowcut / nyq
    high = highcut / nyq
    res = butter(order, [low, high], btype="band")
    assert isinstance(res, tuple)
    assert len(res) == 2
    b, a = res
    return b, a


def PassBand(node: AudioNode, lowcut, highcut, order=3) -> AudioNode:
    frames = yield np.array([])
    b, a = butter_bandpass(lowcut, highcut, order=order)
    zi_l = lfilter_zi(b, a) * 0.0
    zi_r = lfilter_zi(b, a) * 0.0

    while True:
        samples = node.send(frames)
        filtered_l, zi_l = lfilter(b, a, samples[0], zi=zi_l)
        filtered_r, zi_r = lfilter(b, a, samples[1], zi=zi_r)
        frames = yield np.vstack([filtered_l, filtered_r])
