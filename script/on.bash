#!/bin/bash

docker build -f experiment_scheduler.dockerfile . -t experiment_scheduler

docker-compose -f docker-compose.yaml up -d
