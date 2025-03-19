import miniaudio
import numpy as np
from audio_node import AudioNode, an
from modulate import Modulate
from release import Release
from zero import ZERO
from config import SAMPLE_RATE, BUFFER_SIZE_MS
from time import sleep


class Device:
    def __init__(self, node: AudioNode | None = None):
        self.__node = ZERO
        self.__next_node: AudioNode | None = None
        self.set_node(node)
        self.__device = miniaudio.PlaybackDevice(
            output_format=miniaudio.SampleFormat.FLOAT32,
            sample_rate=SAMPLE_RATE,
            buffersize_msec=BUFFER_SIZE_MS,
            nchannels=2,
            app_name="PyTracker",
        )

    def set_node(self, node: AudioNode | None = None):
        if node is None:
            node = ZERO
        self.__next_node = node

    def start(self):
        def noise_maker():
            frames = yield b""
            print(frames)

            while True:
                if self.__next_node is not None:
                    self.__node = self.__next_node
                    self.__next_node = None
                samples = self.__node.send(frames)
                samples = np.column_stack([samples, samples]).flatten()
                frames = yield samples.astype(np.float32).tobytes()

        noise = noise_maker()
        next(noise)

        self.__device.start(noise)

    def stop(self):
        self.set_node(an(Modulate(self.__node, an(Release(0.3)))))
        sleep(0.4)
        self.__device.stop()
