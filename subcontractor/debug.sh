#!/bin/bash

ARG=$1

source environ.sh
if [ "$ARGS" = "build_push" ]; then
  docker push ${IMAGE_NAME}
fi


docker run -it \
  --net=host \
  -e CROWDAI_IS_GRADING=True \
  -e CROWDAI_DEBUG_MODE=True \
  $IMAGE_NAME \
  /home/crowdai/run.sh
