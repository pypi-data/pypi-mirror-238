from __future__ import annotations
import asyncio
import functools
import math
import os
import tempfile
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip, AudioFileClip

from .media import Media
from .image import Image
from .audio import Audio
from .operate import Operate
from .utils import backslash2slash, pre_operate, subprocess_exec
from .remover.transparent_video import transparent
from .detection.face_detection_video import face_detection


class Video(Media):
    async def run(self, op: Operate, output_path: str) -> Video:
        """
        执行操作
        :param op: Operation实例对象
        :param output_path: 输出路径
        :return: 媒体对象
        """
        output_path = backslash2slash(output_path)

        cmd = op.exec()
        await subprocess_exec(cmd, self.input_path, output_path)

        return self.__class__(output_path)

    @pre_operate(suffix='.mp4')
    async def screenshot(self, output_path: str, **kwargs) -> Image:
        """
        视频截图
        :param output_path: 输出图片存放路径
        :return: 图片对象
        """
        output_path = backslash2slash(output_path)
        temp_media: Video = kwargs.get("temp_media")
        input_path = temp_media.input_path if temp_media else self.input_path

        cmd = r'ffmpeg -i {} -ss 0 -frames:v 1 -y -v error {}'
        await subprocess_exec(cmd, input_path, output_path)

        return Image(output_path)

    @pre_operate(suffix='.mp4')
    async def remove(self, output_path: str,
                     model_name: str = 'u2net_human_seg',
                     worker_nodes: int = 2, gpu_batch_size: int = 2,
                     frame_limit: int = -1, frame_rate: int = -1,
                     timeout: int = None, **kwargs) -> Video:
        """
        人像抠图
        :param output_path: 输出路径
        :param model_name: 模型名称
        :param worker_nodes: 工作进程数
        :param gpu_batch_size: GPU批量大小
        :param frame_limit: 总帧数
        :param frame_rate: 帧率
        :param timeout: 超时时间（秒）
        :return: 视频对象
        """
        output_path = backslash2slash(output_path)
        temp_media: Video = kwargs.get("temp_media")

        if temp_media:
            input_path = temp_media.input_path
            video_info = await temp_media.get_info()
        else:
            input_path = self.input_path
            video_info = await self.get_info()

        video_stream = next((s for s in video_info["streams"] if s["codec_type"] == "video"), None)
        if not video_stream:
            raise RuntimeError("no video stream")

        total_frames = int(video_stream["nb_frames"])
        if frame_limit != -1:
            total_frames = min(frame_limit, total_frames)

        fr = video_stream["r_frame_rate"]
        if frame_rate == -1:
            print(F"FRAME RATE DETECTED: {fr} (if this looks wrong, override the frame rate)")
            frame_rate = math.ceil(eval(fr))

        print(F"FRAME RATE: {frame_rate} TOTAL FRAMES: {total_frames}")

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, functools.partial(transparent, input_path, output_path, model_name, worker_nodes, gpu_batch_size, total_frames, frame_rate, timeout))

        return self.__class__(output_path)

    @pre_operate(suffix='.mp4')
    async def face_detection(self, model_name: str = 'haarcascade_frontalface_alt2',
                             proportion: float = 0.9,
                             worker_nodes: int = None,
                             timeout: int = None, **kwargs) -> bool:
        """
        视频逐帧检测人脸
        :param model_name: 人脸检测模型
        :param proportion: 人脸出现占比（0~1）
        :param worker_nodes: 工作进程数（输入后采用多进程校验）
        :param timeout: 超时时间（秒）
        :return 视频中人脸占比是否超过指定值
        """
        temp_media: Video = kwargs.get("temp_media")

        if temp_media:
            input_path = temp_media.input_path
            video_info = await temp_media.get_info()
        else:
            input_path = self.input_path
            video_info = await self.get_info()

        video_stream = next((s for s in video_info["streams"] if s["codec_type"] == "video"), None)
        if not video_stream:
            raise RuntimeError("no video stream")

        total_frames = int(video_stream["nb_frames"])

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, functools.partial(face_detection, input_path, model_name, total_frames, proportion, worker_nodes, timeout))

        return result

    @staticmethod
    async def concat(output_path: str, video_list: list, audio: Audio = None) -> Video:
        """
        视频拼接
        :param output_path: 输出视频路径
        :param video_list: 视频列表
        :param audio: 音频
        :return: 视频对象
        """
        output_path = backslash2slash(output_path)

        temp_path_list = []
        try:
            clips = []
            for item in video_list:
                media = item["media"]
                if not isinstance(media, Video):
                    raise ValueError("only can concat video files")

                if "op" in item and isinstance(item.get("op"), Operate):
                    op = item.get("op")
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ts')
                    temp_file_path = backslash2slash(temp_file.name)
                    temp_file.close()

                    temp_path_list.append(temp_file_path)
                    media = await media.run(op, temp_file_path)

                clips.append(VideoFileClip(media.input_path))

            def _content():
                final_clip: CompositeVideoClip = concatenate_videoclips(clips)
                # 修改音频
                audio_clip = None
                if audio:
                    audio_clip = AudioFileClip(audio.input_path)
                    final_clip = final_clip.set_audio(audio_clip)
                # 保存文件
                final_clip.write_videofile(output_path, logger=None)
                # 释放资源
                for video_clip in clips:
                    video_clip.close()
                if audio_clip:
                    audio_clip.close()
                final_clip.close()

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, _content)

            return Video(output_path)
        finally:
            for temp_path in temp_path_list:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    @staticmethod
    async def composite(output_path: str, media_list: list, audio: Audio = None, canvas: tuple = None):
        """
        视频合成
        :param output_path: 输出路径
        :param media_list: 视频列表
        :param audio: 音频
        :param canvas: 画布大小
        :return: 视频对象
        """
        output_path = backslash2slash(output_path)

        temp_path_list = []
        try:
            clips = []
            for item in media_list:
                media = item["media"]
                if isinstance(media, Video):
                    clip_class = VideoFileClip
                    suffix = '.ts'
                elif isinstance(media, Image):
                    clip_class = ImageClip
                    suffix = '.png'
                    if ("end" not in item) and ("duration" not in item):
                        item["duration"] = 10
                else:
                    raise ValueError("only can composite video/image files")

                if "op" in item and isinstance(item.get("op"), Operate):
                    op = item.get("op")
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                    temp_file_path = backslash2slash(temp_file.name)
                    temp_file.close()

                    temp_path_list.append(temp_file_path)
                    media = await media.run(op, temp_file_path)

                clip = clip_class(media.input_path)
                if "start" in item:
                    clip = clip.set_start(item.get("start"))
                if "end" in item:
                    clip = clip.set_end(item.get("end"))
                if "duration" in item:
                    clip = clip.set_duration(item.get("duration"))
                if "x" in item or "y" in item:
                    clip = clip.set_position((item.get("x", 0), item.get("y", 0)))

                clips.append(clip)

            def _composite():
                # 修改画布大小
                if canvas:
                    final_clip = CompositeVideoClip(clips, size=canvas)
                else:
                    final_clip = CompositeVideoClip(clips)
                # 修改音频
                audio_clip = None
                if audio:
                    audio_clip = AudioFileClip(audio.input_path)
                    final_clip = final_clip.set_audio(audio_clip)
                # 保存文件
                final_clip.write_videofile(output_path, logger=None)
                # 释放资源
                for video_clip in clips:
                    video_clip.close()
                if audio_clip:
                    audio_clip.close()
                final_clip.close()

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, _composite)

            return Video(output_path)
        finally:
            for temp_path in temp_path_list:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
