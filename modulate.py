from audio_node import AudioNode
import numpy as np


def Modulate(node1: AudioNode, node2: AudioNode) -> AudioNode:
    frames = yield np.array([])

    while True:
        samples = node1.send(frames) * node2.send(frames)
        frames = yield samples
