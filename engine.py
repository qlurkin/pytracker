import miniaudio
import numpy as np
from audio_node import AudioNode
from zero import ZERO
from config import SAMPLE_RATE


class Engine:
    def __init__(self, node: AudioNode | None = None):
        self.set_node(node)
        self.__device = miniaudio.PlaybackDevice(
            output_format=miniaudio.SampleFormat.FLOAT32,
            sample_rate=SAMPLE_RATE,
            nchannels=1,
        )

    def set_node(self, node: AudioNode | None = None):
        if node is None:
            node = ZERO
        self.__node: AudioNode = node

    def start(self):
        def noise_maker():
            frames = yield b""

            while True:
                frames = yield self.__node.send(frames).astype(np.float32).tobytes()

        noise = noise_maker()
        next(noise)

        self.__device.start(noise)

    def stop(self):
        self.__device.stop()
