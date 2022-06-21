FROM shosoar/alpine-python-opencv

pip install -U opencv-python
apt-get upgrade
apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
