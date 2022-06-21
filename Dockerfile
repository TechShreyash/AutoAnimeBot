RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN RUN pip3 install opencv-python-headless==4.5.3.56