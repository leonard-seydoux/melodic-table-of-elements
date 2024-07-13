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

FUNDAMENTAL_FREQUENCY = 40
SAMPLING_RATE = 44100
SAMPLE_DURATION = 2

import numpy as np
from scipy.io import wavfile
from scipy.signal.windows import tukey

import elements
import subprocess

# Read the complete periodic table
periodic_table = elements.read()
periodic_table = elements.clean(periodic_table)
periodic_table = elements.move_f_block(periodic_table)

# Iterate over the elements
for index, element in periodic_table.iterrows():

    # Get the atomic number
    atomic_number = element["atomic_number"]
    period = element["period"]
    group = element["group"]

    # Get the sound
    fundamental = period * FUNDAMENTAL_FREQUENCY
    overtone = fundamental * group
    duration = SAMPLE_DURATION

    # Generate the sound
    t = np.linspace(0, duration, int(SAMPLING_RATE * duration), False)
    note = np.sin(fundamental * t * 2 * np.pi)
    if element["block"] == "d-block":
        note += 0.2 * np.sin(overtone * t * 2 * np.pi)
    if element["block"] == "f-block":
        note += 0.1 * np.sin(overtone * t * 2 * np.pi)
        note += 0.05 * np.sin(2 * overtone * t * 2 * np.pi)
    if element["block"] == "p-block":
        note += 0.1 * np.sin(overtone * t * 2 * np.pi)
        note += 0.05 * np.sin(2 * overtone * t * 2 * np.pi)
        note += 0.001 * np.sin(3 * overtone * t * 2 * np.pi)

    # Exponential decay
    decay = np.exp(-t / 0.5)
    note = note * decay

    # Reduce the volume
    note = note / np.abs(note.max()) * 0.1
    note = note * tukey(len(note), 0.1)

    # Save the sound
    filename_wav = f"sounds/sound-{atomic_number}.wav"
    filename_mp3 = f"sounds/sound-{atomic_number}.mp3"
    wavfile.write(filename_wav, 44100, note)

    # Convert WAV to MP3 using ffmpeg
    subprocess.run(
        [
            "ffmpeg",
            "-y",  # Allow overwrite
            "-i",
            filename_wav,
            "-codec:a",
            "libmp3lame",
            "-qscale:a",
            "2",
            "-v",
            "0",  # Disable verbose output
            "-af",
            "volume=0.1",
            filename_mp3,
        ]
    )
