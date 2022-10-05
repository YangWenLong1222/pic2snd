#!/usr/bin/env python3
import sys
import getopt

img_path = '' 
snd_path = ''
is_piano = False # 用钢琴的方式，就无法设定频率范围。
total_time = 10
interval = 0.1
sample_rate = 44100
freq_max = 200000
freq_min = 0

def main(argv):
    get_opts(argv)
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
    
if __name__ == '__main__':
    main(sys.argv)