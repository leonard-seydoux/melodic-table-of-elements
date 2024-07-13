"""Create the sounds to be played on hover over the element.

This script creates as many sounds as elements in the periodic table. Each
sound consists in a series of sine waves with different frequencies and
amplitudes. The basic idea is to create a sound that is unique for each
element, but that remain nice to the ear when multiple elements are played
together. 

All sounds are created from a multiple of the fundamental frequency. The fundamental frequency of an element is the product of the period and the fundamental frequency. The period is the row in which the element is located, and the fundamental frequency is a constant. The overtone is the product of the group and the fundamental frequency. The sound is a sine wave with the fundamental frequency, and additional sine waves with the overtone frequency. 

Several overtones are added depending on the block of the element. The d-block elements have one overtone, the f-block elements have two overtones, and the p-block elements have three overtones. The amplitude of the overtones is reduced as the overtone number increases.

Finally, the waveform is shaped with a Tukey window, with an exponential decay to reduce the volume over time. The sound is saved as a WAV file, and then converted to an MP3 file using ffmpeg.

Notes
-----
The units of the different parameters are as follows:
- Frequencies are in Hz.
- Times are in seconds.

This script requires the following packages:
- numpy
- scipy
- pandas (in elements.py)
- ffmpeg (to convert the WAV files to MP3)
"""

FREQUENCY_LOWEST_FUNDAMENTAL_HZ = 40
FREQUENCY_SAMPLING_HZ = 44100
SAMPLE_DURATION_SECONDS = 2
N_SAMPLES = FREQUENCY_SAMPLING_HZ * SAMPLE_DURATION_SECONDS
SPECTRAL_HARMONIC_DECAY = 0.5, 0.2, 0.1
ENVELOPE_DECAY_SEC = 0.5
ENVELOPE_ATTACK_SEC = 0.2
GENERIC_FILEPATH = "sounds/sound-{}.{}"
OUTPUT_VOLUME = 0.3

import subprocess

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal.windows import tukey
from tqdm import tqdm

import elements


def time_vector(duration=SAMPLE_DURATION_SECONDS, samples=N_SAMPLES):
    """Generate a time vector."""
    return np.linspace(0, duration, samples, endpoint=False)


def sine(frequency):
    """Generate a sine wave with a given frequency."""
    return np.sin(2 * np.pi * frequency * time_vector())


def exponential_decay(tau=ENVELOPE_DECAY_SEC):
    """Generate an exponential decay."""
    return np.exp(-time_vector() / tau)


def window(tau=ENVELOPE_ATTACK_SEC):
    """Apply a window to the signal."""
    return tukey(len(time_vector()), tau)


def main():

    # Read the complete periodic table
    periodic_table = elements.read()
    periodic_table = elements.clean(periodic_table)
    periodic_table = elements.move_f_block(periodic_table)

    # Iterate over the elements
    for _, element in tqdm(
        periodic_table.iterrows(),
        total=len(periodic_table),
        desc="Creating sounds",
    ):
        # Rest of the code

        # Get the atomic number
        atomic_number = element["atomic_number"]
        group = element["group"]

        # Generate fundamental sound
        fundamental = element["period"] * FREQUENCY_LOWEST_FUNDAMENTAL_HZ
        note = sine(fundamental)

        # Add overtones
        overtone = fundamental * group
        if element["block"] == "d-block":
            note += SPECTRAL_HARMONIC_DECAY[0] * sine(overtone)
        if element["block"] == "f-block":
            for i in range(2):
                note += SPECTRAL_HARMONIC_DECAY[i] * sine((i + 1) * overtone)
        if element["block"] == "p-block":
            for i in range(3):
                note += SPECTRAL_HARMONIC_DECAY[i] * sine((i + 1) * overtone)

        # Exponential decay
        note *= exponential_decay()
        note *= window()
        note *= OUTPUT_VOLUME

        # Save the sound in wav and mp3 format
        filename_wav = GENERIC_FILEPATH.format(atomic_number, "wav")
        filename_mp3 = GENERIC_FILEPATH.format(atomic_number, "mp3")
        wavfile.write(filename_wav, FREQUENCY_SAMPLING_HZ, note)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                filename_wav,
                "-codec:a",
                "libmp3lame",
                "-qscale:a",
                "1",
                "-v",
                "0",
                "-af",
                f"volume={OUTPUT_VOLUME}",
                filename_mp3,
            ]
        )

        # Delete the WAV file
        subprocess.run(["rm", filename_wav])


if __name__ == "__main__":
    main()
