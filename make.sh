#!/bin/bash

sudo docker container rm fake
sudo docker image rm fake

sudo docker build -t fake .
sudo docker run --name fake fake




