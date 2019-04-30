FROM ripl/libbot2-pcl-ros:latest

# set working directory
ENV WORKDIR "/code"
WORKDIR /code

# define arguments
ARG NCORES=2
ARG VERBOSE=0
ARG DIRECTOR_SOURCE_DIR="$WORKDIR/director"
ARG DIRECTOR_BUILD_DIR="$WORKDIR/director-build"

# set environment
ENV DIRECTOR_INSTALL_DIR "/usr/local"

# install dependencies
RUN apt update \
  && apt install -y \
    git \
    lsb-core \
    build-essential \
    cmake \
    libglib2.0-dev \
    libqt4-dev \
    libx11-dev \
    libxext-dev \
    libxt-dev \
    libboost-all-dev \
    libeigen3-dev \
    python3-dev \
    python3-lxml \
    python3-numpy \
    python3-scipy \
    python3-yaml \
  && rm -rf /var/lib/apt/lists/*

# copy source code
RUN mkdir -p $DIRECTOR_SOURCE_DIR
COPY ./ $DIRECTOR_SOURCE_DIR/

# build director
RUN mkdir -p $DIRECTOR_BUILD_DIR \
  && cd $DIRECTOR_BUILD_DIR \
  && cmake \
    -DCMAKE_CXX_FLAGS_RELEASE="-fPIC -g -fno-omit-frame-pointer -O3 -DNDEBUG" \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_PCL:BOOL=ON \
    -DUSE_LCM:BOOL=OFF \
    -DUSE_SYSTEM_VTK:BOOL=OFF \
    -DUSE_SYSTEM_PCL:BOOL=ON \
    -DUSE_SYSTEM_EIGEN:BOOL=ON \
    -DUSE_EXTERNAL_INSTALL:BOOL=ON \
    -DCMAKE_INSTALL_PREFIX:PATH=$DIRECTOR_INSTALL_DIR \
    $DIRECTOR_SOURCE_DIR/distro/superbuild \
  && make \
    VERBOSE=${VERBOSE} \
    -j${NCORES} \
  && cd $WORKDIR \
  && rm -rf $DIRECTOR_SOURCE_DIR \
  && rm -rf $DIRECTOR_BUILD_DIR
