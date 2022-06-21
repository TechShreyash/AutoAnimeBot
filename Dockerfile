RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN pip3 install opencv-python-headless==4.5.3.56
RUN apt-get install libgtk2.0-dev && apt-get install pkg-config