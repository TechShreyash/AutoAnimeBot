RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN apt-get install libgtk2.0-dev && apt-get install pkg-config
