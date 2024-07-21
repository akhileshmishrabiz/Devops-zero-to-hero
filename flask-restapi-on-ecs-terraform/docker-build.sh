#!/bin/sh

if [ ! $# -eq 3 ]
  then
    echo "Argument error"
    usage="<ECR_REPO_URL> <ECR_TOKEN> <IMAGE_TAGE>"
    echo  "usage: ${0} ${usage}"
    exit 1
fi

REPO_URL=$1
ECR_TOKEN=$2
IMAGE_TAG=$3

AWS_ECR="${REPO_URL%/*}"
echo "Docker login to ${AWS_ECR}"
echo ${ECR_TOKEN} | docker login --username AWS --password-stdin "${AWS_ECR}"

echo "Building Image"
echo "docker build --platform=linux/amd64 -t \"${REPO_URL}:${IMAGE_TAG}\" ."
docker build --quiet --platform=linux/amd64 -t "${REPO_URL}:${IMAGE_TAG}" .
echo "Pushing Image to ${AWS_ECR}"
echo "docker push \"${REPO_URL}:${IMAGE_TAG}\""
docker push --quiet "${REPO_URL}:${IMAGE_TAG}"