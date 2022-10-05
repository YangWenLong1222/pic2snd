#!/usr/bin/env python3
import cv2
import time
import math
import numpy as np
import soundfile as sf
import sys
import getopt

# sample_rate = 44100
# total_time = 30
# interval = 0.1
# img_path = './example/star.jpeg' 
# snd_path = './example/stereo_file.wav'
# # img_path = './example/t.png' 
# # snd_path = './example/stereo_file2.wav'
# # img_path = './example/t2.png' 
# # snd_path = './example/stereo_file3.wav'
# is_piano = True # 用钢琴的方式，就无法设定频率范围。
# freq_max = 200000
# freq_min = 0

img_path = '' 
snd_path = ''
is_piano = False # 用钢琴的方式，就无法设定频率范围。
total_time = 10
interval = 0.1
sample_rate = 44100
freq_max = 200000
freq_min = 0

# 钢琴88键，频率
piano_f = [
    27500.0,
    29135.0,
    30868.0,
    32703.0,
    34648.0,
    36708.0,
    38891.0,
    41203.0,
    43654.0,
    46249.0,
    48999.0,
    51913.0,
    55000.0,
    58270.0,
    61735.0,
    65406.0,
    69296.0,
    73416.0,
    77782.0,
    82407.0,
    87307.0,
    92499.0,
    97999.0,
    103826.0,
    110000.0,
    116541.0,
    123471.0,
    130813.0,
    138591.0,
    146832.0,
    155563.0,
    164814.0,
    174614.0,
    184997.0,
    195998.0,
    207652.0,
    220000.0,
    233082.0,
    246942.0,
    261626.0,
    277183.0,
    293665.0,
    311127.0,
    329628.0,
    349228.0,
    369994.0,
    391995.0,
    415305.0,
    440000.0,
    466164.0,
    493883.0,
    523251.0,
    554365.0,
    587330.0,
    622254.0,
    659255.0,
    698456.0,
    739989.0,
    783991.0,
    830609.0,
    880000.0,
    932328.0,
    987767.0,
    1046502.0,
    1108731.0,
    1174659.0,
    1244508.0,
    1318510.0,
    1396913.0,
    1479978.0,
    1567982.0,
    1661219.0,
    1760000.0,
    1864655.0,
    1975533.0,
    2093005.0,
    2217461.0,
    2349318.0,
    2489016.0,
    2637020.0,
    2793826.0,
    2959955.0,
    3135963.0,
    3322438.0,
    3520000.0,
    3729310.0,
    3951066.0,
    4186009.0
]

# 因为图像的y轴本身是反的，所以变成了顺时针扫描。

# 步骤1，返回亮度数组。
# TODO: 可以设置起始角度位置，可以设置顺时针还是逆时针。
# TODO: 可以调整弧度值来做到，0到2pi，起始就是起始位置。顺时针就是升序，起始点是0；逆时针就是降序，起始点就是2pi。
def step1():
    img_cv = cv2.imread(img_path)  #读取数据
    print("img_cv:",img_cv.shape)

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
            if is_piano:
                # f means the index of freqArray in this case.
                f = math.floor(p/pmax * 88)
                if f == 88: f = 87
            else:
                # f means the frequency in this case.
                f = calc_freq(p, pmax)
            pass

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
# luminance -- step1中输出的排序完毕的像素点数组。
# total_time -- 整个视频的长度。
# interval -- 一个采样分片的长度。
# rad_init -- 进入这个函数时的弧度。
# index -- 进入这个函数时该取的luminance数组中的数据的下标。
# return sinewave, i, rad -- 指定数量的采样点。本次走到的下标和弧度，为下次调用做准备。
# index -- luminance的起始位置，之前的处理过了, 是排完序的数组。
def step2(luminance, total_time, interval, rad_init, index):
    freq_array = [0.0 for i in range(88)]
    # 弧度范围。
    rad_end = rad_init + interval/total_time * 2 * math.pi
    # 因为是排完序的，没必要遍历。
    i = index
    l = len(luminance)
    time = np.arange(0, interval, 1/sample_rate)
    sinewave = np.empty(len(time))
    count = 0
    while i < l:
        # (s, f, p, w)
        point = luminance[i]
        if point[3] > rad_end: break
        i += 1

        # 过滤掉亮度比较低的点。
        # if point[0] < 450: continue

        if is_piano:

            # 亮度叠加。
            freq_array[point[1]] += point[0]

        else:
            # 不必按照p相同划分了，虽然频率相同，但是是浮点数，可以都当做不同处理，一样的。
            # 每一个点表示一个微正弦波。随机相位，避免首部叠加过强。
            sinewave += point[0] * np.sin(2 * np.pi * point[1] * time + 2 * np.pi * np.random.random())
        pass
        count += 1
    pass

    if is_piano:
        fi = 0
        for fi in range(88):
            if freq_array[fi] < 0.01: continue  # 避免浮点数运算误差。相当于0，无叠加。
            sinewave += freq_array[fi] * np.sin(2 * np.pi * piano_f[fi] * time + 2 * np.pi * np.random.random())
        pass
    pass

    sinewave /= count

    return sinewave, i, rad_end

