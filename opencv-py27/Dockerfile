FROM ubuntu:trusty

# https://github.com/ampervue/docker-python27-opencv

MAINTAINER David Karchmer <dkarchmer@gmail.com>

########################################
#
# Image based on Ubuntu:trusty
#
#   with Python 2.7
#   and OpenCV 3 (built)
#   plus a bunch of build essencials
#######################################

# Set Locale

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt-get -qq remove ffmpeg

RUN echo deb http://archive.ubuntu.com/ubuntu precise universe multiverse >> /etc/apt/sources.list; \
    apt-get update -qq && apt-get install -y --force-yes \
    curl \
    git \
    g++ \
    autoconf \
    automake \
    mercurial \
    libopencv-dev \
    build-essential \
    checkinstall \
    cmake \
    pkg-config \
    yasm \
    libtiff4-dev \
    libpng-dev \
    libjpeg-dev \
    libjasper-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libgtk2.0-dev \
    libtool \
    python2.7 \
    python2.7-dev \
    python-numpy \
    wget \
    unzip; \
    apt-get clean

ENV OPENCV_VERSION  2.4.10

WORKDIR /usr/local/src

RUN git clone https://github.com/Itseez/opencv.git

# Build OpenCV 3.x
# =================================
RUN apt-get update -qq && apt-get install -y --force-yes libopencv-dev
WORKDIR /usr/local/src
RUN mkdir -p opencv/release
WORKDIR /usr/local/src/opencv/release
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D BUILD_PYTHON_SUPPORT=ON \
          ..

RUN make -j4
RUN make install
RUN sh -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'
RUN ldconfig
# =================================

# Remove all tmpfile
# =================================
WORKDIR /usr/local/
RUN rm -rf /usr/local/src
# =================================

# Install pip
# =================================
RUN curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python
