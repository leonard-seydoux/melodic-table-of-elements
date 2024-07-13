"""Create the sounds to be played on hover over the element."""

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
    frequency = period * 40  # Hz
    overtone = frequency * group  # Hz
    duration = 2  # seconds

    # Generate the sound
    t = np.linspace(0, duration, int(44100 * duration), False)
    note = np.sin(frequency * t * 2 * np.pi)
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
