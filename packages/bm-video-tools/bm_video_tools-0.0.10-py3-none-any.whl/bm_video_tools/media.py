from __future__ import annotations
import json

from .utils import backslash2slash, subprocess_exec


class Media:
    def __init__(self, input_path: str):
        self._input_path = backslash2slash(input_path)

    @property
    def input_path(self):
        return self._input_path

    @input_path.setter
    def input_path(self, value):
        raise ValueError('change is not allowed')

    async def get_info(self) -> dict:
        """
        查看媒体信息
        :return: 媒体详细信息
        """
        cmd = r'ffprobe -i {} -v error -show_format -show_streams -print_format json'
        res = await subprocess_exec(cmd, self.input_path)
        return json.loads(res)
