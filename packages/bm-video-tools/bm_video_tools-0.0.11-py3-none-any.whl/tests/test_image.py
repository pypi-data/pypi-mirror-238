import asyncio
from bm_video_tools import Image, Operate

from tests.test_source import image1_path, image2_path, image3_path, output_path


# 查看图片信息
async def test_info():
    img = Image(image1_path)
    info = await img.get_info()
    print(info)


# 图片裁剪
async def test_cut():
    img = Image(image1_path)
    op = Operate().cut(300, 300, 0, 0).cut(100, 100, 0, 0)
    await img.run(op, output_path=f'{output_path}/image1_cut.jpg')


# 图片缩放
async def test_scale():
    img = Image(image1_path)
    op = Operate().scale(200, -1)
    await img.run(op, output_path=f'{output_path}/image1_scale.jpg')


# 图片旋转
async def test_rotate():
    img = Image(image1_path)
    op = Operate().rotate(1)
    await img.run(op, output_path=f'{output_path}/image1_rotate.jpg')


# 图片翻转
async def test_turn():
    img = Image(image1_path)
    op = Operate().turn(v=True)
    await img.run(op, output_path=f'{output_path}/image1_turn.jpg')


# 图片旋转+翻转
async def test_rotate_turn():
    img = Image(image1_path)
    op = Operate().rotate(2).turn(h=True).rotate(1)
    await img.run(op, output_path=f'{output_path}/image1_rotate_turn.jpg')


# 人物抠图
async def test_remove():
    img = Image(image2_path)
    await img.remove(f'{output_path}/image2_remove.png')


# 人脸检测
async def test_face_detection():
    img = Image(image3_path)
    print(f"face_detection result: {await img.face_detection()}")


if __name__ == '__main__':
    async def main():
        await asyncio.gather(
            test_info(),
            test_cut(),
            test_scale(),
            test_rotate(),
            test_turn(),
            test_rotate_turn(),
            test_remove(),
            test_face_detection()
        )


    asyncio.run(main())
