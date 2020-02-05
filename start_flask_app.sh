#!/bin/bash

. ./venv/bin/activate
gunicorn example:flask_app -b 0.0.0.0:8000

