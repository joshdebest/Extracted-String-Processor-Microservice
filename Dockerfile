FROM tensorflow/tensorflow:devel-gpu

SHELL ["/bin/bash", "-c"]

RUN apt update && apt upgrade -y && \
apt install -y \
build-essential \
cmake \
wget \
unzip \
pkg-config \
libjpeg-dev \
libpng-dev \
libtiff-dev \
libavcodec-dev \
libavformat-dev \
libswscale-dev \
libv4l-dev \
libxvidcore-dev \
libx264-dev \
libgtk-3-dev \
libatlas-base-dev \
libtbb-dev \
gfortran \
python3-dev


RUN apt install -y \
libmysqlclient-dev \
libssl-dev \
g++

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

COPY requirements.txt /usr/local/service/requirements.txt
WORKDIR /usr/local/service
RUN pip install -r requirements.txt

COPY . .


EXPOSE 8090
CMD python3 -u server.py