from __future__ import annotations
import asyncio
import functools

from .media import Media
from .operate import Operate
from .utils import backslash2slash, pre_operate, subprocess_exec
from .remover.transparent_image import transparent
from .detection.face_detection_image import face_detection


class Image(Media):
    async def run(self, op: Operate, output_path: str) -> Image:
        """
        执行操作
        :param op: Operation实例对象
        :param output_path: 输出路径
        :return: 媒体对象
        """
        output_path = backslash2slash(output_path)

        cmd = op.exec(o_v=True)
        await subprocess_exec(cmd, self.input_path, output_path)

        return self.__class__(output_path)

    @pre_operate(suffix='.png')
    async def remove(self, output_path: str, model_name: str = 'u2net_human_seg', **kwargs) -> Image:
        """
        人像抠图
        :param output_path: 输出路径
        :param model_name: 模型名称
        :return: 图片对象
        """
        output_path = backslash2slash(output_path)
        temp_media: Image = kwargs.get("temp_media")
        input_path = temp_media.input_path if temp_media else self.input_path

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, functools.partial(transparent, input_path, output_path, model_name))

        return self.__class__(output_path)

    @pre_operate(suffix='.png')
    async def face_detection(self, model_name: str = 'haarcascade_frontalface_alt2', **kwargs) -> bool:
        """
        检测人脸
        :param model_name: 人脸检测模型
        :return 图片中是否包含人脸
        """
        temp_media: Image = kwargs.get("temp_media")
        input_path = temp_media.input_path if temp_media else self.input_path

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, functools.partial(face_detection, input_path, model_name))

        return result
