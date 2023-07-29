#!/bin/bash

if [ -z "$1" ]; then
  echo "Use: ./build-docker.sh <tag>"
  exit 1
fi

tag="$1"
userName="reoskaro434"
repositoryName="web-scrapper"

dockerImageName="$userName/$repositoryName:$tag"

echo "Building Docker image: $dockerImageName"

docker build -t "$dockerImageName" .


docker tag "$userName/$repositoryName:$tag" "$userName/$repositoryName:latest"
