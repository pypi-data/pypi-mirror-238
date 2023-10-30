# bm-video-tools

针对图片、视频、音频常见操作的简易封装

<br />

## 快速开始

### 1.依赖

* ffmpeg
* python >= 3.8

<br />

### 2.安装

```shell
pip install bm-video-tools
```

<br />

### 3.基础使用

#### (1) 操作类

该类是对`ffmpeg`指令相关选项的封装

```python
from bm_video_tools import Operate
op = Operate()
```

##### 裁剪

方法：_cut(width, height, x, y)_

参数：

* width: 裁剪宽度
* height: 裁剪高度
* x: 裁剪的坐标点（默认左上角）
* y: 裁剪的坐标点（默认左上角）

返回：Self

示例：

```python
op = Operate().cut(300, 300)
```

如果不指定高度但指定坐标点，则裁剪坐标点到图像右下角的区域

```python
op = Operate().cut(x=100, y=100)
```

##### 缩放

方法：_scale(width, height)_

参数：

* width: 缩放的宽度
* height: 缩放的高度

返回：Self

示例：

```python
op = Operate().scale(200, 100)
```

如果指定宽度和高度，则按照指定的值进行缩放

如果指定其中一个值，另一个为`-1`，则按照指定值等比例缩放

```python
op = Operate().scale(200, -1)	# 缩放宽度为200，高度等比例缩放
```

##### 旋转

方法：_rotate(unit)_

参数：

* unit: 旋转角度

返回：Self

示例：

```python
op = Operate().rotate(1)	# 旋转90度
op = Operate().rotate(2)	# 旋转180度
op = Operate().rotate(3)	# 旋转270度
op = Operate().rotate(-1)	# 旋转270度(逆时针旋转90度)
```

##### 翻转

方法：_turn(h, v)_

参数：

* h: 水平翻转
* v: 垂直翻转

返回：Self

示例：

```python
op = Operate().turn(v=True)
```

##### 拆分

方法：_split(start, end, second)_

参数：

* start: 开始时间
* end: 结束时间
* second: 截取时长（秒）

返回：Self

示例：

```python
op = Operate().split(5, second=5)
```

##### 剔除

方法：_eliminate(a, v)_

参数：

* a: 剔除音频流
* v: 剔除视频流

返回：Self

示例：

```python
op = Operate().eliminate(a=True)
```

##### 倒放

方法：_reverse()_

参数：无

返回：Self

示例：

```python
op = Operate().reverse()
```

##### 倍速

方法：_speed(rate)_

参数：

* rate: 速率（范围0.5~2.0）

返回：Self

示例：

```python
op = Operate().speed(0.5)
```

##### 修改参数

方法：_params(...)_

参数：

* pix_fmt: 像素格式
* codec_v: 视频编码器
* fps: 视频帧速率
* frames_v: 视频总帧数
* codec_a: 音频编码器
* sample: 音频采样率
* frames_a: 音频总帧数

返回：Self

示例：

```python
op = Operate().params(fps=30)
```

>理论上，音视频流相关格式参数都可修改，当前只列举了一些常见的修改参数，该方法会根据后续实际业务不断更新

<br />

**注意：**

`Operate`的成员方法返回的都是实例对象自身，这意味着这些方法可以链式调用：

```python
op = Operate().rotate(2).turn(h=True).rotate(1).reverse()
op = Operate().split(5, 15).cut(200, 200)
```

但是，这些方法其实并没有实质性的作用，需与下面几个类共同使用

<br />

#### (2) 图片

```python
from bm_video_tools import Image
img = Image(input_path)
```

参数：

* input_path：文件输入路径

<br />

##### 执行基础操作

方法：_run(op, output_path)_

参数：

* op: Operation实例对象
* output_path：输出路径

返回：Image

示例：

```python
img = Image('xxx')
op = Operate().cut(300, 300, 0, 0)
await img.run(op, output_path='xxx')
```

##### 查看图片信息
方法：_get_info()_

参数：无

返回：dict

示例：

```python
info = await img.get_info()
```

