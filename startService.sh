#!/bin/bash
echo "========== Starting Webserver..."
nginx
echo "========== Starting Backend Service..."
python CIBackendService.python
