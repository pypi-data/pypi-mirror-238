import setuptools

with open("README.md", "r", encoding="utf-8") as stream:
    long_description = stream.read()

setuptools.setup(
    name="bm_video_tools",
    version="0.0.9",
    author="galaxyeye",
    author_email="galaxyeye.wechat@galaxyeye-tech.com",
    description="音视频处理工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        r"numpy~=1.24.4",
        r"scikit-image~=0.21.0",
        r"pillow~=10.0.1",
        r"moviepy~=1.0.3",
        r"opencv-python~=4.8.1.78",
        r"torch~=2.0.1",
        r"torchvision~=0.15.2",
    ],
)
