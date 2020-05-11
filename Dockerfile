FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
MAINTAINER Satyalab, satya-group@lists.andrew.cmu.edu

RUN apt-get update --fix-missing \
    && apt-get upgrade -y \
    && apt-get install -y \
    --no-install-recommends \
    apt-utils

RUN apt-get install -y \
    build-essential \
    cmake \
    python3 \
    python3-dev \
    python3-pip \
    wget \
    unzip

#################################
# Install OpenCV
#################################

# Install OpenCV requirements
RUN apt-get install -y \
    cmake \
    git \
    libgtk2.0-dev \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libatlas-base-dev \
    gfortran \
    libtbb-dev \
    liblapack-dev \
    libeigen3-dev

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade numpy

# Download and Configure OpenCV
# DNN module requires nvidia comptue capbility >= 5.3
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.2.0.zip && \
    unzip opencv.zip && \
    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.2.0.zip && \
    unzip opencv_contrib.zip && \
    cd opencv-4.2.0 && \
    mkdir build && \
    cd build && \
    cmake -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D WITH_CUDA=ON \
    -D CUDA_ARCH_BIN=5.3,6.0,6.1,7.0,7.5 \
    -D CUDA_FAST_MATH=1 \
    -D WITH_CUBLAS=1 \
    -D WITH_TBB=ON \
    -D WITH_EIGEN=1 \
    -D ENABLE_FAST_MATH=1 \
    -D BUILD_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib-4.2.0/modules \
    .. && \
    make -j8 && \
    make install

#################################
# Install Ribloc
#################################
COPY ./requirements.txt /requirements.txt
COPY ./ribloc /ribloc
RUN python3 -m pip install -r /requirements.txt

# download/extract model for sandwich
RUN cd /ribloc/model && \
    wget https://storage.cmusatyalab.org/gabriel-model/ribloc-model.zip && \
    unzip ribloc-model.zip

EXPOSE 9099
ENTRYPOINT ["python3"]
CMD ["-m", "ribloc"]
