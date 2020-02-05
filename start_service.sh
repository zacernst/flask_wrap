#!/bin/bash
gunicorn example:flask_app -b 0.0.0.0
