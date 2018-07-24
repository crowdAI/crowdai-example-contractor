#!/bin/bash

ARG=$1

source environ.sh
if [ "$ARGS" = "build_push" ]; then
  docker push ${IMAGE_NAME}
fi

REDIS_HOST="localhost"
OS=$(uname -s)
if [ "$OS" = "Darwin" ]; then
	REDIS_HOST="docker.for.mac.host.internal"
fi

docker run -it \
  --net=host \
  -e CROWDAI_REDIS_HOST=$REDIS_HOST \
  -e CROWDAI_IS_GRADING=True \
  -e CROWDAI_DEBUG_MODE=True \
  $IMAGE_NAME \
  /home/crowdai/run.sh