```json
{
    'streams': [										// 媒体流
        {												
            'index': 0, 								// 媒体流索引
            'codec_name': 'mjpeg', 						// 编码器名
            'codec_long_name': 'Motion JPEG', 			// 编码器全名
            'profile': 'Baseline', 						// 编码器配置文件
            'codec_type': 'video', 						// 流的类型
            'codec_tag_string': '[0][0][0][0]', 		// 流使用的编码器的标识符字符串
            'codec_tag': '0x0000', 						// 流使用的编码器的标识符整数值
            'width': 1024, 								// 流的宽度
            'height': 782, 								// 流的高度
            'coded_width': 1024, 						// 流编码时的宽度
            'coded_height': 782, 						// 流编码时的高度
            'closed_captions': 0, 						// 流是否包含了有关视频注释和字幕的信息(这个参数只对视频流有效)
            'film_grain': 0, 							// 流是否添加了电影颗粒噪点
            'has_b_frames': 0, 							// 流是否存在B帧
            'sample_aspect_ratio': '1:1', 				// 采样宽高比
            'display_aspect_ratio': '512:391', 			// 显示宽高比
            'pix_fmt': 'yuvj420p', 						// 像素格式
            'level': -99, 								// 流的级别
            'color_range': 'pc', 						// 颜色范围(tv: 表示颜色采用了 16-235 范围，pc: 表示颜色采用了 0-255 范围)
            'color_space': 'bt470bg', 					// 颜色空间
            'chroma_location': 'center', 				// 色度坐标的放置位置
            'refs': 1, 									// 编码器中参考图像的数量
            'r_frame_rate': '25/1', 					// 码率的分子和分母
            'avg_frame_rate': '25/1', 					// 平均帧率
            'time_base': '1/25', 						// 时间戳的基本时间单位
            'start_pts': 0, 							// 首个PTS
            'start_time': '0.000000', 					// 流的开始时间
            'duration_ts': 1, 							// 流总时长的时间戳
            'duration': '0.040000', 					// 流总时长的秒数
            'bits_per_raw_sample': '8', 				// 原始采样数据每个样本所占用的位数(音频通常为16、24，视频通常为8、10、12)
            'disposition': {							// 流状态信息
                'default': 0, 
                'dub': 0, 
                'original': 0, 
                'comment': 0, 
                'lyrics': 0, 
                'karaoke': 0, 
                'forced': 0, 
                'hearing_impaired': 0, 
                'visual_impaired': 0, 
                'clean_effects': 0, 
                'attached_pic': 0, 
                'timed_thumbnails': 0, 
                'captions': 0, 
                'descriptions': 0, 
                'metadata': 0, 
                'dependent': 0, 
                'still_image': 0
            }
        }
    ], 
    'format': {											// 容器格式信息
        'filename': './asset/image1.jpg', 				// 输入文件的路径或网络URL地址
        'nb_streams': 1, 								// 媒体文件中流的数量
        'nb_programs': 0, 								// 媒体文件中程序的数量
        'format_name': 'image2', 						// 媒体封装格式的名称
        'format_long_name': 'image2 sequence', 			// 媒体封装格式的全名
        'start_time': '0.000000', 						// 从媒体中哪个时间点开始进行分析
        'duration': '0.040000', 						// 媒体的总时长
        'size': '217901', 								// 媒体文件的大小
        'bit_rate': '43580200', 						// 媒体文件中平均每秒使用的总比特率
        'probe_score': 50								// 判定该媒体文件是正确格式的可能性得分(分值范围为 0~100)
    }
}
```

##### 人物抠图
方法：_remove(output_path, model_name[, op])_

参数：

* output_path: 输出路径
* （可选）model_name: 模型名称（默认u2net_human_seg）
* （可选）op: Operation实例对象

返回：Image

示例：

```python
img = Image('xxx')
await img.remove('xxx')
```

