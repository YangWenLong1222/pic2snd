#!/usr/bin/env python3
import sys
import getopt

sample_rate = 44100
total_time = 30
interval = 0.1
img_path = './example/star.jpeg' 
snd_path = './example/stereo_file.wav'
# img_path = './example/t.png' 
# snd_path = './example/stereo_file2.wav'
# img_path = './example/t2.png' 
# snd_path = './example/stereo_file3.wav'
is_piano = True # 用钢琴的方式，就无法设定频率范围。
freq_top = 200000
freq_bottom = 0

def main(argv):
    # args 表示剩下未解析的参数。
    opts, args = getopt.getopt(argv[1:], 'hi:o:', ['img_path='])
    print(opts)
    print(args)

    global img_path

    for opt, arg in opts:
        if opt == '-h':
            # TODO: show help info and terminate the program.
            print('''
This is the help infomation.
-h, --help:        Show this help information.
-i, --img_path:    The input image file path.
-o, --snd_path:    The output sound file path.
-p, --piano:       Using the piano frequency. Default is not.    
--total_time:      The total time of the sound file. Default is 10s.
--interval:        The interval time is a time piece to collect the points to be transform into sound a time, then next piece. Default is 100ms.
-r, --sample_rate: The wav file sample rate. Default is 44100.
            ''')
            sys.exit(0)
        # if opt == '-i' or opt == '--img_path':
        if opt in ('-i', '--img_path'):
            print(img_path)
            img_path = arg
    pass

    print(img_path)

    return

if __name__ == '__main__':
    main(sys.argv)