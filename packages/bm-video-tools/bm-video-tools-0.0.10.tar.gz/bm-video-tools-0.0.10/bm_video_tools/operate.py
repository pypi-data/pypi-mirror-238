from __future__ import annotations


class Operate(object):
    def __init__(self):
        self._opts = {
            "normal": {
                "-y": None,
                "-v": "error",
            },
            "audio": {
                "-af": []
            },
            "video": {
                "-vf": [],
            }
        }

    def exec(self, o_v: bool = False, o_a: bool = False) -> str:
        args = ""
        for key, value in self._opts.items():
            if (o_a and key == 'video') or (o_v and key == 'audio'):
                continue
            for opt, param in value.items():
                if param is None:
                    args += f'{opt} '
                elif isinstance(param, list):
                    if len(param) > 0:
                        args += r'{} "{}" '.format(opt, ','.join(param))
                else:
                    args += r'{} {} '.format(opt, param)

        cmd = fr'ffmpeg -i {{}} {args} {{}}'

        return cmd

    def params(self, pix_fmt: str = None, codec_v: str = None, fps: int = None, frames_v: int = None, codec_a: str = None, sample: str = None, frames_a: int = None) -> Operate:
        """
        更改相关参数
        :param pix_fmt: 像素格式
        :param codec_v: 视频编码器
        :param fps: 视频帧速率
        :param frames_v: 视频总帧数
        :param codec_a: 音频编码器
        :param sample: 采样率（44100）
        :param frames_a: 音频帧数
        """
        if pix_fmt is not None:
            self._opts["normal"]["-pix_fmt"] = pix_fmt

        if codec_v is not None:
            self._opts["video"]["-codec:v"] = codec_v
        if fps is not None:
            self._opts["video"]["-r"] = fps
        if frames_v is not None:
            self._opts["video"]["-frames:v"] = frames_v

        if codec_a is not None:
            self._opts["audio"]["-codec:a"] = codec_a
        if sample is not None:
            self._opts["audio"]["-ar"] = sample
        if frames_a is not None:
            self._opts["audio"]["-frames:a"] = frames_a

        return self

    def cut(self, width: int = 0, height: int = 0, x: int = 0, y: int = 0) -> Operate:
        """
        裁剪
        :param width: 裁剪的宽度
        :param height: 裁剪的高度
        :param x: 裁剪的坐标点（默认0）
        :param y: 裁剪的坐标点（默认0）
        """
        if width <= 0:
            width = f'in_w-{x}'
        if height <= 0:
            height = f'in_h-{y}'

        crop_params = f"crop={width}:{height}:{x}:{y}"
        self._opts["video"]["-vf"].append(crop_params)

        return self

    def scale(self, width: int, height: int) -> Operate:
        """
        缩放
        如果指定宽度和高度，则按照指定的值进行缩放，如果宽度或高度为-1，则按照指定值等比例缩放
        :param width: 缩放的宽度
        :param height: 缩放的高度
        """
        scale_params = f"scale={width}:{height},pad=ceil(iw/2)*2:ceil(ih/2)*2"
        self._opts["video"]["-vf"].append(scale_params)

        return self

    def rotate(self, unit: int) -> Operate:
        """
        旋转
        :param unit: 旋转角度（1=90° 2=180° 3=270° -1=-90°）
        """
        unit = unit % 4
        if unit == 0:
            return self

        if unit == 1:
            self._opts["video"]["-vf"].append("transpose=1")
        elif unit == 2:
            self.turn(h=True, v=True)
        elif unit == 3:
            self._opts["video"]["-vf"].append("transpose=2")

        return self

    def turn(self, h: bool = False, v: bool = False) -> Operate:
        """
        翻转
        :param h: 水平翻转
        :param v: 垂直翻转
        """
        if not h and not v:
            return self

        if h:
            if "hflip" in self._opts["video"]["-vf"]:
                self._opts["video"]["-vf"].remove("hflip")
            else:
                self._opts["video"]["-vf"].append("hflip")
        if v:
            if "vflip" in self._opts["video"]["-vf"]:
                self._opts["video"]["-vf"].remove("vflip")
            else:
                self._opts["video"]["-vf"].append("vflip")

        return self

    def split(self, start: str | int = None, end: str | int = None, second: int = None) -> Operate:
        """
        拆分
        :param start: 开始时间
        :param end: 结束时间
        :param second: 截取时长（秒）
        """
        if start is not None:
            self._opts["normal"]["-ss"] = start
        if end is not None:
            self._opts["normal"]["-to"] = end
        if second is not None:
            self._opts["normal"]["-t"] = second

        return self

    def eliminate(self, a=False, v=False) -> Operate:
        """
        剔除音频/视频流
        :param a: 剔除音频流
        :param v: 剔除视频流
        """
        if a:
            self._opts["audio"]["-an"] = None
        if v:
            self._opts["video"]["-vn"] = None

        return self

    def reverse(self) -> Operate:
        """
        倒放
        """
        self._opts["video"]["-vf"].append("reverse")
        self._opts["audio"]["-af"].append("areverse")

        return self

    def speed(self, rate: float) -> Operate:
        """
        倍速播放
        :param rate: 速率
        """
        if rate < 0.5 or rate > 2:
            raise ValueError('rate must be be between 0.5 and 2')

        self._opts["video"]["-vf"].append(f"setpts={'%.1f' % (1 / rate)}*PTS")
        self._opts["audio"]["-af"].append(f"atempo={'%.1f' % rate}")

        return self
