FROM shosoar/alpine-python-opencv

RUN pip install -U opencv-python
RUN apt-get upgrade
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
RUN pip uninstall opencv-python-headless -y 
RUN pip install opencv-python --upgrade
