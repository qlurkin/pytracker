from audio_node import an
from sine_oscilator import sine_oscilator
from mixer import mixer, set_track
from engine import Engine

FREQUENCY = 440.0  # Hz (La4)

engine = Engine(an(mixer))

engine.start()

input("Appuyez sur Entrée pour arrêter...\n")

set_track(0, an(sine_oscilator, FREQUENCY))

input("Appuyez sur Entrée pour arrêter...\n")

set_track(1, an(sine_oscilator, FREQUENCY * 0.5))

input("Appuyez sur Entrée pour arrêter...\n")
engine.stop()
