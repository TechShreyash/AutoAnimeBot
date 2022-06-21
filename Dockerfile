FROM shosoar/alpine-python-opencv

RUN apt-get upgrade
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
