#!/bin/bash

xhost +local:root;

nvidia-docker run --rm -it --privileged -e DISPLAY \
  --net=host \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $PWD:/local \
  -w /director \
  -e HOST_NAME=shasta nvidia/cuda:9.2-devel-ubuntu18.04 bash

xhost -local:root;
