# The interactive periodic table of elements

This repository is an artistic project that turns the periodic table of elements into an interactive musical instrument. No description needed, just try it at https://leonard-seydoux.github.io/melodic-table-of-the-elements/. The project aims at evolving, so feel free to contribute! 

## How to sonify the periodic table of elements

The basic idea is to create a sound that is unique for each element, but that remain nice to the ear when multiple elements are played together. All sounds are created from a multiple of the fundamental frequency. The fundamental frequency of an element is the product of the period and the fundamental frequency. The period is the row in which the element is located, and the fundamental frequency is a constant. The overtone is the product of the group and the fundamental frequency. The sound is a sine wave with the fundamental frequency, and additional sine waves with the overtone frequency. 

Several overtones are added depending on the block of the element. The d-block elements have one overtone, the f-block elements have two overtones, and the p-block elements have three overtones. The amplitude of the overtones is reduced as the overtone number increases.

Finally, the waveform is shaped with a Tukey window, with an exponential decay to reduce the volume over time. The sound is saved as a WAV file, and then converted to an MP3 file using ffmpeg.

## Potential improvements

One notable issue is the click sound that may appear when the pointer leaves and re-enters the element before the fade-out of the sound. This is due to the fact that the sound is stopped and restarted when the pointer leaves and re-enters the element. I tried to have an "emergency" fade-out of the sound when the pointer leaves and re-enters the element, but it did not work. If you have any idea on how to solve this issue, please let me know!