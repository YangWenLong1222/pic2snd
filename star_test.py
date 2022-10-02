#!/usr/bin/env python3
import cv2
import time
import math
import numpy as np
import soundfile as sf

sample_rate = 44100
total_time = 10
interval = 0.1

img_path = './example/star.jpeg' 
snd_path = './example/stereo_file.wav'
# img_path = './example/t.png' 
# snd_path = './example/stereo_file2.wav'


# 因为图像的y轴本身是反的，所以变成了顺时针扫描。

# 步骤1，返回亮度数组。
def step1():
    img_cv = cv2.imread(img_path)  #读取数据
    print("img_cv:",img_cv.shape)
    # print(img_cv)

    (hight, width, n) = img_cv.shape

    luminance = []
    pmax = math.sqrt(width * width + hight * hight)/2
    zero_x = width/2
    zero_y = hight/2
    for i in range(width):
        for j in range(hight):
            # s 相当于响度，振幅。
            s = int(img_cv[j][i][0]) + int(img_cv[j][i][1]) + int(img_cv[j][i][2])
            # 距离
            x = i - zero_x
            y = j - zero_y
            p = math.sqrt(x*x + y*y)
            # 计算这个点对应的声音频率是多少。
            f = calc_freq(p, pmax)
            # f = calc_freq2(s)

            # 根据频率再去调整一下音量，以适应人耳。
            # s = adjust_s(f)

            # 弧度
            w = 0.0
            if x == 0 and y == 0: w = 0
            if x == 0 and y > 0: w = math.pi/2
            if x == 0 and y < 0: w = -math.pi/2
            if x != 0: w = math.atan2(y, x)
            # 调整，范围从0~2pi
            if w < 0: w += 2 * math.pi
            luminance.append((s, f, p, w))

    # 按照弧度进行排序。
    luminance.sort(key=lambda x: x[3])

    return luminance

# 步骤2，整理100ms内的数据。
# return -- 指定数量的采样点。
# index -- luminance的起始位置，之前的处理过了, 是排完序的数组。
def step2(luminance, total_time, interval, rad_init, index):
    # 弧度范围。
    rad_end = rad_init + interval/total_time * 2 * math.pi
    # 因为是排完序的，没必要遍历。
    i = index
    l = len(luminance)
    time = np.arange(0, interval, 1/sample_rate)
    sinewave = np.empty(len(time))
    count = 0
    while i < l:
        point = luminance[i]
        if point[3] > rad_end: break
        i += 1

        # 不必按照p相同划分了，虽然频率相同，但是是浮点数，可以都当做不同处理，一样的。
        # 每一个点表示一个微正弦波。随机相位，避免首部叠加过强。
        sinewave += point[0] * np.sin(2 * np.pi * point[1] * time + 2 * np.pi * np.random.random())
        count += 1
        # 过滤暗点，不一定需要。
        # if point[0] > 90:
        #     sinewave += point[0] * np.sin(2 * np.pi * point[1] * time + 2 * np.pi * np.random.random())
        #     count += 1
        # pass
    sinewave /= count

    # 每一小步都归一化一下。感觉不好，会更平了。
    # max = 0.0
    # for s in sinewave:
    #     if s > max: max = s
    # sinewave /= max
        
    return sinewave, i, rad_end

def main():
    start = time.time()

    all_samples = []

    luminance = step1()
    l = len(luminance)
    print('luminance length: %d.' % l)
    i = 0
    rad = 0
    while i < l:
        sinewave, i, rad = step2(luminance , total_time, interval, rad, i)

        print(len(sinewave))
        print(rad)
        print(i)

        for sample in sinewave:
            all_samples.append([sample])
        pass

    print(len(all_samples))
    # samples_2_write = all_samples
    samples_2_write = adjust_range(all_samples)
    sf.write(snd_path, samples_2_write, sample_rate, 'PCM_24')

    # for i in range(100):
    #     print(samples_2_write[i])

    dur = time.time() - start
    print('cost: %f s.' % dur)
    return

def adjust_range(all_samples):
    ret = []
    max = 0.01  # 避免除零错误。
    for sample in all_samples:
        if sample[0] > max: max = sample[0]

    for sample in all_samples:
        ret.append([sample[0]/max])

    print(max)
    return ret

# 根据频率再去调整音量，以适应人耳。
def adjust_s(f):
    return f

# 根据亮度定频率。
def calc_freq2(s):
    # 5000/765
    # return 6.5360 * s
    return np.exp(s/765 * 10)

# 根据距离定频率
def calc_freq(p, pmax):
    # TODO: 映射算法将来是要改动的. 这是直接映射到0~20000了。
    # return (16000-200)/pmax*p + 200
    # return 20000/pmax*p
    return np.exp(p/pmax * 5 + 5)
    # return np.exp(p/pmax * 10)
    # index = math.floor(p/pmax * 88)
    # if index == 88: index = 87
    # return piano_f[index]

if __name__ == '__main__':
    main()
