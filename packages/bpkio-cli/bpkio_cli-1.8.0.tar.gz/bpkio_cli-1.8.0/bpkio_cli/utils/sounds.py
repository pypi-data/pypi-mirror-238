import os

import simpleaudio as sa

# Get directory containing this script file
here = os.path.dirname(os.path.realpath(__file__))


def chime_down():
    _chime("G4-C4")


def chime_up():
    _chime("C4-G4")


def chime_uphigh():
    _chime("C4-C5")


def chime():
    _chime("E4-E4")


def _chime(filename):
    file = os.path.join(here, f"../assets/{filename}.wav")
    wave_obj = sa.WaveObject.from_wave_file(file)
    play_obj = wave_obj.play()
    # play_obj.wait_done()  # Wait until sound has finished playing
