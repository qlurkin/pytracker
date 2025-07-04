import miniaudio
import numpy as np
from audio_node import AudioNode, an
from modulate import Modulate
from passband import PassBand
from release import Release
from zero import ZERO_STEREO
from config import SAMPLE_RATE, BUFFER_SIZE_MS
from time import sleep


class Device:
    def __init__(self, node: AudioNode | None = None):
        self.__node = ZERO_STEREO
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
            node = ZERO_STEREO

        self.__next_node = an(PassBand(node, 40, 18000))  # Protecion

    def start(self):
        def noise_maker():
            frames = yield b""

            while True:
                if self.__next_node is not None:
                    self.__node = self.__next_node
                    self.__next_node = None
                samples = self.__node.send(frames)
                samples = samples.T.flatten()
                samples = np.clip(samples, -1, 1)  # basic protection
                frames = yield samples.astype(np.float32).tobytes()

        noise = noise_maker()
        next(noise)

        self.__device.start(noise)

    def stop(self):
        self.set_node(an(Modulate(self.__node, an(Release(0.3)))))
        sleep(0.4)
        self.__device.stop()
