#!/usr/bin/env python3
import numpy as np

sample_rate = 1000
start_time = 0
end_time = 10
theta = 0

time = np.arange(start_time, end_time, 1/sample_rate)
print(time)
print(len(time))

sinewave = 25 * np.sin(2 * np.pi * 1000 * time + theta)
print(sinewave)
print(len(sinewave))


print('hihihi')
sinewave = np.empty(5)
print(sinewave)
sinewave += 5
print(sinewave)
sinewave /= 2
print(sinewave)

for i in range(10):
    print(np.random.random())