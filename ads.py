import numpy as np
from config import SAMPLE_RATE
from util import down_eramp


def Ads(attack: float, decay: float, sustain: float):
    frames = yield np.array([])
    elapsed_frames = 0

    attack = round(attack * SAMPLE_RATE)
    decay = round(decay * SAMPLE_RATE)

    while True:
        parts = []
        remaining_frames = frames
        if elapsed_frames < attack:
            attack_frames = min(remaining_frames, attack - elapsed_frames)
            attack_samples = (
                np.arange(attack_frames) + elapsed_frames
            ) / attack  # Linear Attack
            parts.append(attack_samples)
            remaining_frames -= attack_frames
        if elapsed_frames + frames - remaining_frames < attack + decay:
            decay_frames = min(
                remaining_frames,
                attack + decay - (elapsed_frames + frames - remaining_frames),
            )
            decay_samples = (
                down_eramp(
                    (
                        np.arange(decay_frames)
                        + (elapsed_frames + frames - remaining_frames - attack)
                    )
                    / decay
                )
                * (1 - sustain)
                + sustain
            )
            parts.append(decay_samples)
            remaining_frames -= decay_frames
        if elapsed_frames + frames >= attack + decay:
            sustained_frames = remaining_frames
            sustained_samples = np.full(sustained_frames, sustain)
            parts.append(sustained_samples)
            remaining_frames = 0

        samples = np.hstack(parts)
        elapsed_frames += frames
        frames = yield samples


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    env = Ads(1, 1, 0.9)
    next(env)
    frames = SAMPLE_RATE // 10
    print(frames)
    parts = []
    for i in range(30):
        parts.append(env.send(frames))

    out = np.hstack(parts)
    t = np.arange(len(out)) / SAMPLE_RATE

    plt.plot(t, out)
    plt.show()
