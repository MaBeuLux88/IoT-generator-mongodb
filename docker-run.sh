#!/usr/bin/env bash
docker run --rm --name iot-generator-mongodb -v $(pwd):/home -w /home --network host python:3.9.0 /bin/bash -c "pip install -r requirements.txt; python importiot.py '${1}'"

