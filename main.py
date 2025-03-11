from audio_node import an
from sine_oscilator import sine_oscilator
from mixer import mixer, set_track
from engine import Engine

FREQUENCY = 440.0  # Hz (La4)

mix = an(mixer)

engine = Engine(mix)

engine.start()

input("Appuyez sur Entrée pour arrêter...\n")

sine = an(sine_oscilator, FREQUENCY)

set_track(0, sine)

input("Appuyez sur Entrée pour arrêter...\n")

sine = an(sine_oscilator, FREQUENCY * 0.5)

set_track(1, sine)

input("Appuyez sur Entrée pour arrêter...\n")
engine.stop()
