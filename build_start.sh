#!/bin/bash
sudo docker build -t flask_wrap:latest .
sudo docker run -p 8000:8000 -it flask_wrap
