import asyncio

from bm_video_tools import Audio, Operate

from tests.test_source import audio1_path, audio2_path, output_path


# 查看音频信息
async def test_info():
    audio = Audio(audio1_path)
    info = await audio.get_info()
    print(info)


# 修改音频参数
async def test_params():
    audio = Audio(audio1_path)
    op = Operate().params(sample='44100')
    await audio.run(op, output_path=f'{output_path}/audio1_params.mp3')


# 音频拆分
async def test_split():
    audio = Audio(audio1_path)
    op = Operate().split('00:00:00', second=5)
    await audio.run(op, output_path=f'{output_path}/audio1_split.mp3')


# 倍速播放
async def test_speed():
    audio = Audio(audio1_path)
    op = Operate().speed(0.5)
    await audio.run(op, output_path=f'{output_path}/audio1_speed.mp3')


# 音频拼接
async def test_concat():
    audio1 = Audio(audio1_path)
    audio2 = Audio(audio2_path)
    await Audio.concat(f'{output_path}/audio_concat.mp3', [{"media": audio1}, {"media": audio2}])


# 音频合成
async def test_composite():
    audio1 = Audio(audio1_path)
    audio2 = Audio(audio2_path)
    await Audio.composite(f'{output_path}/audio_composite.mp3', [{"media": audio1, "start": 5}, {"media": audio2}])


if __name__ == '__main__':
    async def main():
        await asyncio.gather(
            test_info(),
            test_params(),
            test_split(),
            test_speed(),
            test_concat(),
            test_composite()
        )


    asyncio.run(main())
