RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN apt-get install libgtk2.0-dev && apt-get install pkg-config
RUN apt-get install -y python3-opencv
RUN apt-get install libgl1
RUN apt-get install ffmpeg libsm6 libxext6 -y
