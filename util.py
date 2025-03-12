def up_eramp(x):
    x = x - 1.0
    return 32**x + x / 32


def down_eramp(x):
    return 32 ** (-x) - x / 32


def up_lramp(x):
    return x


def down_lramp(x):
    return -x + 1
