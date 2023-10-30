import time
import math
import os
import tempfile
import torch
import torch.multiprocessing as multiprocessing
import subprocess as sp
import numpy as np
from moviepy.editor import VideoFileClip

from .net import Net, DEVICE, remove_many


def _producer(input_path, worker_nodes, gpu_batch_size, total_frames, frames_dict, error_dict):
    print(f"Producer online")
    _video_clip = None
    idx = 0
    try:
        _video_clip = VideoFileClip(input_path, target_resolution=(320, None), fps_source='fps')
        _iter_frames = _video_clip.iter_frames(dtype="uint8")

        for idx, frame in enumerate(_iter_frames):
            if idx >= total_frames:
                break
            frames_dict[idx] = frame
            while len(frames_dict) > worker_nodes * gpu_batch_size * 2:
                time.sleep(0.1)
    except Exception as e:
        error_dict["error"] = str(e)
    finally:
        if _video_clip:
            # 释放资源（否则报错：句柄无效）
            _video_clip.close()
        print(f"Producer finished: {idx}")


def _consumer(model_name, worker_nodes, gpu_batch_size, total_frames, frames_dict, results_dict, error_dict, consumer_index):
    print(f"Consumer {consumer_index} online")
    try:
        output_index = consumer_index + 1
        base_index = consumer_index * gpu_batch_size
        net = Net(model_name)
        script_net = None

        group = [list(range(base_index + i * worker_nodes * gpu_batch_size, min(base_index + i * worker_nodes * gpu_batch_size + gpu_batch_size, total_frames)))
                 for i in range(math.ceil(total_frames / worker_nodes / gpu_batch_size))]

        for fi in group:
            if not fi:
                break

            last = fi[-1]
            while last not in frames_dict:
                time.sleep(0.1)

            input_frames = [frames_dict[index] for index in fi]

            if script_net is None:
                script_net = torch.jit.trace(net, torch.as_tensor(np.stack(input_frames), dtype=torch.float32, device=DEVICE))

            results_dict[output_index] = remove_many(input_frames, script_net)

            for fdex in fi:
                del frames_dict[fdex]
            output_index += worker_nodes
    except Exception as e:
        error_dict["error"] = str(e)
    finally:
        print(f"Consumer {consumer_index} finished")


# 关闭进程
def _kill_proc(proc_list, output_proc):
    for proc in proc_list:
        if proc.is_alive():
            proc.kill()
    if output_proc is not None:
        output_proc.stdin.close()
        output_proc.kill()
        output_proc.wait()


# 校验异常
def _check_error(error_dict, proc_list, output_proc):
    if error_dict.get("error"):
        _kill_proc(proc_list, output_proc)
        raise RuntimeError(error_dict.get("error"))


# 校验超时
def _check_timeout(start_time, timeout, proc_list, output_proc):
    if (timeout is not None) and (time.time() - start_time > timeout):
        _kill_proc(proc_list, output_proc)
        raise TimeoutError("transparent timeout")


def matte_key(input_path, matte_path, model_name, worker_nodes, gpu_batch_size, total_frames, frame_rate, timeout):
    manager = multiprocessing.Manager()
    frames_dict = manager.dict()
    results_dict = manager.dict()
    error_dict = manager.dict()

    start_time = time.time()

    producer = multiprocessing.Process(target=_producer, args=(input_path, worker_nodes, gpu_batch_size, total_frames, frames_dict, error_dict))
    workers = [multiprocessing.Process(target=_consumer, args=(model_name, worker_nodes, gpu_batch_size, total_frames, frames_dict, results_dict, error_dict, wi)) for wi in range(worker_nodes)]
    process_list = [producer, *workers]

    for process in process_list:
        process.start()

    command = None
    proc = None
    frame_counter = 0

    for i in range(math.ceil(total_frames / worker_nodes)):
        for wi in range(worker_nodes):
            _check_error(error_dict, process_list, proc)
            _check_timeout(start_time, timeout, process_list, proc)

            hash_index = i * worker_nodes + 1 + wi
            while hash_index not in results_dict:
                _check_error(error_dict, process_list, proc)
                _check_timeout(start_time, timeout, process_list, proc)
                time.sleep(0.1)

            frames = results_dict[hash_index]
            del results_dict[hash_index]

            for frame in frames:
                if command is None:
                    command = ['ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-s', f"{frame.shape[1]}x{frame.shape[0]}", '-pix_fmt', 'gray', '-r', f"{frame_rate}", '-i', '-',
                               '-an', '-vcodec', 'mpeg4', '-b:v', '2000k', '%s' % matte_path]
                    proc = sp.Popen(command, stdin=sp.PIPE)

                proc.stdin.write(frame.tostring())
                frame_counter = frame_counter + 1

                if frame_counter >= total_frames:
                    while not all(not process.is_alive() for process in process_list):
                        _check_error(error_dict, process_list, proc)
                        _check_timeout(start_time, timeout, process_list, proc)
                        time.sleep(0.5)
                    proc.stdin.close()
                    proc.wait()
                    print(F"FINISHED ALL FRAMES ({total_frames})!")
                    return


def transparent(input_path: str, output_path: str, model_name: str, worker_nodes: int, gpu_batch_size: int, total_frames: int, frame_rate: int, timeout: int):
    # 仅允许输出mov和webm格式
    fmt = output_path.split('.')[-1].lower()
    if fmt not in ['mov', 'webm']:
        raise ValueError('output format allow only mov/webm')

    temp_matte = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    temp_matte_path = temp_matte.name.replace("\\", "/")
    temp_matte.close()

    try:
        matte_key(input_path, temp_matte_path, model_name, worker_nodes, gpu_batch_size, total_frames, frame_rate, timeout)

        print("Starting alpha merge")
        if fmt == 'mov':
            c_v = 'qtrle'
        elif fmt == 'webm':
            c_v = 'libvpx-vp9'
        else:
            raise ValueError('output format allow only mov/webm')

        cmd = r'ffmpeg -v error -i {} -i {} ' \
              r'-filter_complex "[1][0]scale2ref[mask][main];[main][mask]alphamerge=shortest=1" ' \
              r'-c:v {} -shortest {} -y'.format(input_path, temp_matte_path, c_v, output_path)

        process = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            raise RuntimeError(stderr)

        print("Process finished")
    finally:
        if os.path.exists(temp_matte_path):
            os.remove(temp_matte_path)