def main(argv):
    start = time.time()

    get_opts(argv)

    all_samples = []

    luminance = step1()
    l = len(luminance)
    print('luminance length: %d.' % l)
    i = 0
    rad = 0
    while i < l:
    # while i < 26000:
        sinewave, i, rad = step2(luminance , total_time, interval, rad, i)

        print('%%%.2f' % (rad/(2*np.pi)*100))

        for sample in sinewave:
            all_samples.append([sample])
        pass

    # print(len(all_samples))
    # samples_2_write = all_samples
    samples_2_write = adjust_range(all_samples)
    sf.write(snd_path, samples_2_write, sample_rate, 'PCM_24')

    dur = time.time() - start
    print('cost: %f s.' % dur)
    return


def get_opts(argv):

    global img_path
    global snd_path
    global is_piano
    global total_time
    global interval
    global sample_rate
    global freq_max
    global freq_min

    try:
        # args 表示剩下未解析的参数。
        opts, args = getopt.getopt(argv[1:], 'hi:o:pt:r:', [
            'help',
            'img_path=',
            'snd_path=',
            'piano',
            'total_time=',
            'interval=',
            'sample_rate=',
            'freq_max=',
            'freq_min=',
        ])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                # exit(0) in help_info() fn could also be catched by try-except clause.
                # so, just raise an exception here to show the help info.
                # help_info()
                raise Exception()
            if opt in ('-i', '--img_path'):
                if arg == '': raise Exception()
                img_path = arg
                continue
            if opt in ('-o', '--snd_path'):
                if arg == '': raise Exception()
                snd_path = arg
                continue
            if opt in ('-p', '--piano'):
                if arg != '': raise Exception()
                is_piano = True
                continue
            if opt in ('-t', '--total_time'):
                total_time = int(arg)
                continue
            if opt in ('--interval'):
                interval = float(arg/100.0)
                continue
            if opt in ('-r', '--sample_rate'):
                sample_rate = int(arg)
                continue
            if opt in ('--freq_max'):
                freq_max = int(arg)
                continue
            if opt in ('--freq_min'):
                freq_min = int(arg)
                continue
        pass
    except:
        help_info()

    # img and snd path check.
    if img_path == '' or snd_path == '':
        help_info()

    test_options()

    return

# show help info and terminate the program.
def help_info():
    print('''
This is the help infomation.
-h, --help:            Show this help information.
-i, --img_path:        The input image file path. This option is required.
-o, --snd_path:        The output sound file path. This option is required.
-p, --piano:           Using the piano frequency. This option has no argument. Default is not set.
-t, --total_time:      The total time of the sound file. The argument must be an integer. Default is 10s.
--interval:            The interval time is a time piece to collect the points to be transform into sound a time, then next piece. The argument must be an integer. Default is 100ms.
-r, --sample_rate:     The wav file sample rate. The argument must be an integer. Default is 44100.
--freq_max:            The maximum frequency. The argument must be an integer. Default is 200000Hz. This parameter only works when '-p' or '--piano' is not set.
--freq_min:            The minimum frequency. The argument must be an integer. Default is 0Hz. This parameter only works when '-p' or '--piano' is not set.
    ''')
    sys.exit(0)

def test_options():
    print('img_path:\t %s' % img_path)
    print('snd_path:\t %s' % snd_path)
    print('is_piano:\t', is_piano)
    print('total_time:\t %d' % total_time)
    print('interval:\t %f' % interval)
    print('sample_rate:\t %d' % sample_rate)
    print('freq_max:\t %d' % freq_max)
    print('freq_min:\t %d' % freq_min)
    return
    
def adjust_range(all_samples):
    ret = []
    max = 0.01  # 避免除零错误。
    for sample in all_samples:
        if sample[0] > max: max = sample[0]

    for sample in all_samples:
        ret.append([sample[0]/max])

    # print(max)
    return ret

# TODO: 根据频率再去调整音量，以适应人耳。
def adjust_s(f):
    return f

# 根据亮度定频率。
# 废弃，没有使用。
def calc_freq2(s):
    # 5000/765
    # return 6.5360 * s
    return np.exp(s/765 * 10)

# 根据距离定频率，直接频率，
def calc_freq(p, pmax):
    # np.exp(10) == 22026
    # np.exp(5) == 148
    rate = (freq_max - freq_min)/(22026 - 148)
    # TODO: 映射算法将来是要改动的. 这是直接映射到0~20000了。
    # return (16000-200)/pmax*p + 200
    # return 20000/pmax*p
    return np.exp(p/pmax * 5 + 5) * rate + freq_min
    # return np.exp(p/pmax * 10)

if __name__ == '__main__':
    main(sys.argv)
