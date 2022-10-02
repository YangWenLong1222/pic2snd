#!/usr/bin/env python3
import numpy as np
import soundfile as sf

# a = np.random.randn(10, 2)
a = np.random.randn(44100, 1)
print(a)
sf.write('stereo_file.wav', a, 44100, 'PCM_24')