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

### 算法说明

算法说明:
主要分为两种算法，
钢琴算法：一种以钢琴弹奏思想为基础创造的算法，在命令行中，以-p, —piano参数表示。以画面中心为起始点，至画面一角，连接一线段。以此线段为半径，从3点钟位置开始，顺时针旋转一周。将这个圆的半径划分为88个钢琴琴键区域，靠近中心为低音区，远离中心为高音区。画面的亮度，即是击键的强弱。用这个方法，如上线段扫过一个圆周，亮点击打钢琴琴键发出的声音组合在一起，生成对应的音频文件。

听觉算法：一种以人类听觉声音振动频率为范围，自定义频率分布，画面亮点发出声音的算法。在命令行中，不以-p, —piano，以画面中心为起始点，至画面一角，连接一线段。以此线段为半径，从3点钟位置开始，顺时针旋转一周。中心点为低频振动，远离中心点振动频率增加。因为人类听觉对频率的敏感度是非线性的，所以本算法采用了从低频到高频，以自然常熟e指数的方式递增。像素点的亮度就是该频率振动的幅度。所有一周的振动组合在一起，生成对应的音频文件。