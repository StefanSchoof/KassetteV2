#!/bin/bash
set -e
function pullarmimage {
  # since the platform arg needs experimental daemon and there is no way do activate experimental daemon on azure pipeline => a hack...
  imagename=${1%:*}
  digest=$(DOCKER_CLI_EXPERIMENTAL="enabled" docker manifest inspect $1 | jq --raw-output '.manifests[] | select(.platform.architecture == "arm" and .platform.variant == "v5").digest')
  docker pull $imagename@$digest
  docker tag $imagename@$digest $1
}

# in azure pipeline git is in detached head so git does not know it brach and we take the env var. But these are in the format /ref/head/master, so we take the basename
branch=$(basename ${BUILD_SOURCEBRANCH:-$(git rev-parse --abbrev-ref HEAD)})
targets=( )
image="stefanschoof/kassettev2arm32v7"
# enable cross compile with on not arm devices
if [[ ! $(uname -m) == arm* ]]
then
  docker run --rm --privileged multiarch/qemu-user-static:register --reset
  for baseimage in $(sed -n 's/^FROM \([^ ]*\).*/\1/p' Dockerfile | sort --uniq)
  do
    pullarmimage $baseimage
  done
  targets=( qemu ${targets[@]} )
  dockerfilearg="-f Dockerfile_x86"
  sed 's/#x86only //' Dockerfile > Dockerfile_x86
fi

# cache-from does not work with multistage, see https://github.com/moby/moby/issues/34715
for target in "${targets[@]}"
do
  tag=$image:build-cache-$target
  if [[ ! -z "$USECACHEFROM" ]]
  then
    cachefrom+="--cache-from $tag "
    docker pull $tag || true
  fi
  docker build --target $target \
    $cachefrom \
    $dockerfilearg \
    -t $tag .
  if [[ ! -z "$PUSH" ]]
  then
    docker push $tag
  fi
done

if [[ ! -z "$USECACHEFROM" ]]
then
  cachefrom+="--cache-from $image:$branch"
  docker pull $image:$branch || true
fi

if [[ ! -z "$BUILD_BUILDID" ]]
then
  buildtag="-t $image:build$BUILD_BUILDID "
fi

docker build \
  $cachefrom \
  $dockerfilearg \
  $buildtag \
  -t $image:$branch .

if [[ ! -z "$PUSH" ]]
then
  docker push $image:${branch}
  docker push $image:build${BUILD_BUILDID}
fi
