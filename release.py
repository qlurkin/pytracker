import numpy as np
from config import SAMPLE_RATE
from util import down_eramp


def Release(release_time: float):
    frames = yield np.array([])
    elapsed_frames = 0

    release = round(release_time * SAMPLE_RATE)

    while True:
        parts = []
        remaining_frames = frames
        if elapsed_frames > release:
            break
        else:
            release_frames = min(remaining_frames, release - elapsed_frames)
            release_samples = down_eramp(
                (np.arange(release_frames) + elapsed_frames) / release
            )
            parts.append(release_samples)
            remaining_frames -= release_frames
            elapsed_frames += release_frames
        if remaining_frames >= 0:
            sustained_samples = np.full(remaining_frames, 0.0)
            parts.append(sustained_samples)
            elapsed_frames += remaining_frames

        samples = np.hstack(parts)
        frames = yield samples


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    env = Release(1)
    next(env)
    frames = SAMPLE_RATE // 10
    print(frames)
    parts = []
    try:
        for i in range(30):
            parts.append(env.send(frames))
    except StopIteration:
        pass

    out = np.hstack(parts)
    t = np.arange(len(out)) / SAMPLE_RATE

    plt.plot(t, out)
    plt.show()
