#!/bin/bash
echo "========== Starting Backend Service..."
python CIBackendService.py &
echo "========== Starting Webserver..."
nginx
