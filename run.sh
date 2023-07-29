#!/bin/bash

CONTAINER_NAME="web-scrapper-container"
tag="latest"
userName="reoskaro434"
repositoryName="web-scrapper"
originPathName="/mnt/e/projects/web-scrapper/src"
containerPathName="/web-scrapper"


if docker ps -a | grep -q "$CONTAINER_NAME"; then
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 # >/dev/null 2>&1  clears console
fi

docker run --name "$CONTAINER_NAME" -v "$originPathName:$containerPathName" "$userName/$repositoryName:$tag"
