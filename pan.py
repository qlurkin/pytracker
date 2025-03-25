from audio_node import AudioNode
import numpy as np


def Pan(node: AudioNode, pan_node: AudioNode) -> AudioNode:
    frames = yield np.array([])

    while True:
        samples = 2 * node.send(frames)
        left = pan_node.send(frames)
        right = 1.0 - left
        frames = yield np.vstack([left * samples, right * samples])


if __name__ == "__main__":
    from sine_oscilator import SineOscilator
    from value import Value
    from audio_node import an
    from matplotlib import pyplot as plt
    from config import SAMPLE_RATE

    sine = an(SineOscilator(55))
    value = an(Value(0.0))
    value.set_value(1.0)

    pan = an(Pan(sine, value))

    res = pan.send(SAMPLE_RATE // 5)
    print(res)
    print(res.shape)

    t = np.arange(res.shape[1]) / SAMPLE_RATE

    plt.plot(t, res[0])
    plt.plot(t, res[1])

    plt.show()
