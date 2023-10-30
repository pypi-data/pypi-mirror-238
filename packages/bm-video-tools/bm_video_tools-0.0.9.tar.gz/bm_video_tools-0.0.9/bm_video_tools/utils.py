import os
import tempfile
import shlex
import asyncio

from bm_video_tools.operate import Operate


def backslash2slash(path):
    return path.replace("\\", "/")


def pre_operate(suffix):
    def wrapper(func):
        async def inner(self, *args, **kwargs):
            if "op" in kwargs and isinstance(kwargs.get("op"), Operate):
                op = kwargs.get("op")

                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                temp_file_path = backslash2slash(temp_file.name)
                temp_file.close()
                try:
                    temp_media = await self.run(op, temp_file_path)
                    result = await func(self, *args, **kwargs, temp_media=temp_media)
                    return result
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
            else:
                result = await func(self, *args, **kwargs)
                return result

        return inner

    return wrapper


async def subprocess_exec(cmd: str, *args) -> bytes:
    cmd = cmd.format(*args)
    print(f'exec: {cmd}')
    proc = await asyncio.create_subprocess_exec(*shlex.split(cmd), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if stderr:
        raise RuntimeError(stderr.decode('utf-8'))
    return stdout
