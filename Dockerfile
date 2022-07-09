#FROM nikolaik/python-nodejs:python3.9-nodejs18
FROM scratch

RUN apt-get upgrade
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
RUN apt-get install -y --no-install-recommends ffmpeg

COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

CMD python3 -m main
