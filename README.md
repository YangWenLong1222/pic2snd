# pic2snd
picture --> sound

## Python运行需要的包

|数据包名|用途|pip3安装包名|
|:-:|:-:|:-:|
|cv2|opencv库，图像识别处理。|opencv-python|
|time|内置时间库，时间相关计算。||
|math|内置数学库，数学计算。||
|numpy|数据计算相关库，优秀数据结构。|numpy|
|soundfile|音频库，声音文件处理。|soundfile|
|sys|内置系统库，处理参数。||
|getopt|内置库，处理参数。||

## 运行参数

```
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
```

### 例子

```
➜  pic2snd git:(main) ✗ python3 pic2snd.py -i example/t.png -o example/sound.wav -p -t 30
img_path:	 example/t.png
snd_path:	 example/sound.wav
is_piano:	 True
total_time:	 30
interval:	 0.100000
sample_rate:	 44100
freq_max:	 200000
freq_min:	 0
img_cv: (504, 734, 3)
luminance length: 369936.
%100.00
cost: 4.675538 s.
➜  pic2snd git:(main) ✗
```