#!/bin/bash

ARG=$1

source environ.sh
./build.sh push

docker run -it \
  --net=host \
  -e CROWDAI_IS_GRADING=True \
  -e CROWDAI_DEBUG_MODE=True \
  $IMAGE_NAME \
  /home/crowdai/run.sh
