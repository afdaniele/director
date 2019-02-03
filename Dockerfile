# FROM ripl/libbot2:latest
FROM innerspace/docker-pcl:ubuntu_16.04

# set working directory
ENV WORKDIR "/code"
WORKDIR /code

# set environment
ENV DIRECTOR_VERSION "ND"
ENV DIRECTOR_ORIGIN "https://github.com/afdaniele/director"
ENV DIRECTOR_SHA "230b770a50d0b85599c815e1d3b230a96608f383"
ENV DIRECTOR_SOURCE_DIR "$WORKDIR/director"
ENV DIRECTOR_BUILD_DIR "$WORKDIR/director-build"
ENV DIRECTOR_INSTALL_DIR "$WORKDIR/director-install"

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
        python3-dev \
        python3-lxml \
        python3-numpy \
        python3-scipy \
        python3-yaml \
    && rm -rf /var/lib/apt/lists/*

# retrieve source code
RUN git clone $DIRECTOR_ORIGIN $DIRECTOR_SOURCE_DIR \
    && cd $DIRECTOR_SOURCE_DIR \
    && git fetch origin $DIRECTOR_SHA \
    && git checkout $DIRECTOR_SHA

# build director
RUN mkdir -p $DIRECTOR_BUILD_DIR \
  && cd $DIRECTOR_BUILD_DIR \
  && cmake \
  -DCMAKE_CXX_FLAGS_RELEASE="-fPIC -g -fno-omit-frame-pointer -O3 -DNDEBUG" \
  -DCMAKE_BUILD_TYPE=Release \
  -DUSE_PCL:BOOL=ON \
  -DUSE_LCM:BOOL=ON \
  -DUSE_SIGNAL_SCOPE:BOOL=OFF \
  -DUSE_SYSTEM_VTK:BOOL=OFF \
  -DUSE_SYSTEM_PCL:BOOL=ON \
  -DUSE_SYSTEM_EIGEN:BOOL=ON \
  -DUSE_EXTERNAL_INSTALL:BOOL=ON \
  -DCMAKE_INSTALL_PREFIX:PATH=$DIRECTOR_INSTALL_DIR \
  $DIRECTOR_SOURCE_DIR/distro/superbuild

RUN cd $DIRECTOR_BUILD_DIR && make -j

ENV PATH=/code/software/build/bin:$PATH
