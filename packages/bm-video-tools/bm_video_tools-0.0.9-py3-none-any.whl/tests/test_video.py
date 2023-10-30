import asyncio
import os
import tempfile
import multiprocessing

from bm_video_tools import Video, Image, Audio, Operate

from tests.test_source import video1_path, video2_path, video3_path, audio2_path, image1_path, output_path

multiprocessing.set_start_method('spawn', force=True)


# 查看视频信息
async def test_info():
    video = Video(video1_path)
    info = await video.get_info()
    print(info)


# 修改视频参数
async def test_params():
    video = Video(video1_path)
    op = Operate().params(fps=15)
    await video.run(op, output_path=f'{output_path}/video1_params.mp4')


# 视频裁剪
async def test_cut():
    video = Video(video1_path)
    op = Operate().cut(150, 150)
    await video.run(op, output_path=f'{output_path}/video1_cut.mp4')


# 视频缩放
async def test_scale():
    video = Video(video1_path)
    op = Operate().scale(150, -1)
    await video.run(op, output_path=f'{output_path}/video1_scale.mp4')


# 视频旋转
async def test_rotate():
    video = Video(video1_path)
    op = Operate().rotate(1)
    await video.run(op, output_path=f'{output_path}/video1_rotate.mp4')


# 视频翻转
async def test_turn():
    video = Video(video1_path)
    op = Operate().turn(v=True)
    await video.run(op, output_path=f'{output_path}/video1_turn.mp4')


# 视频旋转+翻转
async def test_rotate_turn():
    video = Video(video1_path)
    op = Operate().rotate(2).turn(h=True).rotate(1)
    await video.run(op, output_path=f'{output_path}/video1_rotate_turn.mp4')


# 视频拆分
async def test_split():
    video = Video(video1_path)
    op = Operate().split(5, second=5)
    await video.run(op, output_path=f'{output_path}/video1_split.mp4')


# 视频倒放
async def test_reverse():
    video = Video(video1_path)
    op = Operate().reverse()
    await video.run(op, output_path=f'{output_path}/video1_reverse.mp4')


# 倍速播放
async def test_speed():
    video1 = Video(video1_path)
    op = Operate().speed(0.5)
    await video1.run(op, output_path=f'{output_path}/video1_speed.mp4')


# 视频截图
async def test_screenshot():
    video = Video(video1_path)
    op = Operate().split(5, second=5).cut(200, 200)

    # 使用临时文件执行操作，对操作后的临时文件进行截图
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    temp_file_path = temp_file.name.replace("\\", "/")
    temp_file.close()

    try:
        video_res = await video.run(op, output_path=temp_file_path)
        await video_res.screenshot(output_path=f'{output_path}/video1_screenshot.jpg')
        del video_res
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    # 上述代码等同于
    # await video.screenshot(output_path=f'{output_path}/video1_screenshot.jpg', op=op)


# 视频拼接
async def test_concat():
    video1 = Video(video1_path)
    video2 = Video(video2_path)
    op = Operate().scale(480, 320).params(fps=30)
    await Video.concat(f'{output_path}/video_concat.mp4', [{"media": video1, "op": op}, {"media": video2, "op": op}])


# 视频倒放+拼接
async def test_reverse_concat():
    video = Video(video1_path)
    op = Operate().reverse()
    await Video.concat(f'{output_path}/video1_reverse_concat.mp4', [{"media": video}, {"media": video, "op": op}])


# 人物抠图
async def test_remove():
    video = Video(video3_path)
    await video.remove(f'{output_path}/video3_remove.webm')


# 人物抠图（超时）
async def test_remove_timeout():
    video = Video(video3_path)
    try:
        await video.remove(f'{output_path}/video3_remove_timeout.webm', timeout=30)
    except TimeoutError as e:
        print("remove timeout")


# 人脸检验
async def test_face_detection():
    video = Video(video3_path)
    print(f"test_face_detection result: {await video.face_detection()}")


# 人脸检测-多线程
async def test_face_detection_parallel():
    video = Video(video3_path)
    print(f"test_face_detection_parallel result: {await video.face_detection(worker_nodes=2)}")


# 视频合成
async def test_composite():
    video1 = Video(video1_path)
    video3 = Video(video3_path)
    image1 = Image(image1_path)
    await Video.composite(f'{output_path}/video_composite.mp4', [
        {"media": video3},
        {"media": video1, "start": 5},
        {"media": image1, "start": 3, "x": 50, "y": 50}
    ])


# 视频合成（综合）
async def test_composite_mix():
    video1 = Video(video1_path)
    video3 = Video(video3_path)
    image1 = Image(image1_path)
    audio2 = Audio(audio2_path)

    op = Operate().eliminate(a=True)

    await Video.composite(f'{output_path}/video_composite_mix.mp4', [
        {"media": video3, "op": op},
        {"media": video1, "start": 5, "op": op},
        {"media": image1, "start": 3, "x": 50, "y": 50}
    ], audio=audio2, canvas=(1280, 720))


if __name__ == '__main__':
    async def main():
        await asyncio.gather(
            # test_info(),
            # test_params(),
            # test_cut(),
            # test_scale(),
            # test_rotate(),
            # test_turn(),
            # test_rotate_turn(),
            # test_split(),
            # test_reverse(),
            # test_speed(),
            # test_screenshot(),
            # test_concat(),
            # test_reverse_concat(),
            # test_remove(),
            # test_remove_timeout(),
            # test_face_detection(),
            # test_face_detection_parallel(),
            # test_composite(),
            # test_composite_mix()
        )


    asyncio.run(main())
