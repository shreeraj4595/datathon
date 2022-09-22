#!/bin/sh
echo "Stopping running docker container"
docker stop datathon

echo "Removing existing docker container"
docker rm datathon

echo "Building new docker image"
docker build -t datathon-datacrafters .

echo "Starting docker container"
docker run -d --name datathon -p 11202:11202 datathon-datacrafters:latest

echo "Docker container is now running successfully. docker ps to check running container"