>人物抠图功能是基于[backgroundremover](https://github.com/nadermx/backgroundremover)项目实现的
>
>可选模型：u2netp、u2net、u2net_human_seg
>
>请从项目中下载模型至操作系统当前用户的`.bm-video-tools`文件夹，否则无法使用抠图功能

有时候，我们需要对媒体资源进行一些前置操作，然后再执行相应方法，例如：

```python
img = Image('xxx')
op = Operate().cut(200, 200)

# 使用临时文件执行操作，对操作后的临时文件进行抠图
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
temp_file_path = temp_file.name.replace("\\", "/")
temp_file.close()
try:
    img_res = await img.run(op, output_path=temp_file_path)
    await img_res.remove('xxx')
    del img_res
finally:
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
```

但对于使用者来说，并不需要关注这些中间状态以及临时文件，上述代码等同于：

```python
img = Image('xxx')
op = Operate().cut(200, 200)

await video.remove("xxx", op=op)	# 注意: 该Operate实例对象是对输入文件进行处理，而非输出文件
```

##### 人脸检测

方法：_face_detection(model_name[, op])_

参数：

* （可选）model_name: 模型名称（默认haarcascade_frontalface_alt2）
* （可选）op: op: Operation实例对象

返回：bool

示例：

```python
img = Image(image1_path)
await img.face_detection()
```

>人脸检测使用的是OpenCV的检测方法
>
>可选模型：haarcascade_frontalface_alt2、haarcascade_fullbody等
>
>和人物抠图一样，需将xml文件保存至操作系统当前用户的`.bm-video-tools`文件夹，否则无法正常使用

<br />

#### (3) 视频

```python
from bm_video_tools import Video
video = Video(input_path)
```

参数：

* input_path：文件输入路径

<br />

##### 执行基础操作

方法：_run(op, output_path)_

参数：

* op: Operation实例对象
* output_path：输出路径

返回：Video

示例：

```python
video = Video("xxx")
op = Operate().turn(v=True)
await video.run(op, output_path="xxx")
```

##### 查看视频信息

方法：_get_info()_

参数：无

返回：dict

示例：

```python
info = await video.get_info()
```

```json
{
    'streams': [
        {
            'index': 0,
            'codec_name': 'h264', 
            'codec_long_name': 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10',
            'profile': 'Constrained Baseline',
            'codec_type': 'video',
            'codec_tag_string': 'avc1', 
            'codec_tag': '0x31637661', 
            'width': 320, 
            'height': 240, 
            'coded_width': 320, 
            'coded_height': 240, 
            'closed_captions': 0, 
            'film_grain': 0, 
            'has_b_frames': 0, 
            'pix_fmt': 'yuv420p', 
            'level': 13, 
            'color_range': 'tv',
            'color_space': 'smpte170m',
            'color_transfer': 'bt709',
            'color_primaries': 'smpte170m', 
            'chroma_location': 'left', 
            'field_order': 'progressive', 
            'refs': 1, 
            'is_avc': 'true', 
            'nal_length_size': '4', 
            'id': '0x1', 
            'r_frame_rate': 
            '30000/1001', 
            'avg_frame_rate': '93500/3153', 
            'time_base': '1/90000', 
            'start_pts': 0, 
            'start_time': '0.000000', 
            'duration_ts': 1135080, 
            'duration': '12.612000', 
            'bit_rate': '80637', 
            'bits_per_raw_sample': '8', 
            'nb_frames': '374', 
            'extradata_size': 40, 
            'disposition': {
                'default': 1, 
                'dub': 0, 
                'original': 0, 
                'comment': 0, 
                'lyrics': 0, 
                'karaoke': 0, 
                'forced': 0, 
                'hearing_impaired': 0, 
                'visual_impaired': 0, 
                'clean_effects': 0, 
                'attached_pic': 0, 
                'timed_thumbnails': 0, 
                'captions': 0, 
                'descriptions': 0, 
                'metadata': 0, 
                'dependent': 0, 
                'still_image': 0
            }, 
            'tags': {
                'creation_time': '2010-05-11T10:32:06.000000Z', 
                'language': 'und', 
                'vendor_id': '[0][0][0][0]', 
                'encoder': 'JVT/AVC Coding'
            }
        }, {
            'index': 1, 
            'codec_name': 'aac', 
            'codec_long_name': 'AAC (Advanced Audio Coding)', 
            'profile': 'LC', 
            'codec_type': 'audio', 
            'codec_tag_string': 'mp4a', 
            'codec_tag': '0x6134706d', 
            'sample_fmt': 'fltp', 
            'sample_rate': '48000', 
            'channels': 2, 
            'channel_layout': 'stereo', 
            'bits_per_sample': 0, 
            'initial_padding': 0, 
            'id': '0x2', 
            'r_frame_rate': '0/0', 
            'avg_frame_rate': '0/0', 
            'time_base': '1/48000', 
            'start_pts': 0, 
            'start_time': '0.000000', 
            'duration_ts': 605184, 
            'duration': '12.608000', 
            'bit_rate': '115752', 
            'nb_frames': '591', 
            'extradata_size': 2, 
            'disposition': {
                'default': 1, 
                'dub': 0, 
                'original': 0, 
                'comment': 0, 
                'lyrics': 0, 
                'karaoke': 0, 
                'forced': 0, 
                'hearing_impaired': 0, 
                'visual_impaired': 0, 
                'clean_effects': 0, 
                'attached_pic': 0, 
                'timed_thumbnails': 0, 
                'captions': 0, 
                'descriptions': 0, 
                'metadata': 0, 
                'dependent': 0, 
                'still_image': 0
            }, 
            'tags': {
                'creation_time': '2010-05-11T10:32:06.000000Z', 
                'language': 'und', 
                'vendor_id': '[0][0][0][0]'
            }
        }, {
            'index': 2, 
            'codec_name': 'bin_data', 
            'codec_long_name': 'binary data', 
            'codec_type': 'data', 
            'codec_tag_string': 'text', 
            'codec_tag': '0x74786574', 
            'id': '0x3', 
            'r_frame_rate': '0/0', 
            'avg_frame_rate': '0/0', 
            'time_base': '1/90000', 
            'start_pts': 0, 
            'start_time': '0.000000', 
            'duration_ts': 1135080, 
            'duration': '12.612000', 
            'bit_rate': '8', 
            'nb_frames': '1', 
            'extradata_size': 43, 
            'disposition': {
                'default': 0, 
                'dub': 0, 
                'original': 0, 
                'comment': 0, 
                'lyrics': 0, 
                'karaoke': 0, 
                'forced': 0, 
                'hearing_impaired': 0, 
                'visual_impaired': 0, 
                'clean_effects': 0, 
                'attached_pic': 0, 
                'timed_thumbnails': 0, 
                'captions': 0, 
                'descriptions': 0, 
                'metadata': 0, 
                'dependent': 0, 
                'still_image': 0
            }, 
            'tags': {
                'creation_time': '2010-05-11T10:32:06.000000Z', 
                'language': 'und'
            }
        }
    ], 
    'format': {
        'filename': './asset/video1.mp4', 
        'nb_streams': 3, 
        'nb_programs': 0, 
        'format_name': 'mov,mp4,m4a,3gp,3g2,mj2',
        'format_long_name': 'QuickTime / MOV', 
        'start_time': '0.000000', 
        'duration': '12.612000', 
        'size': '318465', 
        'bit_rate': '202007', 
        'probe_score': 100, 
        'tags': {
            'major_brand': 'mp42', 
            'minor_version': '0', 
            'compatible_brands': 'mp42isomavc1', 
            'creation_time': '2010-05-11T10:32:06.000000Z', 
            'encoder': 'HandBrake 0.9.4 2009112300'
        }
    }
}
```

##### 视频截图

方法：_screenshot(output_path[, op])_

参数：

* output_path：图片输出路径
* （可选）op: Operation实例对象

返回：Image

示例：

```python
img = await video.screenshot("xxx")
```

##### 人物抠图

方法：_remove(output_path, model_name, worker_nodes, gpu_batch_size, frame_limit, frame_rate[, op])_

参数：

* output_path: 输出路径
* （可选）model_name: 模型名称
* （可选）worker_nodes: 工作进程数（默认2）
* （可选）gpu_batch_size: GPU批量大小（默认2）
* （可选）frame_limit: 总帧数
* （可选）frame_rate: 帧率
* （可选）timeout: 超时时间（秒）
* （可选）op: Operation实例对象

返回：Video

示例：

```python
video = Video(video3_path)
await video.remove('xxx.webm')
```

>可选模型：u2netp、u2net、u2net_human_seg

注意：

* 一般情况下，`frame_limit`和`frame_rate`无需输入，除非无法正常获取视频总帧数和帧率，可手动指定

* 工具会识别GPU是否可用，若可用，则使用GPU进行算法处理，否则使用CPU

  工具默认安装`torch`和`torchvision`版本如下：

  ```tex
  torch~=2.0.1
  torchvision~=0.15.2
  ```

  请根据设备CUDA版本安装对应的依赖版本，否则可能识别不到CUDA

* 当前仅允许输出`mov`和`webm`格式文件

* 推荐传入`timeout`以防止意外情况所产生的僵尸进程

##### 人脸检测

方法：_face_detection(model_name, proportion, worker_nodes[, op])_

参数：

* （可选）model_name: 模型名称（默认haarcascade_frontalface_alt2）
* （可选）proportion: 人脸出现占比（0~1，默认0.9）
* （可选）worker_nodes: 工作进程数（输入后采用多进程校验）
* （可选）timeout: 超时时间（秒）
* （可选）op: op: Operation实例对象

返回：bool

示例：

```python
video = Video("xxx")
await video.face_detection()
await video.face_detection(worker_nodes=2)
```

>可选模型：haarcascade_frontalface_alt2、haarcascade_fullbody等
>

##### 视频拼接

方法：_concat(output_path, video_list, audio)_

参数：

* output_path: 输出路径

* video_list: 视频列表

  ```json
  {
      "media":Video实例对象,
      "op":Operate实例对象（可选）
  }
  ```

* （可选）audio: 音频

  如果传递该参数，则使用该音频作为最终合成视频的音频流

返回：Video

示例：

```python
# 视频倒放+拼接
video = Video("xxx")
op = Operate().reverse()
await Video.concat('xxx', [{"media": video}, {"media": video, "op": op}])
```

注意：该方法为静态方法，使用`Video.`调用

##### 视频合成

方法：_composite(output_path, media_list, audio, canvas)_

参数：

* output_path: 输出路径

* media_list: 视频/图片列表

  ```json
  {
      "media":Video/Image实例对象,
      "op":Operate实例对象（可选）,
      "start":开始时间（可选）,
      "end":结束时间（可选）,
      "x":在画布中的坐标点（可选）,
      "y":在画布中的坐标点（可选）
  }
  ```

* （可选）audio: 音频

  如果传递该参数，则使用该音频作为最终合成视频的音频流
  
* （可选）canvas: 画布大小

  在默认情况下，合成的视频和第一个剪辑的尺寸相同，但是如果你想让你的剪辑在更大的合成视频里浮动，可以使用该参数：

  ```python
  composite(..., canvas=(1280,720))
  ```

返回：Video

示例：

```python
video1 = Video(video1_path)
video2 = Video(video2_path)
image1 = Image(image1_path)
await Video.composite(f'{output_path}/video_composite.mp4', [
    {"media": video2},
    {"media": video1, "start": 5},
    {"media": image1, "start": 3, "x": 50, "y": 50}
])
```

注意：

* 该方法为静态方法，使用`Video.`调用
* 如果是`Image`实例对象，默认显示10s，若不满足要求，请指定该媒体对象的开始和结束时间
* `Video`实例对象结束时间和开始时间的间隔必须小于视频时长

<br />

#### (4) 音频
```python
from bm_video_tools import Audio
audio = Audio(input_path)
```

参数：

* input_path：文件输入路径

<br />

##### 执行基础操作

方法：_run(op, output_path)_

参数：

* op: Operation实例对象
* output_path：输出路径

返回：Audio

示例：

```python
audio = Audio("xxx")
op = Operate().params(sample='44100')
await audio.run(op, output_path="xxx")
```

##### 查看音频信息

方法：_get_info()_

参数：无

返回：dict

示例：

```python
info = await audio.get_info()
```

##### 音频拼接

方法：_concat(output_path, audio_list)_

参数：

* output_path: 输出路径

* audio_list: 音频列表

  ```json
  {
      "media":Audio实例对象,
      "op":Operate实例对象
  }
  ```

返回：Audio

示例：

```python
audio1 = Audio(audio1_path)
audio2 = Audio(audio2_path)
await Audio.concat(f'{output_path}/audio_concat.mp3', [{"media": audio1}, {"media": audio2}])
```

注意：该方法为静态方法，使用`Audio.`调用

##### 音频合成

方法：_composite(output_path, audio_list)_

参数：

* output_path: 输出路径

* audio_list: 音频列表

  ```json
  {
      "media":Audio实例对象,
      "op":Operate实例对象,
      "start":音频开始时间,
      "end":音频结束时间
  }
  ```

返回：Audio

示例：

```python
audio1 = Audio(audio1_path)
audio2 = Audio(audio2_path)
await Audio.composite(f'{output_path}/audio_composite.mp3', [{"media": audio1, "start": 5}, {"media": audio2}])
```

注意：该方法为静态方法，使用`Audio.`调用
