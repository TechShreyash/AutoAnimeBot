RUN apt-get update && apt-get ugrade
RUN pip3 install -r requirements.txt
RUN pip3 uninstall opencv-python && pip3 install opencv-python-headless
