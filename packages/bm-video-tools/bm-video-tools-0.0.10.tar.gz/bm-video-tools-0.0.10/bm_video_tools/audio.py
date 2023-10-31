from __future__ import annotations
import tempfile
import asyncio
import os
from moviepy.editor import AudioFileClip, concatenate_audioclips, CompositeAudioClip

from .media import Media
from .operate import Operate
from .utils import backslash2slash, subprocess_exec


class Audio(Media):
    async def run(self, op: Operate, output_path: str) -> Audio:
        """
        执行操作
        :param op: Operation实例对象
        :param output_path: 输出路径
        :return: 媒体对象
        """
        output_path = backslash2slash(output_path)

        cmd = op.exec(o_a=True)
        await subprocess_exec(cmd, self.input_path, output_path)

        return self.__class__(output_path)

    @staticmethod
    async def concat(output_path: str, audio_list: list) -> Audio:
        """
        音频拼接
        :param output_path: 输出路径
        :param audio_list: 音频列表
        :return: 音频对象
        """
        output_path = backslash2slash(output_path)

        temp_path_list = []
        try:
            clips = []
            for item in audio_list:
                media = item["media"]
                if not isinstance(media, Audio):
                    raise ValueError("only can concat audio files")

                if "op" in item and isinstance(item.get("op"), Operate):
                    op = item.get("op")
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                    temp_file_path = backslash2slash(temp_file.name)
                    temp_file.close()

                    temp_path_list.append(temp_file_path)
                    media = await media.run(op, temp_file_path)

                clips.append(AudioFileClip(media.input_path))

            def _content():
                final_clip: CompositeAudioClip = concatenate_audioclips(clips)
                final_clip.write_audiofile(output_path, logger=None)

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, _content)

            return Audio(output_path)
        finally:
            for temp_path in temp_path_list:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    @staticmethod
    async def composite(output_path: str, audio_list: list) -> Audio:
        """
        音频合成
        :param output_path: 输出路径
        :param audio_list: 音频列表
        :return: 音频对象
        """
        output_path = backslash2slash(output_path)

        temp_path_list = []
        try:
            clips = []
            for item in audio_list:
                media = item["media"]
                if not isinstance(media, Audio):
                    raise ValueError("only can composite audio files")

                if "op" in item and isinstance(item.get("op"), Operate):
                    op = item.get("op")
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                    temp_file_path = backslash2slash(temp_file.name)
                    temp_file.close()

                    temp_path_list.append(temp_file_path)
                    media = await media.run(op, temp_file_path)

                clip = AudioFileClip(media.input_path)
                if "start" in item:
                    clip = clip.set_start(item.get("start"))
                if "end" in item:
                    clip = clip.set_end(item.get("end"))

                clips.append(clip)

            def _composite():
                final_clip = CompositeAudioClip(clips)
                final_clip.fps = 44100
                final_clip.write_audiofile(output_path, logger=None)

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, _composite)

            return Audio(output_path)
        finally:
            for temp_path in temp_path_list:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
