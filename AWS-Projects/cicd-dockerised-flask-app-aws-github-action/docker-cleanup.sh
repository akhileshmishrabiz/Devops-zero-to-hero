#!/bin/bash

# Check if there are containers
if [ -n "$(docker ps -aq)" ]; then
    # Remove containers
    docker rm -f $(docker ps -aq)
else
    echo "No containers to remove."
fi

# Check if there are images
if [ -n "$(docker images -q)" ]; then
    # Remove images
    docker rmi $(docker images -q)
else
    echo "No images to remove."
fi
